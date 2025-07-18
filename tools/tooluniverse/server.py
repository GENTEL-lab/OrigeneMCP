from asyncio import to_thread
from mcp import types
from typing import List, get_origin, Callable, Any
import json
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools import Tool
from mcp.types import ToolAnnotations
import inspect
from mcp.server.fastmcp.utilities.func_metadata import (
    _get_typed_signature,
    _get_typed_annotation,
    ArgModelBase,
    FuncMetadata,
)
from typing import Awaitable
from collections.abc import Awaitable, Callable, Sequence
from typing import (
    Annotated,
)

from pydantic import Field, WithJsonSchema, create_model
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from mcp.server.fastmcp.exceptions import InvalidSignature
from typing import Sequence

from tools.tooluniverse import ToolUniverse

tn = ToolUniverse()
tn.load_tools()


class MyFuncMetaData(FuncMetadata):
    async def call_fn_with_arg_validation(
        self,
        fn: Callable[..., Any] | Awaitable[Any],
        fn_is_async: bool,
        arguments_to_validate: dict[str, Any],
        arguments_to_pass_directly: dict[str, Any] | None,
    ) -> Any:
        arguments_parsed_dict = arguments_to_validate
        if fn_is_async:
            if isinstance(fn, Awaitable):
                return await fn
            return await fn(**arguments_parsed_dict)
        if isinstance(fn, Callable):
            return fn(**arguments_parsed_dict)
        raise TypeError("fn must be either Callable or Awaitable")


def func_metadata(
    func: Callable[..., Any], skip_names: Sequence[str] = ()
) -> FuncMetadata:
    """Given a function, return metadata including a pydantic model representing its
    signature.

    The use case for this is
    ```
    meta = func_to_pyd(func)
    validated_args = meta.arg_model.model_validate(some_raw_data_dict)
    return func(**validated_args.model_dump_one_level())
    ```

    **critically** it also provides pre-parse helper to attempt to parse things from
    JSON.

    Args:
        func: The function to convert to a pydantic model
        skip_names: A list of parameter names to skip. These will not be included in
            the model.
    Returns:
        A pydantic model representing the function's signature.
    """
    sig = _get_typed_signature(func)
    params = sig.parameters
    dynamic_pydantic_model_params: dict[str, Any] = {}
    globalns = getattr(func, "__globals__", {})
    for param in params.values():
        if param.name.startswith("_"):
            raise InvalidSignature(
                f"Parameter {param.name} of {func.__name__} cannot start with '_'"
            )
        if param.name in skip_names:
            continue
        annotation = param.annotation

        # `x: None` / `x: None = None`
        if annotation is None:
            annotation = Annotated[
                None,
                Field(
                    default=(
                        param.default
                        if param.default is not inspect.Parameter.empty
                        else PydanticUndefined
                    )
                ),
            ]

        # Untyped field
        if annotation is inspect.Parameter.empty:
            annotation = Annotated[
                Any,
                Field(),
                # 🤷
                WithJsonSchema({"title": param.name, "type": "string"}),
            ]

        field_info = FieldInfo.from_annotated_attribute(
            _get_typed_annotation(annotation, globalns),
            (
                param.default
                if param.default is not inspect.Parameter.empty
                else PydanticUndefined
            ),
        )
        dynamic_pydantic_model_params[param.name] = (field_info.annotation, field_info)
        continue

    arguments_model = create_model(
        f"{func.__name__}Arguments",
        **dynamic_pydantic_model_params,
        __base__=ArgModelBase,
    )
    resp = MyFuncMetaData(arg_model=arguments_model)
    return resp


