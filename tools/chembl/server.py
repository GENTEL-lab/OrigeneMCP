import json

from mcp.server.fastmcp import FastMCP
from tools.chembl.chembl_api import ChemblAPI

mcp = FastMCP(
    "chembl_mcp",
    stateless_http=True,
)
chembl_api = ChemblAPI()


@mcp.tool()
async def get_activity():
    """
    Retrieves a list of bioactivity data entries from the ChEMBL database. Note: This tool does not accept any filtering parameters and will return a default list of the first few activity entries from the entire database. To search for specific activities, use the 'search_activity' tool instead.
    
    Args:
    
    Query example: {}
    
    Returns:
        A list of activity objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_activity()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_activity: {str(e)}"}]
    return result


@mcp.tool()
async def get_activity_by_id(activity_id: int):
    """
    Retrieve the details of a single bioactivity entry from the ChEMBL database by its unique activity ID.
    
    Args:
        activity_id: The unique integer identifier for the ChEMBL activity entry.
    
    Query example: {"activity_id": 31863}
    
    Returns:
        A dictionary containing the detailed properties of the specified activity entry.
    """

    try:
        result = chembl_api.get_activity_by_id(activity_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_activity_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_activity_by_ids(activity_ids: list[int]):
    """
    Retrieves a list of bioactivity entries from the ChEMBL database. Note: This tool currently does not function as expected. It does not correctly filter by the provided list of IDs and instead returns a default list of activities from the database.
    
    Args:
        activity_ids: A list of unique integer identifiers for ChEMBL activity entries.
    
    Query example: {"activity_ids": [31863, 31864]}
    
    Returns:
        A default list of activity objects from the ChEMBL database, not limited to the provided IDs.
    """

    try:
        result = chembl_api.get_activity_by_ids(activity_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_activity_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_activity(query_str: str):
    """
    Performs a full-text search for bioactivity data in the ChEMBL database using a query string. This tool can search across various fields in the activity records, such as assay descriptions, target names, or molecule information.
    
    Args:
        query_str: The search string. This can be a keyword, a target name, a journal, or any other text expected to be found in the activity records.
    
    Query example: {"query_str": "cyclooxygenase"}
    
    Returns:
        A list of activity objects that match the search query.
    """

    try:
        result = chembl_api.search_activity(query_str)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying search_activity: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_activity_supplementary_data_by_activity():
    """
    Retrieves a default list of supplementary bioactivity data from the ChEMBL database. Note: This tool is flawed and does not accept any filtering parameters, ignoring any provided input. To retrieve data for a specific activity, use the 'get_activity_supplementary_data_by_activity_id' tool instead.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of supplementary activity data objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_activity_supplementary_data_by_activity()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_activity: {str(e)}"}]
    return result


