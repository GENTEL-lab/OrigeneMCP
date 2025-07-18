from mcp import types
from mcp.server.fastmcp import FastMCP

from tools.pdb.pdb_api import PDBAPI


mcp = FastMCP(
    name="pdb_mcp",
    stateless_http=True,
)

pdb_api = PDBAPI()


# Entry-related tools
@mcp.tool()
async def pdb_get_structure(entry_id: str):
    """
    Retrieve detailed structure information for a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of structure information including:
                - 'rcsb_id': PDB ID
                - 'rcsb_accession_info': accession details  
                - 'struct': structure metadata
                - 'exptl': experimental details
                - 'citation': publication info
                - 'cell': unit cell parameters
                - 'symmetry': symmetry info
                - 'pdbx_database_status': entry status
                
        Returns empty list if entry not found or error occurs.
    
    Query example: {"entry_id": "1CRN"}
    """
    result = pdb_api.get_structure(entry_id)
    return result

@mcp.tool()
async def pdb_get_pubmed_annotations(entry_id: str):
    """
    Retrieve PubMed literature annotations for a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of PubMed annotations including:
                - 'rcsb_id': PDB ID
                - 'pubmed': list of PubMed articles with:
                    - 'id': PubMed ID
                    - 'title': article title
                    - 'journal': journal info
                    - 'authors': author list
                    - 'year': publication year
                    
        Returns empty list if no annotations found or error occurs.
        
    Query example: {"entry_id": "1CRN"}
    """
    result = pdb_api.get_pubmed_annotations(entry_id)
    return result

# Entity-related tools
@mcp.tool()
async def pdb_get_polymer_entity(entry_id: str, entity_id: str):
    """
    Retrieve detailed information about a polymer entity in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        entity_id (str): The polymer entity identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of polymer entity info including:
                - 'entity': 
                    - 'id': entity ID
                    - 'type': entity type (e.g. "polymer")
                    - 'src_method': source method
                    - 'pdbx_description': description
                    - 'pdbx_number_of_molecules': molecule count
                    - 'pdbx_ec': EC numbers
                    - 'pdbx_mutation': mutation info
                    - 'pdbx_fragment': fragment info
                - 'rcsb_polymer_entity':
                    - 'container_identifiers': container info
                    - 'entity_poly': polymer details
                    
        Returns empty list if entity not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_polymer_entity(entry_id, entity_id)
    return result

@mcp.tool()
async def pdb_get_branched_entity(entry_id: str, entity_id: str):
    """
    Retrieve detailed information about a branched entity in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        entity_id (str): The branched entity identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of branched entity info including:
                - 'entity':
                    - 'id': entity ID
                    - 'type': entity type (e.g. "branched")
                    - 'pdbx_description': description
                    - 'pdbx_number_of_molecules': molecule count
                - 'rcsb_branched_entity':
                    - 'container_identifiers': container info
                    - 'branched_entity': branched details
                    - 'branched_entity_instance_count': instance count
                    
        Returns empty list if entity not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_branched_entity(entry_id, entity_id)
    return result