# 因为FastMCP的封装add_tool无法指定parameters，所以把一些代码copy出来重写
def from_function(
    fn: Callable[..., Any],
    name: str | None = None,
    description: str | None = None,
    parameters: Any = None,
    context_kwarg: str | None = None,
    annotations: ToolAnnotations | None = None,
) -> Tool:
    """Create a Tool from a function."""
    from mcp.server.fastmcp.server import Context

    func_name = name or fn.__name__

    if func_name == "<lambda>":
        raise ValueError("You must provide a name for lambda functions")

    func_doc = description or fn.__doc__ or ""
    is_async = inspect.iscoroutinefunction(fn)

    if context_kwarg is None:
        sig = inspect.signature(fn)
        for param_name, param in sig.parameters.items():
            if get_origin(param.annotation) is not None:
                continue
            if issubclass(param.annotation, Context):
                context_kwarg = param_name
                break
    func_arg_metadata = func_metadata(
        fn,
        skip_names=[context_kwarg] if context_kwarg is not None else [],
    )
    if parameters is None:
        parameters = func_arg_metadata.arg_model.model_json_schema()
    # func_arg_metadata.call_fn_with_arg_validation = call_fn_with_arg_validation
    # print("model dump", func_arg_metadata.arg_model.model_dump())
    return Tool(
        fn=fn,
        name=func_name,
        description=func_doc,
        parameters=parameters,
        fn_metadata=func_arg_metadata,
        is_async=is_async,
        context_kwarg=context_kwarg,
        annotations=annotations,
    )


def get_all_tools(tools: List):
    all_tools = []
    for t in tools:
        input_schema = t["parameter"]
        parameters = input_schema
        tool = from_function(
            get_func(t["name"]),
            name=t["name"],
            description=t["description"],
            parameters=parameters,
        )
        all_tools.append(tool)
    return all_tools


def get_func(name: str):
    async def f(**arguments):
        def run():
            result = tn.run(
                {
                    "name": name,
                    "arguments": arguments,
                }
            )
            if type(result) != str:
                result = json.dumps(result)
            return types.TextContent(type="text", text=str(result))

        return await to_thread(run)

    return f


fda_drug_mcp = FastMCP(
    name="fda_drug_mcp",
    tools=get_all_tools(tn.tool_category_dicts["fda_drug_label"]),
    stateless_http=True,
)
monarch_mcp = FastMCP(
    name="monarch_mcp",
    tools=get_all_tools(tn.tool_category_dicts["monarch"]),
    stateless_http=True,
)

opentargets_mcp = FastMCP(
    name="opentargets_mcp",
    tools=get_all_tools(tn.tool_category_dicts["opentarget"]),
    stateless_http=True,
)


@opentargets_mcp.tool()
async def get_general_info_by_disease_name(name: str):
    """
    Get disease EFO ID and description by disease name from OpenTargets.
    Description information will include disease name, EFO ID, disease targets, related drugs and related disease phenotypes.

    Args:
        name: The disease name to search for

    Returns:
        Dictionary containing disease ID and related information including targets, drugs and phenotypes
    """

    final_result = {}
    final_result["disease_name"] = name

    # Get disease EFO ID
    result = tn.run(
        {
            "name": "get_disease_id_description_by_name",
            "arguments": {"diseaseName": name},
        }
    )

    try:
        efoId = result["data"]["search"]["hits"][0]["id"]
        final_result["efoId"] = efoId
    except Exception as e:
        print(e)
        return final_result

    # Get disease targets information
    raw_target_info = tn.run(
        {
            "name": "get_associated_targets_by_disease_efoId",
            "arguments": {"efoId": efoId},
        }
    )
    try:
        final_result["disease_targets"] = raw_target_info["data"]["disease"][
            "associatedTargets"
        ].get("rows", [])
    except Exception as e:
        print(e)
        final_result["disease_targets"] = []

    # Get disease associated drugs information
    raw_drug_info = tn.run(
        {
            "name": "get_associated_drugs_by_disease_efoId",
            "arguments": {"efoId": efoId, "size": 10},
        }
    )
    try:
        final_result["disease_drugs"] = raw_drug_info["data"]["disease"][
            "knownDrugs"
        ].get("rows", [])
    except Exception as e:
        print(e)
        final_result["disease_drugs"] = []

    # Get disease associated phenotypes information
    raw_phenotype_info = tn.run(
        {
            "name": "get_associated_phenotypes_by_disease_efoId",
            "arguments": {"efoId": efoId},
        }
    )
    try:
        final_result["disease_phenotypes"] = raw_phenotype_info["data"]["disease"][
            "phenotypes"
        ].get("rows", [])
    except Exception as e:
        print(e)
        final_result["disease_phenotypes"] = []

    return final_result