@mcp.tool()
async def get_activity_supplementary_data_by_activity_by_id(activity_id: int):
    """
    Retrieve single activitysupplementarydatabyactivity object details by ID.
    :param activity_id: Unique ID for the activity (int)
    :return:
    """
    try:
        result = chembl_api.get_activity_supplementary_data_by_activity_by_id(
            activity_id
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_activity_supplementary_data_by_activity_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_activity_supplementary_data_by_activity_by_ids(activity_ids: list[int]):
    """
    Retrieve multiple activitysupplementarydatabyactivity objects by IDs.
    :param activity_ids: list of Unique ID for the activity
    :return:
    """
    try:
        result = chembl_api.get_activity_supplementary_data_by_activity_by_ids(
            activity_ids
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_activity_supplementary_data_by_activity_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_assay():
    """
    [WARNING] This tool is broken and does NOT retrieve assay data. It incorrectly calls the activity endpoint and returns a default list of bioactivity data instead. DO NOT USE. The 'search_assay' tool should be used to find assay information.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of bioactivity objects, NOT assay objects.
    """

    try:
        result = chembl_api.get_activity()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_activity: {str(e)}"}]
    return result


@mcp.tool()
async def get_assay_by_id(assay_chembl_id: str):
    """
    Retrieves the details for a single assay (experimental procedure) from the ChEMBL database using its unique ChEMBL ID.
    
    Args:
        assay_chembl_id: The unique ChEMBL identifier for the assay (e.g., 'CHEMBL663853'). This must be a string.
    
    Query example: {"assay_chembl_id": "CHEMBL663853"}
    
    Returns:
        A dictionary containing the detailed properties of the specified assay.
    """

    try:
        result = chembl_api.get_assay_by_id(assay_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_assay_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_assay_by_ids(assay_chembl_ids: list[str]):
    """
    Retrieves detailed information for multiple assays from the ChEMBL database using a list of their unique ChEMBL IDs.
    
    Args:
        assay_chembl_ids: A list of unique ChEMBL string identifiers for the assays (e.g., ['CHEMBL663853', 'CHEMBL872937']).
    
    Query example: {"assay_chembl_ids": ["CHEMBL663853", "CHEMBL872937"]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified assay.
    """

    try:
        result = chembl_api.get_assay_by_ids(assay_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_assay_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_assay(query_str: str):
    """
    Performs a full-text search for assays (experimental procedures) in the ChEMBL database using a query string. This can search across various fields like the assay description.
    
    Args:
        query_str: The search string, e.g., a protein name like 'Heparanase' or other keywords from the assay description.
    
    Query example: {"query_str": "Heparanase"}
    
    Returns:
        A list of assay objects that match the search query.
    """

    try:
        result = chembl_api.search_assay(query_str)
    except Exception as e:
        return [{"error": f"An error occurred while querying search_assay: {str(e)}"}]
    return result


@mcp.tool()
async def get_assay_class():
    """
    Retrieves a default list of assay classifications from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of assay classification objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_assay_class()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_assay_class: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_assay_class_by_id(assay_class_id: int):
    """
    Retrieves the details for a single assay classification from the ChEMBL database using its unique integer ID.
    
    Args:
        assay_class_id: The unique integer identifier for the assay classification.
    
    Query example: {"assay_class_id": 1}
    
    Returns:
        A dictionary containing the detailed properties of the specified assay classification.
    """

    try:
        result = chembl_api.get_assay_class_by_id(assay_class_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_assay_class_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_assay_class_by_ids(assay_class_ids: list[int]):
    """
    Retrieves detailed information for multiple assay classifications from the ChEMBL database using a list of their unique integer IDs.
    
    Args:
        assay_class_ids: A list of unique integer identifiers for the assay classifications.
    
    Query example: {"assay_class_ids": [1, 2]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified assay classification.
    """

    try:
        result = chembl_api.get_assay_class_by_ids(assay_class_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_assay_class_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_atc_class():
    """
    Retrieves a default list of ATC (Anatomical Therapeutic Chemical) classifications from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of ATC class objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_atc_class()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_atc_class: {str(e)}"}]
    return result


@mcp.tool()
async def get_atc_class_by_id(level5: str):
    """
    Retrieves the details for a single ATC (Anatomical Therapeutic Chemical) classification from the ChEMBL database. Note: This tool is named '_by_id' but it searches by the level 5 ATC code string, not a numerical ID.
    
    Args:
        level5: The level 5 ATC code string for the desired classification (e.g., 'A01AA01').
    
    Query example: {"level5": "A01AA01"}
    
    Returns:
        A dictionary containing the detailed properties of the specified ATC classification.
    """

    try:
        result = chembl_api.get_atc_class_by_id(level5)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_atc_class_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_atc_class_by_ids(level5s: list[str]):
    """
    Retrieves the details for multiple ATC (Anatomical Therapeutic Chemical) classifications from the ChEMBL database using a list of their level 5 ATC codes. Note: This tool is named '_by_ids' but it searches by a list of level 5 ATC code strings.
    
    Args:
        level5s: A list of level 5 ATC code strings for the desired classifications (e.g., ['A01AA01', 'A01AA02']).
    
    Query example: {"level5s": ["A01AA01", "A01AA02"]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified ATC classification.
    """

    try:
        result = chembl_api.get_atc_class_by_ids(level5s)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_atc_class_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_binding_site():
    """
    Retrieves a default list of binding sites from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of binding site objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_binding_site()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_binding_site: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_binding_site_by_id(site_id: int):
    """
    Retrieves the details for a single binding site from the ChEMBL database using its unique integer ID.
    
    Args:
        site_id: The unique integer identifier for the binding site.
    
    Query example: {"site_id": 2}
    
    Returns:
        A dictionary containing the detailed properties of the specified binding site.
    """

    try:
        result = chembl_api.get_binding_site_by_id(site_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_binding_site_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_binding_site_by_ids(site_ids: list):
    """
    Retrieves detailed information for multiple binding sites from the ChEMBL database using a list of their unique integer IDs. Note: The schema for this tool does not explicitly define the type of items in the list, but it expects integers.
    
    Args:
        site_ids: A list of unique integer identifiers for the binding sites.
    
    Query example: {"site_ids": [2, 3]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified binding site.
    """

    try:
        result = chembl_api.get_binding_site_by_ids(site_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_binding_site_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_biotherapeutic():
    """
    Retrieves a default list of biotherapeutics from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of biotherapeutic objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_biotherapeutic()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_biotherapeutic: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_biotherapeutic_by_id(molecule_chembl_id: str):
    """
    Retrieves the details for a single biotherapeutic from the ChEMBL database using its unique molecule ChEMBL ID.
    
    Args:
        molecule_chembl_id: The unique ChEMBL identifier (string) for the biotherapeutic.
    
    Query example: {"molecule_chembl_id": "CHEMBL448105"}
    
    Returns:
        A dictionary containing the detailed properties of the specified biotherapeutic.
    """

    try:
        result = chembl_api.get_biotherapeutic_by_id(molecule_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_biotherapeutic_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_biotherapeutic_by_ids(molecule_chembl_ids: list[str]):
    """
    Retrieves detailed information for multiple biotherapeutics from the ChEMBL database using a list of their unique molecule ChEMBL IDs.
    
    Args:
        molecule_chembl_ids: A list of unique ChEMBL identifier strings for the biotherapeutics.
    
    Query example: {"molecule_chembl_ids": ["CHEMBL448105", "CHEMBL266571"]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified biotherapeutic.
    """

    try:
        result = chembl_api.get_biotherapeutic_by_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_biotherapeutic_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_cell_line():
    """
    Retrieves a default list of cell lines from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of cell line objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_cell_line()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_cell_line: {str(e)}"}]
    return result


@mcp.tool()
async def get_cell_line_by_id(cell_id: int):
    """
    Retrieves the details for a single cell line from the ChEMBL database using its unique integer ID.
    
    Args:
        cell_id: The unique integer identifier for the cell line.
    
    Query example: {"cell_id": 1}
    
    Returns:
        A dictionary containing the detailed properties of the specified cell line.
    """

    try:
        result = chembl_api.get_cell_line_by_id(cell_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_cell_line_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_cell_line_by_ids(cell_ids: list[int]):
    """
    Retrieves detailed information for multiple cell lines from the ChEMBL database using a list of their unique integer IDs.
    
    Args:
        cell_ids: A list of unique integer identifiers for the cell lines.
    
    Query example: {"cell_ids": [1, 2]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified cell line.
    """

    try:
        result = chembl_api.get_cell_line_by_ids(cell_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_cell_line_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_id_lookup():
    """
    Retrieve chembl_id_lookup object list.
    
    Args:
    
    Query example: {"kwargs": {}}
    
    Returns:
        XML-formatted data containing ChEMBL ID lookup information,
    including identifier mappings and related attributes
    """

    try:
        result = chembl_api.get_chembl_id_lookup()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_id_lookup: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_id_lookup_by_id(chembl_id: str):
    """
    Fetches ChEMBL identifier mappings by a specified chembl_id, enabling reverse lookup of entity details (e.g., compound structures, target annotations) associated with a ChEMBL ID.
    
    Args:
        chembl_id: ChEMBL identifier (e.g., 'CHEMBL123') to query, formatted as a string (e.g., 'CHEMBL123')
    
    
    Query example: {"chembl_id": "CHEMBL145"}
    
    Returns:
        Returns a JSON object with detailed entity information mapped to the chembl_id.
    """

    try:
        result = chembl_api.get_chembl_id_lookup_by_id(chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_id_lookup_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_id_lookup_by_ids(chembl_ids: list[str]):
    """
    Retrieve multiple chembl_id_lookup objects by IDs.
    
    Args:
        chembl_ids: Array of ChEMBL IDs to query (e.g., ["CHEMBL145", "CHEMBL235"]). Each ID must follow the format CHEMBL[0-9]+
    
    
    Query example: {"chembl_ids": ["CHEMBL145", "CHEMBL235"]}
    
    Returns:
        Returns a JSON object with bulk query results.
    """

    try:
        result = chembl_api.get_chembl_id_lookup_by_ids(chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_id_lookup_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def search_chembl_id_lookup(query_str: str):
    """
    Search chemblidlookup using query string.
    
    Args:
        query_str: Search query string in Lucene syntax (e.g., 'compound:aspirin' or 'target_name:EGFR AND activity_value:<=10')
    
    
    Query example: {"query_str": "compound:aspirin OR target_name:cyclooxygenase"}
    
    Returns:
        Returns a paginated JSON response with search results.
    """

    try:
        result = chembl_api.search_chembl_id_lookup(query_str)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying search_chembl_id_lookup: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_release():
    """
    Retrieve chembl_release object list.
    
    Args:
    
    Returns:
        Returns a JSON object with release metadata.
    """

    try:
        result = chembl_api.get_chembl_release()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_chembl_release: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_chembl_release_by_id(chembl_release: str):
    """
    Retrieve single chembl_release object details by ID.
    
    Args:
        chembl_release: String representing the ChEMBL release version (e.g., "35"). Must be a valid release number (e.g., numeric string matching an existing release).
    
    
    Query example: {"chembl_release": "35"}
    
    Returns:
        Returns a JSON object with metadata for the specified release.
    """

    try:
        result = chembl_api.get_chembl_release_by_id(chembl_release)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_release_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_chembl_release_by_ids(chembl_releases: list[str]):
    """
    Retrieve multiple chembl_release objects by IDs.
    
    Args:
        chembl_releases: Array of ChEMBL release version strings (e.g., ["35", "34"]). Each version must be a valid numeric string matching an existing release (e.g., "35", "34").
    
    
    Query example: {"chembl_releases": ["35", "34"]}
    
    Returns:
        Returns a JSON object with an array of metadata for each specified release.
    """

    try:
        result = chembl_api.get_chembl_release_by_ids(chembl_releases)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_chembl_release_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_record():
    """
    Retrieve compound record object list.
    
    Args: 
    
    Query example: {"chembl_id": "CHEMBL145"}
    
    Returns:
        Returns a JSON object with comprehensive compound metadata.
    """

    try:
        result = chembl_api.get_compound_record()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_compound_record: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_compound_record_by_id(record_id: int):
    """
    Retrieve single compound_record object details by ID.
    
    Args:
        record_id: Integer representing the internal record ID of the compound in ChEMBL's database (e.g., 12345). This ID is distinct from the ChEMBL ID (e.g., CHEMBL145).
    
    
    Query example: {"record_id": 12345}
    
    Returns:
        Returns a JSON object with compound metadata, similar to get_compound_record, but linked via the internal record ID.
    """

    try:
        result = chembl_api.get_compound_record_by_id(record_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_record_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_record_by_ids(record_ids: list[int]):
    """
    Retrieve multiple compound_record objects by IDs.
    
    Args:
        record_ids: Array of integer values representing internal record IDs of compounds in ChEMBL (e.g., [12345, 67890]). Each ID must be a valid numeric record ID from the database.
    
    
    Query example: {"record_ids": [12345, 67890]}
    
    Returns:
        Returns a JSON object with an array of compound metadata for each valid record ID.
    """

    try:
        result = chembl_api.get_compound_record_by_ids(record_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_record_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_structural_alert():
    """
    Retrieve compound structural alert object list.
    
    Args:
    
    Query example: {"chembl_id": "CHEMBL145"}
    
    Returns:
        Returns a JSON object with structural alert metadata for the compound.
    """

    try:
        result = chembl_api.get_compound_structural_alert()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_structural_alert: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_structural_alert_by_id(cpd_str_alert_id: int):
    """
    Retrieve compound structural alert object details by ID.
    
    Args:
        cpd_str_alert_id: Integer representing the internal ID of the structural alert in ChEMBL's database (e.g., 123). This ID references a specific substructure annotation associated with compounds.
    
    
    Query example: {"cpd_str_alert_id": 123}
    
    Returns:
        Returns a JSON object with structural alert details.
    """

    try:
        result = chembl_api.get_compound_structural_alert_by_id(cpd_str_alert_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_structural_alert_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_compound_structural_alert_by_ids(cpd_str_alert_ids: list[int]):
    """
    Retrieve multiple compound structural alert objects by IDs.
    
    Args:
        cpd_str_alert_ids: Array of integer values representing internal IDs of structural alerts in ChEMBL (e.g., [123, 456]). Each ID references a specific substructure annotation linked to compounds.
    
    
    Query example: {"cpd_str_alert_ids": [1, 6]}
    
    Returns:
        Returns a JSON object with an array of structural alert details for each valid ID.
    """

    try:
        result = chembl_api.get_compound_structural_alert_by_ids(cpd_str_alert_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_compound_structural_alert_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_document():
    """
    Retrieve document object list.
    
    Args:
    
    Query example: {"document_chembl_id": "DOC123"}
    
    Returns:
        Returns a JSON object with comprehensive document metadata.
    """

    try:
        result = chembl_api.get_document()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_document: {str(e)}"}]
    return result


@mcp.tool()
async def get_document_by_id(document_chembl_id: str):
    """
    Retrieve single document object details by ID.
    
    Args:
        document_chembl_id: ChEMBL identifier of the document, formatted as a string (e.g., 'DOC123'). The ID follows the pattern DOC[0-9]+ (e.g., DOC100, DOC256).
    
    
    Query example: {"document_chembl_id": "DOC123"}
    
    Returns:
        Returns a JSON object with comprehensive document metadata.
    """

    try:
        result = chembl_api.get_document_by_id(document_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_document_by_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_document_by_ids(document_chembl_ids: list[str]):
    """
    Retrieve multiple document objects by IDs.
    
    Args:
        document_chembl_ids: Array of ChEMBL document identifiers (e.g., ['DOC123', 'DOC456']). Each ID must follow the format DOC[0-9]+ (e.g., DOC100, DOC256).
    
    
    Query example: {"document_chembl_ids": ["DOC123", "DOC456"]}
    
    Returns:
        Returns a JSON object with an array of document metadata for each valid ID
    """

    try:
        result = chembl_api.get_document_by_ids(document_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_document_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_document(query_str: str):
    """
    Search document by query string.
    
    Args:
        query_str: Search query string in Lucene syntax (e.g., 'aspirin AND 2020' or 'title:cyclooxygenase'). Supports field-specific searches (e.g., `author:Smith`, `year:2022`).
    
    
    Query example: {"query_str": "title:aspirin AND year:[2018 TO 2022]"}
    
    Returns:
        Returns a paginated JSON response with search results.
    """

    try:
        result = chembl_api.search_document(query_str)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying search_document: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_document_similarity():
    """
    Retrieve document similarity object list.
    
    Args:
    
    Query example: {"document_chembl_id": "DOC123"}
    
    Returns:
        Returns a JSON object with similar documents and similarity scores.
    """

    try:
        result = chembl_api.get_document_similarity()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_document_similarity: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_document_similarity_by_id(document_1_chembl_id: str):
    """
    Retrieve single document similarity object details by ID.
    
    Args:
        document_1_chembl_id: ChEMBL identifier of the reference document (e.g., 'DOC123'), used as the basis for similarity calculation.
    
    
    Query example: {"document_1_chembl_id": "DOC123"}
    
    Returns:
        Returns a JSON object with similarity results.
    """

    try:
        result = chembl_api.get_document_similarity_by_id(document_1_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_document_similarity_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_document_similarity_by_ids(document_1_chembl_ids: list[str]):
    """
    Retrieve multiple document similarity objects by IDs.
    
    Args:
        document_1_chembl_ids: Array of ChEMBL document identifiers (e.g., ['DOC123', 'DOC456']) to use as reference points for similarity calculation. Each ID must follow the format DOC[0-9]+
    
    
    Query example: {"document_1_chembl_ids": ["DOC123", "DOC456"]}
    
    Returns:
        Returns a JSON object with similarity results for each valid input ID.
    """

    try:
        result = chembl_api.get_document_similarity_by_ids(document_1_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_document_similarity_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_drug():
    """
    Retrieve drug object list.
    
    Args:
    
    Query example: {"drug_chembl_id": "DRUGB123"}
    
    Returns:
        Returns a JSON object with comprehensive drug metadata.
    """

    try:
        result = chembl_api.get_drug()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_drug: {str(e)}"}]
    return result


@mcp.tool()
async def get_drug_by_id(molecule_chembl_id):
    """
    Retrieve single drug object details by ID.
    
    Args:
        molecule_chembl_id: ChEMBL identifier of the drug, formatted as a string (e.g., 'CHEMBL145'). The ID follows the pattern CHEMBL[0-9]+ (e.g., CHEMBL100, CHEMBL256).
    
    
    Query example: {"molecule_chembl_id": "CHEMBL145"}
    
    Returns:
        Returns a JSON object with comprehensive drug metadata.
    """

    try:
        result = chembl_api.get_drug_by_id(molecule_chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_drug_by_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_drug_by_ids(molecule_chembl_ids: list[str]):
    """
    Retrieve multiple drus objects by IDs.
    
    Args:
        molecule_chembl_ids: Array of ChEMBL identifiers for drugs (e.g., ['CHEMBL145', 'CHEMBL235']). Each ID must follow the format CHEMBL[0-9]+ (e.g., CHEMBL100, CHEMBL256).
    
    
    Query example: {"molecule_chembl_ids": ["CHEMBL145", "CHEMBL235"]}
    
    Returns:
        Returns a JSON object with an array of drug metadata for each valid ID.
    """

    try:
        result = chembl_api.get_drug_by_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_by_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_indication():
    """
    Retrieve drug indication object list.
    
    Args: 
    
    Query example: {"molecule_chembl_id": "CHEMBL145"}
    
    Returns:
        Returns a JSON object with clinical indication data.
    """

    try:
        result = chembl_api.get_drug_indication()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_indication: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_indication_by_id(drugind_id: int):
    """
    Retrieve drug indication object details by ID
    
    Args:
        drugind_id: Integer representing the internal ID of the clinical indication in ChEMBL's database (e.g., 123). This ID references a specific therapeutic use annotation for drugs.
    
    
    Query example: {"drugind_id": 123}
    
    Returns:
        Returns a JSON object with comprehensive indication details.
    """

    try:
        result = chembl_api.get_drug_indication_by_id(drugind_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_drug_indication_by_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_drug_indication_by_ids(drugind_ids: list[int]):
    """
    Retrieve multiple drus objects by IDs.
    :param drugind_ids:list of primary key of drug indication object
    :return:
    """
    try:
        result = chembl_api.get_drug_indication_by_ids(drugind_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_drug_indication_by_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_drug_warning():
    """
    Retrieve drug_warning object list
    
    Args: 
    
    Query example: {"molecule_chembl_id": "CHEMBL145"}
    
    Returns:
        Returns a JSON object with comprehensive safety warning data.
    """

    try:
        result = chembl_api.get_drug_warning()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_warning: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_warning_id(warning_id: int):
    """
    Retrieve single drug_warning object details by ID
    
    Args:
        warning_id: Integer representing the internal ID of the safety warning in ChEMBL's database (e.g., 789). This ID references a specific safety annotation for drugs.
    
    
    Query example: {"warning_id": 145}
    
    Returns:
        Returns a JSON object with comprehensive warning details.
    """

    try:
        result = chembl_api.get_drug_warning_id(warning_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_drug_warning_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_drug_warning_ids(warning_ids: list[int]):
    """
    Retrieve multiple drug_warning objects by IDs.
    
    Args:
        warning_ids: Array of integer values representing internal IDs of safety warnings in ChEMBL (e.g., [789, 910]). Each ID references a specific safety annotation for drugs.
    
    
    Query example: {"warning_ids": [145, 910]}
    
    Returns:
        Returns a JSON object with an array of warning metadata for each valid ID.
    """

    try:
        result = chembl_api.get_drug_warning_ids(warning_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_drug_warning_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_go_slim():
    """
    Retrieves a default list of GO (Gene Ontology) slim classifications from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of GO slim objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_go_slim()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_go_slim: {str(e)}"}]
    return result


@mcp.tool()
async def get_go_slim_id(go_id: str):
    """
    Retrieves the details for a single GO (Gene Ontology) slim classification from the ChEMBL database using its unique GO ID. Note: The naming of this tool ('_id') is inconsistent with the '_by_id' convention used in other tool families.
    
    Args:
        go_id: The unique GO identifier string for the GO slim term (e.g., 'GO:0000003').
    
    Query example: {"go_id": "GO:0000003"}
    
    Returns:
        A dictionary containing the detailed properties of the specified GO slim classification.
    """

    try:
        result = chembl_api.get_go_slim_id(go_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_go_slim_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_go_slim_ids(go_ids: list[str]):
    """
    Retrieves the details for multiple GO (Gene Ontology) slim classifications from the ChEMBL database using a list of their unique GO IDs. Note: The naming of this tool ('_ids') is inconsistent with the '_by_ids' convention used in other tool families.
    
    Args:
        go_ids: A list of unique GO identifier strings for the GO slim terms (e.g., ['GO:0000003', 'GO:0000149']).
    
    Query example: {"go_ids": ["GO:0000003", "GO:0000149"]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified GO slim classification.
    """

    try:
        result = chembl_api.get_go_slim_ids(go_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_go_slim_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_mechanism():
    """
    Retrieves a default list of mechanisms of action from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of mechanism objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_mechanism()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_mechanism: {str(e)}"}]
    return result


@mcp.tool()
async def get_mechanism_id(mec_id: int):
    """
    Retrieves the details for a single drug mechanism of action from the ChEMBL database. Note: The naming of this tool ('_id') is inconsistent with the '_by_id' convention used in other tool families.
    
    Args:
        mec_id: The unique integer identifier for the drug mechanism of action.
    
    Query example: {"mec_id": 13}
    
    Returns:
        A dictionary containing the detailed properties of the specified mechanism.
    """

    try:
        result = chembl_api.get_mechanism_id(mec_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_mechanism_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_mechanism_ids(mec_ids: list[int]):
    """
    Retrieves detailed information for multiple drug mechanisms of action from the ChEMBL database using a list of their unique integer IDs. Note: The naming of this tool ('_ids') is inconsistent with the '_by_ids' convention used in other tool families.
    
    Args:
        mec_ids: A list of unique integer identifiers for the drug mechanisms of action.
    
    Query example: {"mec_ids": [13, 14]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified mechanism.
    """

    try:
        result = chembl_api.get_mechanism_ids(mec_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_mechanism_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_metabolism():
    """
    Retrieves a default list of metabolism records from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of metabolism objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_metabolism()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_metabolism: {str(e)}"}]
    return result


@mcp.tool()
async def get_metabolism_id(met_id: int):
    """
    Retrieve single metabolism object details by ID.
    :param met_id:Primary key of metabolism
    :return:
    """
    try:
        result = chembl_api.get_metabolism_id(met_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_metabolism_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_metabolism_ids(met_ids: list[int]):
    """
    Retrieves detailed information for multiple drug metabolism records from the ChEMBL database using a list of their unique integer IDs. Note: The naming of this tool ('_ids') is inconsistent with the '_by_ids' convention used in other tool families.
    
    Args:
        met_ids: A list of unique integer identifiers for the drug metabolism records.
    
    Query example: {"met_ids": [119, 120]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified metabolism record.
    """

    try:
        result = chembl_api.get_metabolism_ids(met_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_metabolism_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule():
    """
    Retrieves a default list of molecules from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input. To find specific molecules, use the 'search_molecule' tool.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of molecule objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_molecule()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_molecule: {str(e)}"}]
    return result


@mcp.tool()
async def get_molecule_id(molecule_chembl_id: str):
    """
    Retrieves the details for a single molecule from the ChEMBL database using its unique molecule ChEMBL ID. Note: The naming of this tool ('_id') is inconsistent with the '_by_id' convention used in other tool families.
    
    Args:
        molecule_chembl_id: The unique ChEMBL identifier (string) for the molecule.
    
    Query example: {"molecule_chembl_id": "CHEMBL6329"}
    
    Returns:
        A dictionary containing the detailed properties of the specified molecule.
    """

    try:
        result = chembl_api.get_molecule_id(molecule_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_molecule_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule_ids(molecule_chembl_ids: list[str]):
    """
    Retrieves detailed information for multiple molecules from the ChEMBL database using a list of their unique molecule ChEMBL IDs. Note: The naming of this tool ('_ids') is inconsistent with the '_by_ids' convention used in other tool families.
    
    Args:
        molecule_chembl_ids: A list of unique ChEMBL identifier strings for the molecules.
    
    Query example: {"molecule_chembl_ids": ["CHEMBL6329", "CHEMBL19"]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified molecule.
    """

    try:
        result = chembl_api.get_molecule_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_molecule_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def search_molecule(query_str: str):
    """
    Performs a full-text search for molecules in the ChEMBL database using a query string. This can search across various fields like the preferred name, synonyms, or other molecule properties.
    
    Args:
        query_str: The search string, e.g., a molecule name like 'METHAZOLAMIDE'.
    
    Query example: {"query_str": "METHAZOLAMIDE"}
    
    Returns:
        A list of molecule objects that match the search query.
    """

    try:
        result = chembl_api.search_molecule(query_str)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying search_molecule: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule_form():
    """
    Retrieves a default list of molecule forms from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of molecule form objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_molecule_form()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_molecule_form: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_molecule_form_id(molecule_chembl_id: str):
    """
    Retrieves molecule form information for a given molecule from the ChEMBL database using its unique molecule ChEMBL ID. Note: The naming of this tool ('_id') is inconsistent with the '_by_id' convention used in other tool families.
    
    Args:
        molecule_chembl_id: The unique ChEMBL identifier (string) for the molecule.
    
    Query example: {"molecule_chembl_id": "CHEMBL6329"}
    
    Returns:
        A list containing a dictionary with the molecule form details.
    """

    try:
        result = chembl_api.get_molecule_form_id(molecule_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_molecule_form_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_molecule_form_ids(molecule_chembl_ids: list[str]):
    """
    Retrieves molecule form information for multiple molecules from the ChEMBL database using a list of their unique molecule ChEMBL IDs. Note: The naming of this tool ('_ids') is inconsistent with the '_by_ids' convention used in other tool families.
    
    Args:
        molecule_chembl_ids: A list of unique ChEMBL identifier strings for the molecules.
    
    Query example: {"molecule_chembl_ids": ["CHEMBL6329", "CHEMBL6328"]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the molecule form details for a given input ID.
    """

    try:
        result = chembl_api.get_molecule_form_ids(molecule_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_molecule_form_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_organism():
    """
    Retrieves a default list of organisms from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of organism objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_organism()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_organism: {str(e)}"}]
    return result


@mcp.tool()
async def get_organism_id(oc_id: int):
    """
    Retrieves the details for a single organism from the ChEMBL database using its unique integer ID. Note: The naming of this tool ('_id') is inconsistent with the '_by_id' convention used in other tool families.
    
    Args:
        oc_id: The unique integer identifier for the organism.
    
    Query example: {"oc_id": 1}
    
    Returns:
        A dictionary containing the detailed properties of the specified organism.
    """

    try:
        result = chembl_api.get_organism_id(oc_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_organism_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_organism_ids(oc_ids: list[int]):
    """
    Retrieves detailed information for multiple organisms from the ChEMBL database using a list of their unique integer IDs. Note: The naming of this tool ('_ids') is inconsistent with the '_by_ids' convention used in other tool families.
    
    Args:
        oc_ids: A list of unique integer identifiers for the organisms.
    
    Query example: {"oc_ids": [1, 2]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified organism.
    """

    try:
        result = chembl_api.get_organism_ids(oc_ids)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_organism_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_protein_classification():
    """
    Retrieves a default list of protein classifications from the ChEMBL database. Note: This tool is flawed as it does not accept any filtering parameters and ignores any provided input.
    
    Args:
    
    Query example: {}
    
    Returns:
        A default list of protein classification objects from the ChEMBL database.
    """

    try:
        result = chembl_api.get_protein_classification()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_protein_classification: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_protein_classification_id(protein_class_id: int):
    """
    Retrieves the details for a single protein classification from the ChEMBL database using its unique integer ID. Note: The naming of this tool ('_id') is inconsistent with the '_by_id' convention used in other tool families.
    
    Args:
        protein_class_id: The unique integer identifier for the protein classification.
    
    Query example: {"protein_class_id": 1}
    
    Returns:
        A dictionary containing the detailed properties of the specified protein classification.
    """

    try:
        result = chembl_api.get_protein_classification_id(protein_class_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_protein_classification_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_protein_classification_ids(protein_class_ids: list[int]):
    """
    Retrieves detailed information for multiple protein classifications from the ChEMBL database using a list of their unique integer IDs. Note: The naming of this tool ('_ids') is inconsistent with the '_by_ids' convention used in other tool families.
    
    Args:
        protein_class_ids: A list of unique integer identifiers for the protein classifications.
    
    Query example: {"protein_class_ids": [0, 1]}
    
    Returns:
        A list of dictionaries, where each dictionary contains the detailed properties of a specified protein classification.
    """

    try:
        result = chembl_api.get_protein_classification_ids(protein_class_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_protein_classification_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def search_protein_classification(query_str: str):
    """
    Search protein_classification object by query string.
    
    Args:
        query_str: a value of query string data of protein_classification (e.g. definition)
        type: string
    
    Query example: {"query_str": "kinase"}
    
    Returns:
        List of dictionaries, each with classification details including protein_class_id, pref_name and hierarchical levels.
    """

    try:
        result = chembl_api.search_protein_classification(query_str)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying search_protein_classification: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_similarity_smiles(standard_inchi_key: str, similarity: int):
    """
    Retrieve single similarity object details by ID.
    
    Args:
        standard_inchi_key: IUPAC standard InChI key for the compound
        similarity: Fixed precision numeric data specifying similarity threshold
        type_of_standard_inchi_key: string
        type_of_similarity: integer
    
    Query example: {"standard_inchi_key": "CCO", "similarity": 85}
    
    Returns:
        List of compounds with similarity score and metadata
    """

    try:
        result = chembl_api.get_similarity_smiles(standard_inchi_key, similarity)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_similarity_smiles: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_source():
    """
    Retrieve source object list.
    
    Args:
    
    Returns:
        List of dictionaries with src_id, src_description, src_short_name etc.
    """

    try:
        result = chembl_api.get_source()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_source: {str(e)}"}]
    return result


@mcp.tool()
async def get_source_id(src_id: int):
    """
    Retrieve single source object details by ID.
    
    Args:
        src_id: Identifier for each source (used in compound_records and assays tables)
        type: integer
    
    Query example: {"src_id": 1}
    
    Returns:
        A dictionary containing src_id, src_description, etc.
    """

    try:
        result = chembl_api.get_source_id(src_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_source_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_source_ids(src_ids: list[int]):
    """
    Retrieve multiple source object details by IDs.
    
    Args:
        src_ids: list of src identifier for source
        type: array
    
    Query example: {"src_ids": [1, 2, 3]}
    
    Returns:
        List of source dictionaries including src_short_name, src_comment, src_description
    """

    try:
        result = chembl_api.get_source_ids(src_ids)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_source_ids: {str(e)}"}]
    return result


@mcp.tool()
async def get_status():
    """
    Retrieve status object list.
    
    Args:
    
    Returns:
        List of status dictionaries including activities, chembl_db_version, chembl_release_date, compound_records,  disinct_compounds, publications, status and targets
    """

    try:
        result = chembl_api.get_status()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_status: {str(e)}"}]
    return result


@mcp.tool()
async def substructure_info(molecule_chembl_id: str):
    """
    Retrieve single substructure object details by ID.
    
    Args:
        molecule_chembl_id: SMILES string data of substructure
        type: string
    
    Query example: {"molecule_chembl_id": "c1ccccc1"}
    
    Returns:
        List of compound matches, each with molecule_chembl_id, pref_name, max_phase, molecule_type, first_approval, black_box_warning etc.
    """

    try:
        result = chembl_api.substructure_info(molecule_chembl_id)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying substructure_info: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_target():
    """
    Retrieve target object list.
    
    Args:
    
    Returns:
        List of dictionaries with target_chembl_id, pref_name, organism, target_type, protein_classifications, target_components etc.
    """

    try:
        result = chembl_api.get_target()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_target: {str(e)}"}]
    return result


@mcp.tool()
async def get_target_id(target_chembl_id: str):
    """
    Retrieve single target object details by ID.
    
    Args:
        target_chembl_id: Target Chembl Id
        type: string
    
    Query example: {"target_chembl_id": "CHEMBL203"}
    
    Returns:
        Dictionary with target_chembl_id, pref_name, organism, target_type, target_components containing protein/accession info, protein_classifications
    """

    try:
        result = chembl_api.get_target_id(target_chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_target_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_target_ids(target_chembl_ids: list[str]):
    """
    Retrieve multiple target objects by IDs
    
    Args:
        target_chembl_ids: list of target_chembl_ids
        type: array
    
    Query example: {"target_chembl_ids": ["CHEMBL203", "CHEMBL240", "CHEMBL210"]}
    
    Returns:
        List of dictionaries with target_chembl_id, pref_name, organism, target_type, target_components containing protein/accession info, protein_classifications
    """

    try:
        result = chembl_api.get_target_ids(target_chembl_ids)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_target_ids: {str(e)}"}]
    return result


@mcp.tool()
async def search_target(query_str: str):
    """
    Search target using query string.
    
    Args:
        query_str: a value of string data of target (e.g. pref_name)
        type: string
    
    Query example: {"query_str": "kinase"}
    
    Returns:
        List of matching targets, each with target_chembl_id, pref_name, organism, target_type, protein_classifications, target_components
    """

    try:
        result = chembl_api.search_target(query_str)
    except Exception as e:
        return [{"error": f"An error occurred while querying search_target: {str(e)}"}]
    return result


@mcp.tool()
async def get_target_component():
    """
    Retrieve target_component object list
    
    Args:
    
    Returns:
        A list of dictionaries, each describing a target component (usually a protein or other biomolecule), including fields such as component_chembl_id, UniProt accession ID, component_type, species name, list of protein family classifications, structural or descriptive annotations
    """

    try:
        result = chembl_api.get_target_component()
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_component: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_component_id(component_id: int):
    """
    Retrieve single target_component object details by ID.
    
    Args:
        component_id: The ChEMBL component ID
        type: integer
    
    Query example: {"component_id": "135"}
    
    Returns:
        A dictionary containing detailed information about the specified target component, including: component_chembl_id: The unique component ID, the UniProt accession, the species name, component_type,  additional metadata such as sequence, tax ID, or cross-references
    """

    try:
        result = chembl_api.get_target_component_id(component_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_component_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_component_ids(component_ids: list[int]):
    """
    Retrieve multiple target_component object details by IDs.
    
    Args:
        component_ids: A list of unique identifiers for the component
        type: array
    
    Query example: {"component_ids": [135, 136, 137]}
    
    Returns:
        A list of dictionaries containing detailed information about the specified target component, including: component_chembl_id: The unique component ID, the UniProt accession, the species name, component_type,  additional metadata such as sequence, tax ID, or cross-references
    """

    try:
        result = chembl_api.get_target_component_ids(component_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_component_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_relation():
    """
    Retrieve target relation object list.
    
    Args:
    
    Returns:
        A list of dictionaries, each describing a target-to-target relationship, including information such as source and target ChEMBL IDs, relationship type and confidence level if available.
    """

    try:
        result = chembl_api.get_target_relation()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_target_relation: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_target_relation_id(related_target_chembl_id: str):
    """
    Retrieve single target_relation object details by ID
    
    Args:
        related_target_chembl_id: Related Target Chembl Id
        type: string
    
    Query example: {"related_target_chembl_id": "CHEMBL2096619"}
    
    Returns:
        A dictionary containing information about the target relation, including source and target ChEMBL IDs, the type of relationship and any related annotations.
    """

    try:
        result = chembl_api.get_target_relation_id(related_target_chembl_id)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_relation_id: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_target_relation_ids(related_target_chembl_ids: list[str]):
    """
    Retrieve multiple target_relation objects by IDs
    
    Args:
        related_target_chembl_ids: list of related target chembl Ids
        type: array
    
    Query example: {"related_target_chembl_ids": ["CHEMBL_TC_5607"]}
    
    Returns:
        A list of dictionaries, each describing a target-to-target relationship. Each dictionary includes the unique ID of the target relation ,the ChEMBL ID of the source target, the ChEMBL ID of the related (child) target, the type of relationship, additional metadata such as confidence_score, target_relation_type if available
    """

    try:
        result = chembl_api.get_target_relation_ids(related_target_chembl_ids)
    except Exception as e:
        return [
            {
                "error": f"An error occurred while querying get_target_relation_ids: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_tissue():
    """
    Retrieve tissue object list
    
    Args:
    
    Returns:
        A list of dictionaries, each containing information about a tissue, such as its ChEMBL ID, name, Uberon ID, and additional annotations.
    """

    try:
        result = chembl_api.get_tissue()
    except Exception as e:
        return [{"error": f"An error occurred while querying get_tissue: {str(e)}"}]
    return result


@mcp.tool()
async def get_tissue_id(tissue_chembl_id: str):
    """
    Retrieve single tissue object details by ID.
    
    Args:
        tissue_chembl_id: Unicode string data, such as tissue_chembl_id(string)
    
    Query example: {"tissue_chembl_id": "CHEMBL3559723"}
    
    Returns:
        Dictionary containing information about the tissue, such as its pref_name, associated Uberon ID, bto_id, caloha_id, efo_id.
    """

    try:
        result = chembl_api.get_tissue_id(tissue_chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_tissue_id: {str(e)}"}]
    return result


@mcp.tool()
async def get_tissue_ids(tissue_chembl_ids: list[str]):
    """
    Retrieve single tissue object details by IDs.
    
    Args:
        tissue_chembl_ids: list of unicode string data(Tissue Chembl Ids)
        type: array
    
    Query example: {"tissue_chembl_ids": ["CHEMBL3559723", "CHEMBL3307558", "CHEMBL3307556"]}
    """

    try:
        result = chembl_api.get_tissue_ids(tissue_chembl_ids)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_tissue_ids: {str(e)}"}]
    return result


@mcp.tool()
async def get_xref_source():
    """
    Retrieve xref_source object list
    
    Args:
    
    Returns:
        A list of dictionaries, each containing information about a cross-reference source, such as its name, description, URL, and ID prefix.
    """

    try:
        result = chembl_api.get_xref_source()
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_xref_source: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_xref_source_id(xref_src_db: str):
    """
    Retrieve single xref_source object details by ID.
    
    Args:
        xref_src_db: Name of the source database that is cross-referenced from chembl
        type: string
    
    Query example: {"xref_src_db": "UniProt"}
    
    Returns:
        Dictionary containing details about the xref source, such as name, description, URL, and ID prefix.
    """

    try:
        result = chembl_api.get_xref_source_id(xref_src_db)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_xref_source_id: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_xref_source_ids(xref_src_dbs: list[str]):
    """
    Retrieve multiple xref_source objects by IDs
    
    Args:
        xref_src_dbs: list of Name of the source database that is cross-referenced from chembl(array)
    
    Query example: {"xref_src_dbs": ["PDB", "UniProt"]}
    
    Returns:
        A list of dictionaries, each containing details about one xref source, such as name, description, URL, and ID prefix.
    """

    try:
        result = chembl_api.get_xref_source_ids(xref_src_dbs)
    except Exception as e:
        return [
            {"error": f"An error occurred while querying get_xref_source_ids: {str(e)}"}
        ]
    return result


@mcp.tool()
async def get_image(chembl_id: str):
    """
    Get image of the compound, specified by ChEMBL ID or Standard InChI Key
    You can specify optional parameters:
    engine - chemistry toolkit used for rendering, can be rdkit only, default: rdkit.
    dimensions - size of the image (the length of the square image side). Can't be more than 500, default: 500.
    ignoreCoords - Ignore 2D coordinates encoded in the molfile and let the chemistry toolkit to recompute them.
    
    Args:
        chembl_id: Chembl Id or Standard InChI Key
        type_of_chembl_id: string
        smiles(optional): valid SMILES
        type_of_smiles(optional): string
        engine(optional): chemistry toolkit used for rendering, can be rdkit only, default: rdkit.
        dimensions(optional): size of the image (the length of the square image side). Can't be more than 500, default: 500.
        ignoreCoords(optional): Ignore 2D coordinates encoded in the molfile and let the chemistry toolkit to recompute them.
    
    Query example: {"chembl_id": "CHEMBL25"}
    
    Returns:
        Returns an image file (typically PNG format) representing the compound's 2D chemical structure.
    """

    try:
        result = chembl_api.get_image(chembl_id)
    except Exception as e:
        return [{"error": f"An error occurred while querying get_image: {str(e)}"}]
    return result


@mcp.tool()
async def get_compound_chembl_id_by_name(name: str):
    """
    Get compound ChEMBL ID by name.
    
    Args:
        name: The compound name to search for
        
    Query example: {"name": "aspirin"}
    
    Returns:
        The ChEMBL ID of the compound if found, otherwise "No compound found"
    """
    try:
        result = chembl_api.search_molecule(name)
        if isinstance(result, str):
            result = json.loads(result)
        chembl_id = result['molecules'][0]['molecule_chembl_id']
    except Exception as e:
        print(e)
        chembl_id = 'No compound found'
    return chembl_id


@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    prompt = """You have access to tools for searching CHEMBL: ChEMBL Data Web Services.
    Use the API tools to extract the relevant information.
    Fill in missing arguments with sensible values if the user hasn't provided them. """
    return prompt