@mcp.tool()
async def pdb_get_nonpolymer_entity(entry_id: str, entity_id: str):
    """
    Retrieve detailed information about a non-polymer entity in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        entity_id (str): The non-polymer entity identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of non-polymer entity info including:
                - 'entity':
                    - 'id': entity ID
                    - 'type': entity type (e.g. "non-polymer")
                    - 'pdbx_description': description
                    - 'pdbx_number_of_molecules': molecule count
                - 'rcsb_non_polymer_entity':
                    - 'container_identifiers': container info
                    - 'non_polymer_comp': chemical component details
                    - 'non_polymer_entity_instance_count': instance count
                    
        Returns empty list if entity not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_non_polymer_entity(entry_id, entity_id)
    return result

# Entity instance tools
@mcp.tool()
async def pdb_get_polymer_entity_instance(entry_id: str, instance_id: str):
    """
    Retrieve detailed information about a polymer entity instance in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        instance_id (str): The polymer entity instance identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of polymer entity instance info including:
                - 'rcsb_polymer_entity_instance':
                    - 'id': instance ID
                    - 'asym_id': asymmetric unit ID
                    - 'auth_asym_id': author asymmetric unit ID
                    - 'entity_id': parent entity ID
                    - 'transformation': transformation matrix
                    - 'struct_asym': structure asymmetric unit info
                    - 'rcsb_polymer_entity_instance_container_identifiers': container info
                    
        Returns empty list if instance not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "instance_id": "1"}
    """
    result = pdb_api.get_polymer_entity_instance(entry_id, instance_id)
    return result

@mcp.tool()
async def pdb_get_branched_entity_instance(entry_id: str, instance_id: str):
    """
    Retrieve detailed information about a branched entity instance in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        instance_id (str): The branched entity instance identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of branched entity instance info including:
                - 'rcsb_branched_entity_instance':
                    - 'id': instance ID
                    - 'asym_id': asymmetric unit ID
                    - 'auth_asym_id': author asymmetric unit ID
                    - 'entity_id': parent entity ID
                    - 'transformation': transformation matrix
                    - 'struct_asym': structure asymmetric unit info
                    - 'rcsb_branched_entity_instance_container_identifiers': container info
                    
        Returns empty list if instance not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "instance_id": "1"}
    """
    result = pdb_api.get_branched_entity_instance(entry_id, instance_id)
    return result

@mcp.tool()
async def pdb_get_nonpolymer_entity_instance(entry_id: str, instance_id: str):
    """
    Retrieve detailed information about a non-polymer entity instance in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        instance_id (str): The non-polymer entity instance identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of non-polymer entity instance info including:
                - 'rcsb_non_polymer_entity_instance':
                    - 'id': instance ID
                    - 'asym_id': asymmetric unit ID
                    - 'auth_asym_id': author asymmetric unit ID
                    - 'entity_id': parent entity ID
                    - 'transformation': transformation matrix
                    - 'struct_asym': structure asymmetric unit info
                    - 'rcsb_non_polymer_entity_instance_container_identifiers': container info
                    
        Returns empty list if instance not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "instance_id": "1"}
    """
    result = pdb_api.get_non_polymer_entity_instance(entry_id, instance_id)
    return result

# Annotation tools
@mcp.tool()
async def pdb_get_uniprot_annotations(entry_id: str, entity_id: str):
    """
    Retrieve UniProt annotations for a polymer entity in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        entity_id (str): The polymer entity identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of UniProt annotations including:
                - 'rcsb_id': PDB ID
                - 'entity_id': entity ID
                - 'uniprot_accession': UniProt accession number
                - 'uniprot_id': UniProt ID
                - 'uniprot_name': protein name
                - 'uniprot_description': protein description
                - 'uniprot_sequence': protein sequence
                - 'uniprot_organism': source organism
                - 'uniprot_gene': gene name
                - 'uniprot_domain': domain annotations
                
        Returns empty list if no annotations found or error occurs.
        
    Query example: {"entry_id": "1CRN", "entity_id": "1"}
    """
    result = pdb_api.get_uniprot_annotations(entry_id, entity_id)
    return result

@mcp.tool()
async def pdb_get_drugbank_annotations(component_id: str):
    """
    Retrieve DrugBank annotations for a chemical component in PDB.
    
    Args:
        component_id (str): The 3-letter chemical component ID (e.g. "ATP", "HEM")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of DrugBank annotations including:
                - 'drugbank_id': DrugBank ID
                - 'name': drug name
                - 'description': drug description
                - 'groups': drug groups (e.g. approved, experimental)
                - 'indication': therapeutic indications
                - 'pharmacology': pharmacological action
                - 'mechanism_of_action': mechanism description
                - 'toxicity': toxicity information
                - 'metabolism': metabolic pathway
                - 'targets': list of drug targets with:
                    - 'uniprot_id': UniProt ID
                    - 'gene_name': gene name
                    - 'action': drug action on target
                    
        Returns empty list if no annotations found or error occurs.
        
    Query example: {"component_id": "ATP"}
    """
    result = pdb_api.get_drugbank_annotations(component_id)
    return result

# Assembly tools
@mcp.tool()
async def pdb_get_structural_assembly(entry_id: str, assembly_id: str = "1"):
    """
    Retrieve structural assembly information for a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        assembly_id (str): The assembly identifier (default: "1")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of assembly information including:
                - 'rcsb_struct_assembly':
                    - 'id': assembly ID
                    - 'details': assembly description
                    - 'method': assembly method
                    - 'oligomeric_details': oligomeric state
                    - 'polymer_entity_instance_count': instance count
                    - 'rcsb_struct_assembly_provenance': provenance info
                    - 'rcsb_struct_assembly_container_identifiers': container info
                - 'assemblies': list of assembly components with:
                    - 'assembly_id': component ID
                    - 'asym_id_list': list of asymmetric unit IDs
                    - 'transformation': transformation matrix
                    
        Returns empty list if assembly not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "assembly_id": "1"}
    """
    result = pdb_api.get_structural_assembly(entry_id, assembly_id)
    return result

# Interface tools
@mcp.tool()
async def pdb_get_polymer_interface(entry_id: str, assembly_id: str, interface_id: str):
    """
    Retrieve detailed information about a polymer interface in a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        assembly_id (str): The assembly identifier (usually "1", "2", etc.)
        interface_id (str): The interface identifier (usually "1", "2", etc.)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of interface information including:
                - 'rcsb_interface_info':
                    - 'id': interface ID
                    - 'interface_area': interface area in Å²
                    - 'solvent_content': solvent content percentage
                    - 'interface_type': interface classification
                    - 'interface_chemistry': chemical composition
                - 'interface_partner':
                    - 'asym_id': list of asymmetric unit IDs
                    - 'entity_id': list of entity IDs
                    - 'interface_residues': list of interface residues
                - 'interface_features':
                    - 'hydrogen_bonds': count and details
                    - 'salt_bridges': count and details
                    - 'disulfide_bonds': count and details
                    
        Returns empty list if interface not found or error occurs.
        
    Query example: {"entry_id": "1CRN", "assembly_id": "1", "interface_id": "1"}
    """
    result = pdb_api.get_polymer_interface(entry_id, assembly_id, interface_id)
    return result

# Chemical component tools
@mcp.tool()
async def pdb_get_chemical_component(component_id: str):
    """
    Retrieve detailed information about a chemical component in PDB.
    
    Args:
        component_id (str): The 3-letter chemical component ID (e.g. "ATP", "HEM")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of chemical component information including:
                - 'chem_comp':
                    - 'id': component ID
                    - 'name': component name
                    - 'type': component type
                    - 'formula': chemical formula
                    - 'formula_weight': molecular weight
                    - 'pdbx_formal_charge': formal charge
                    - 'pdbx_initial_date': date added
                    - 'pdbx_modified_date': last modified
                    - 'pdbx_release_status': release status
                - 'pdbx_chem_comp_descriptor': descriptors
                - 'pdbx_chem_comp_identifier': identifiers
                - 'pdbx_chem_comp_feature': features
                - 'pdbx_chem_comp_audit': audit info
                - 'rcsb_chem_comp_container_identifiers': container info
                - 'rcsb_chem_comp_related': related components
                - 'rcsb_chem_comp_synonyms': synonyms
                    
        Returns empty list if component not found or error occurs.
        
    Query example: {"component_id": "ATP"}
    """
    result = pdb_api.get_chemical_component(component_id)
    return result

# Group tools
@mcp.tool()
async def pdb_get_aggregation_group_provenance(group_id: str):
    """
    Retrieve provenance information for an aggregation group in PDB.
    
    Args:
        group_id (str): The aggregation group identifier (e.g. "1", "2")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of aggregation group provenance including:
                - 'rcsb_aggregation_group_provenance':
                    - 'group_id': group ID
                    - 'aggregation_method': method used
                    - 'aggregation_criteria': criteria details
                    - 'aggregation_version': version info
                    - 'aggregation_date': date of aggregation
                    - 'aggregation_software': software used
                    - 'aggregation_parameters': parameters used
                    - 'aggregation_references': reference info
                    - 'aggregation_notes': additional notes
                    
        Returns empty list if group not found or error occurs.
        
    Query example: {"group_id": "1"}
    """
    result = pdb_api.get_aggregation_group_provenance(group_id)
    return result

@mcp.tool()
async def pdb_get_pdb_cluster_data_aggregation(cluster_id: str):
    """
    Retrieve data aggregation information for a PDB cluster.
    
    Args:
        cluster_id (str): The cluster identifier (e.g. "1", "2")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of cluster data aggregation including:
                - 'rcsb_cluster_data_aggregation':
                    - 'cluster_id': cluster ID
                    - 'cluster_size': number of members
                    - 'cluster_method': clustering method
                    - 'cluster_cutoff': similarity cutoff
                    - 'cluster_members': list of member PDB IDs
                    - 'cluster_representative': representative PDB ID
                    - 'cluster_sequence_identity': average sequence identity
                    - 'cluster_rmsd': average structural RMSD
                    - 'cluster_coverage': sequence coverage
                    
        Returns empty list if cluster not found or error occurs.
        
    Query example: {"cluster_id": "1"}
    """
    result = pdb_api.get_pdb_cluster_data_aggregation(cluster_id)
    return result

@mcp.tool()
async def pdb_get_pdb_cluster_data_aggregation_method(method_id: str):
    """
    Retrieve details about a PDB cluster data aggregation method.
    
    Args:
        method_id (str): The method identifier (e.g. "sequence_identity", "structure_similarity")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of method details including:
                - 'rcsb_cluster_data_aggregation_method':
                    - 'id': method ID
                    - 'name': method name
                    - 'description': method description
                    - 'version': method version
                    - 'parameters': method parameters
                    - 'reference': reference info
                    - 'software': software used
                    - 'cutoff': similarity cutoff value
                    - 'coverage': sequence coverage value
                    
        Returns empty list if method not found or error occurs.
        
    Query example: {"method_id": "sequence_identity"}
    """
    result = pdb_api.get_pdb_cluster_data_aggregation_method(method_id)
    return result

# Residue tools
@mcp.tool()
async def pdb_get_residue_chains(entry_id: str):
    """
    Retrieve residue chain information for a PDB entry.
    
    Args:
        entry_id (str): The 4-character PDB entry ID (e.g. "1CRN", "1TUP")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string of residue chain information including:
                - 'rcsb_id': PDB ID
                - 'chains': list of chains with:
                    - 'asym_id': asymmetric unit ID
                    - 'auth_asym_id': author asymmetric unit ID
                    - 'entity_id': parent entity ID
                    - 'entity_type': entity type (polymer/branched/non-polymer)
                    - 'residues': list of residues with:
                        - 'residue_number': residue number
                        - 'residue_name': residue name
                        - 'chem_comp_id': chemical component ID
                        - 'pdbx_PDB_ins_code': insertion code
                        - 'pdbx_formal_charge': formal charge
                        - 'pdbx_polymer_type': polymer type
                    
        Returns empty list if no chains found or error occurs.
        
    Query example: {"entry_id": "1CRN"}
    """
    result = pdb_api.get_residue_chains(entry_id)
    return result

@mcp.tool()
async def pdb_get_entry_groups(group_id: str):
    """
    Retrieve detailed group information from RCSB PDB for a specified Group Deposition ID.
    
    Args:
        group_id (str): The PDB Group Deposition ID (e.g., "G_1002011")
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string containing:
                - rcsb_id: Group-level RCSB identifier
                - rcsb_group_container_identifiers: Group and member ID relationships
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info: Name, description, granularity, and member count
                - rcsb_group_statistics: Similarity score cutoff and score range
                - rcsb_group_accession_info: Version information
                - rcsb_group_related: Related group structures (if any)
                
        Returns empty list if group not found or error occurs.
        
    Query example: {"group_id": "G_1002011"}
    """
    result = pdb_api.get_entry_groups(group_id)
    return result

@mcp.tool()
async def pdb_get_polymer_entity_groups(group_id: str):
    """
    Retrieve a polymer entity group from RCSB PDB by UniProt ID or sequence cluster ID.
    
    Args:
        group_id (str): A UniProt ID (e.g., "Q3Y9I6") or RCSB sequence cluster ID
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string containing:
                - rcsb_id: Identifier for the entity group
                - rcsb_group_container_identifiers:
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info:
                    - group_name
                    - group_description
                    - group_members_granularity (e.g., assembly, chain)
                    - group_members_count
                - rcsb_group_statistics:
                    - similarity_cutoff
                    - similarity_score_min / max
                - rcsb_group_accession_info:
                    - version
                - rcsb_group_related: Related group entries
                - rcsb_polymer_entity_group_members_rankings: Ranking info
                - rcsb_polymer_entity_group_sequence_alignment:
                    - abstract_reference: Reference sequence info
                    - group_members_alignment: Aligned member sequences
                    
        Returns empty list if group not found or error occurs.
        
    Query example: {"group_id": "Q3Y9I6"}
    """
    result = pdb_api.get_polymer_entity_groups(group_id)
    return result

@mcp.tool()
async def pdb_get_nonpolymer_entity_groups(group_id: str):
    """
    Retrieve a non-polymer entity group object from RCSB PDB by Chemical Component ID.
    
    Args:
        group_id (str): The Chemical Component ID (e.g., "HEM" for heme group)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON string containing:
                - rcsb_id: Group-level identifier
                - rcsb_group_container_identifiers:
                    - group_id
                    - group_provenance_id
                    - parent_member_ids
                    - group_member_ids
                - rcsb_group_info:
                    - group_name
                    - group_description
                    - group_members_granularity
                    - group_members_count
                - rcsb_group_statistics:
                    - similarity_cutoff
                    - similarity_score_min / max
                - rcsb_group_accession_info:
                    - version
                - rcsb_group_related: Related groups (if any)
                - rcsb_polymer_entity_group_members_rankings: Ranking info
                - rcsb_polymer_entity_group_sequence_alignment:
                    - abstract_reference
                    - group_members_alignment
                    
        Returns empty list if group not found or error occurs.
        
    Query example: {"group_id": "HEM"}
    """
    result = pdb_api.get_nonpolymer_entity_groups(group_id)
    return result

@mcp.prompt()
def system_prompt():
    return """You are the Protein Data Bank (PDB) MCP server. 
    You can answer questions about protein structures and related data using the PDB API.
    Always include the result of tool calls in your final answer."""