@opentargets_mcp.tool()
async def get_target_ensembl_id(target_name: str):
    """
    Get target Ensembl ID by target name.
    
    Args:
        target_name: The target name to search for
        
    """
    result = tn.run({
        "name": "get_target_id_description_by_name", 
        "arguments": {"targetName": target_name}
    })
    try:
        return result['data']['search']['hits'][0]['id']
    except:
        return None

@opentargets_mcp.tool()
async def get_disease_efo_id(disease_name: str):
    """
    Get disease EFO ID by disease name.
    
    Args:
        disease_name: The disease name to search for
    """
    result = tn.run({
        "name": "get_disease_id_description_by_name", 
        "arguments": {"diseaseName": disease_name}
    })
    try:
        return result['data']['search']['hits'][0]['id']
    except:
        return None

@opentargets_mcp.tool()
async def get_drug_chembl_id_by_name(drug_name: str):
    """
    Find drug ChEMBL ID by drug name.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    result = tn.run({
        "name": "get_drug_id_description_by_name", 
        "arguments": {"drugName": drug_name}
    })
    try:
        return result['data']['search']['hits'][0]['id']
    except:
        return None

@opentargets_mcp.tool()
async def get_associated_targets_by_disease_name(disease_name: str):
    """
    Find targets associated with a specific disease or phenotype based on its name.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_associated_targets_by_disease_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result

@opentargets_mcp.tool()
async def get_associated_diseases_phenotypes_by_target_name(target_name: str):
    """
    Find diseases or phenotypes associated with a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_associated_diseases_phenotypes_by_target_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_disease_evidence_by_name(target_name: str, disease_name: str):
    """
    Explore evidence that supports a specific target-disease association. Input is disease name and target name.
    
    Args:
        target_name: The target name to search for
        disease_name: The disease name to search for
    
    Query example: {"target_name": "BRCA1", "disease_name": "Breast cancer"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    efo_id = await get_disease_efo_id(disease_name)
    if target_ensembl_id is None or efo_id is None:
        result = 'No target or disease found'
    else:
        result = tn.run({
            "name": "target_disease_evidence", 
            "arguments": {"ensemblId": target_ensembl_id, "efoId": efo_id}
        })
    return result
    

@opentargets_mcp.tool()
async def get_drug_warnings_by_name(drug_name: str):
    """
    Retrieve warnings for a specific drug.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    chembl_id = await get_drug_chembl_id_by_name(drug_name)
    if chembl_id is None:   
        result = 'No drug found'
    else:
        result = tn.run({
            "name": "get_drug_warnings_by_chemblId", 
            "arguments": {"chemblId": chembl_id}
        })
    return result


@opentargets_mcp.tool()
async def get_drug_mechanisms_of_action_by_name(drug_name: str):
    """
    Retrieve the mechanisms of action associated with a specific drug.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    chembl_id = await get_drug_chembl_id_by_name(drug_name)
    if chembl_id is None:
        result = 'No drug found'
    else:
        result = tn.run({
            "name": "get_drug_mechanisms_of_action_by_chemblId", 
            "arguments": {"chemblId": chembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_associated_drugs_by_disease_name(disease_name: str):
    """
    Retrieve known drugs associated with a specific disease by disease name.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_associated_drugs_by_disease_efoId", 
            "arguments": {"efoId": efo_id, "size": 10}
        })
    return result


@opentargets_mcp.tool()
async def get_similar_entities_by_disease_name(disease_name: str):
    """
    Retrieve similar entities for a given disease using a model trained with PubMed.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_similar_entities_by_disease_efoId", 
            "arguments": {"efoId": efo_id, "threshold": 0.2, "size": 10}
        })
    return result

@opentargets_mcp.tool()
async def get_similar_entities_by_drug_name(drug_name: str):
    """
    Retrieve similar entities for a given drug using a model trained with PubMed.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    chembl_id = await get_drug_chembl_id_by_name(drug_name)
    if chembl_id is None:
        result = 'No drug found'
    else:
        result = tn.run({
            "name": "get_similar_entities_by_drug_chemblId", 
            "arguments": {"chemblId": chembl_id, "threshold": 0.2, "size": 10}
        })
    return result


@opentargets_mcp.tool()
async def get_similar_entities_by_target_name(target_name: str):
    """
    Retrieve similar entities for a given target using a model trained with PubMed.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_similar_entities_by_target_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id, "threshold": 0.2, "size": 10}
        })
    return result

@opentargets_mcp.tool()
async def get_associated_phenotypes_by_disease_name(disease_name: str):
    """
    Find HPO phenotypes asosciated with the specified disease.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_associated_phenotypes_by_disease_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result


@opentargets_mcp.tool()
async def get_drug_indications_by_name(drug_name: str):
    """
    Fetch indications (treatable phenotypes/diseases) for a given drug.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    chembl_id = await get_drug_chembl_id_by_name(drug_name)
    if chembl_id is None:
        result = 'No drug found'
    else:
        result = tn.run({
            "name": "get_drug_indications_by_chemblId", 
            "arguments": {"chemblId": chembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_gene_ontology_by_name(target_name: str):
    """
    Retrieve Gene Ontology annotations for a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_gene_ontology_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_homologues_by_name(target_name: str):
    """
    Fetch homologues for a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_homologues_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_safety_profile_by_name(target_name: str):
    """
    Retrieve known target safety liabilities for a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_safety_profile_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_biological_mouse_models_by_target_name(target_name: str):
    """
    Retrieve biological mouse models, including allelic compositions and genetic backgrounds, for a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_biological_mouse_models_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_genomic_location_by_name(target_name: str):
    """
    Retrieve genomic location data for a specific target, including chromosome, start, end, and strand.
    
    Args:
        target_name: The target name to search for

    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_genomic_location_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_subcellular_locations_by_name(target_name: str):
    """
    Retrieve information about subcellular locations for a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_subcellular_locations_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_synonyms_by_name(target_name: str):
    """
    Retrieve synonyms for specified target, including alternative names and symbols.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_synonyms_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_tractability_by_name(target_name: str):
    """
    Retrieve tractability assessments, including modality and values.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_tractability_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_classes_by_name(target_name: str):
    """
    Retrieve the target classes associated with a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_classes_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_enabling_packages_by_name(target_name: str):
    """
    Retrieve the Target Enabling Packages (TEP) associated with a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_enabling_packages_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_target_interactions_by_name(target_name: str):
    """
    Retrieve interaction data for a specific target, including interaction partners and evidence.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_interactions_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result


@opentargets_mcp.tool()
async def get_disease_ancestors_parents_by_name(disease_name: str):
    """
    Retrieve the ancestors and parents of a specific disease.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_disease_ancestors_parents_by_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result


@opentargets_mcp.tool()
async def get_disease_descendants_children_by_name(disease_name: str):
    """
    Retrieve the descendants and children of a specific disease.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_disease_descendants_children_by_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result


@opentargets_mcp.tool()
async def get_disease_locations_by_name(disease_name: str):
    """
    Retrieve the locations of a specific disease.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_disease_locations_by_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result

@opentargets_mcp.tool()
async def get_disease_synonyms_by_name(disease_name: str):
    """
    Retrieve synonyms for a specific disease.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_disease_synonyms_by_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result

@opentargets_mcp.tool()
async def get_disease_description_by_name(disease_name: str):
    """
    Retrieve the description of a specific disease.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_disease_description_by_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result

@opentargets_mcp.tool()
async def get_disease_therapeutic_areas_by_name(disease_name: str):
    """
    Retrieve the therapeutic areas associated with a specific disease.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_disease_therapeutic_areas_by_efoId", 
            "arguments": {"efoId": efo_id}
        })
    return result


@opentargets_mcp.tool()
async def get_chemical_probes_by_target_name(target_name: str):
    """
    Retrieve chemical probes associated with a specific target.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({   
            "name": "get_chemical_probes_by_target_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_associated_drugs_by_target_name(target_name: str):
    """
    Get known drugs associated with a specific target, including clinical trial phase and mechanism of action of the drugs.
    
    Args:
        target_name: The target name to search for

    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_associated_drugs_by_target_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id, "size": 10}
        })
    return result


@opentargets_mcp.tool()
async def get_associated_diseases_by_drug_name(drug_name: str):
    """
    Retrieve the list of diseases associated with a specific drug based on clinical trial data or post-marketed drugs.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    chembl_id = await get_drug_chembl_id_by_name(drug_name)
    if chembl_id is None:
        result = 'No drug found'
    else:
        result = tn.run({
            "name": "get_associated_diseases_by_drug_chemblId", 
            "arguments": {"chemblId": chembl_id}
        })
    return result


@opentargets_mcp.tool()
async def get_associated_targets_by_drug_name(drug_name: str):
    """
    Retrieve the list of targets linked to a specific drug based on its mechanism of action.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    chembl_id = await get_drug_chembl_id_by_name(drug_name)
    if chembl_id is None:
        result = 'No drug found'
    else:
        result = tn.run({
            "name": "get_associated_targets_by_drug_chemblId", 
            "arguments": {"chemblId": chembl_id}
        })
    return result


@opentargets_mcp.tool()
async def get_target_constraint_info_by_name(target_name: str):
    """
    Retrieve genetic constraint information for a specific target, including expected and observed values, and scores.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_target_constraint_info_by_ensemblID", 
            "arguments": {"ensemblId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_publications_by_disease_name(disease_name: str):
    """
    Retrieve publications related to a disease name, including PubMed IDs and publication dates.
    
    Args:
        disease_name: The disease name to search for
        
    Query example: {"disease_name": "Breast cancer"}
    """
    efo_id = await get_disease_efo_id(disease_name)
    if efo_id is None:
        result = 'No disease found'
    else:
        result = tn.run({
            "name": "get_publications_by_disease_efoId", 
            "arguments": {"entityId": efo_id}
        })
    return result

@opentargets_mcp.tool()
async def get_publications_by_target_name(target_name: str):
    """
    Retrieve publications related to a target, including PubMed IDs and publication dates.
    
    Args:
        target_name: The target name to search for
        
    Query example: {"target_name": "BRCA1"}
    """
    target_ensembl_id = await get_target_ensembl_id(target_name)
    if target_ensembl_id is None:
        result = 'No target found'
    else:
        result = tn.run({
            "name": "get_publications_by_target_ensemblID", 
            "arguments": {"entityId": target_ensembl_id}
        })
    return result

@opentargets_mcp.tool()
async def get_publications_by_drug_name(drug_name: str):
    """
    Retrieve publications related to a drug, including PubMed IDs and publication dates.
    
    Args:
        drug_name: The drug name to search for
        
    Query example: {"drug_name": "aspirin"}
    """
    chembl_id = await get_drug_chembl_id_by_name(drug_name)
    if chembl_id is None:
        result = 'No drug found'
    else:
        result = tn.run({
            "name": "get_publications_by_drug_chemblId", 
            "arguments": {"entityId": chembl_id}
        })
    return result


app = FastMCP(
    name="tooluniverse_mcp",
    tools=get_all_tools(tn.all_tools),
    stateless_http=True,
)

