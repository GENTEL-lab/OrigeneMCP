
from mcp.server.fastmcp import FastMCP

from tools.kegg.kegg_api import KeggAPI

mcp = FastMCP(
    "kegg_mcp",
    stateless_http=True,
)
kegg_api = KeggAPI()


@mcp.tool()
async def kegg_info(db: str):
    """
    
    This operation displays the database release information with statistics for the databases.
    Except for kegg, genes and ligand, this operation also displays the list of linked databases that can be used in the link operation.
    Displays the current statistics of a given database.

    Args:
        db: kegg database (string)

    Query example: {"db": "genes"}

    Returns:
        text message
    """
    try:
        result = kegg_api.kegg_info(database=db)
    except Exception as e:
        return [{"error": f"An error occurred while querying kegg_info: {str(e)}"}]
    return result


@mcp.tool()
async def kegg_find(db: str, query: str, option: str = ''):
    """
    
    KEGG find - Data search. Finds entries with matching query keywords or other query data in a given database.

    Args:
        db: KEGG database (string)
        query: Keywords or identifiers to search (string)
        option: Additional Search Options (string)

    Query example: {"db": "genes", "query": "p53", "option": ""}
    
    Returns:
        tab-delimited text
    """
    try:
        result = kegg_api.kegg_find(database=db, query=query, option=option)
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_find: {str(e)}"}
    return result


@mcp.tool()
async def kegg_list(db: str, org: str = ''):
    """
    
    This operation can be used to obtain a list of all entries in each database.When the organism code is known, the second form can be used to obtain a list of organism-specific pathways.The third form is a similar option for brite hierarchies.The fourth form may be used to obtain a list of definitions for a given set of database entry identifiers. The maximum number of identifiers that can be given is 10.

    Args:
        db: kegg database (string)
        org: Optional parameter to specify an organism prefix.Valid only if the db is of certain types (string)

    Query example: {"db": "pathway", "org": ""}

    Returns:
        tab-delimited text
    """
    try:
        result = kegg_api.kegg_list(database=db, org=org)
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_list: {str(e)}"}
    return result


@mcp.tool()
async def kegg_get(dbentries: str, option: str):
    """
    
    This operation retrieves given database entries in a flat file format or in other formats with options. Flat file formats are available for all KEGG databases except brite. The input is limited up to 10 entries.

    Args:
        dbentries: Specify the KEGG entry identifier or list to be queried.Multiple entries separated by +(string)
        option:  Controls the format or content of returned data(string)

    Query example: {"dbentries": "path:hsa00010", "option": "kgml"}

    Returns:
        flat file database format
    """
    try:
        result = kegg_api.kegg_get(dbentries=dbentries, option=option)
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_get: {str(e)}"}
    return result


@mcp.tool()
async def kegg_conv(target_db: str, source_db_or_dbentries: str, option: str):
    """
    
    This operation can be used to convert entry identifiers (accession numbers) of outside databases to KEGG identifiers, and vice versa. The first form allows database to database mapping, while the second form allows conversion of a selected number of entries. The database name "genes" may be used only in the second form.

    Args:
        target_db: Target Db (string)
        source_db_or_dbentries: Source Db Or Dbentries (string)
        option: Option (string)

    Query example: {"target_db": "ncbi-geneid", "source_db_or_dbentries": "hsa:10458", "option": ""}

    Returns:
        tab-delimited text
    """
    try:
        result = kegg_api.kegg_conv(
            target_db=target_db, source_db=source_db_or_dbentries, option=option
        )
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_conv: {str(e)}"}
    return result


@mcp.tool()
async def kegg_link(target_db: str, source_db_or_dbentries: str, option: str):
    """
    
    KEGG link - find related entries by using database cross-references.

    Args:
        target_db: Specify the name of the target database to map to (string)
        source_db_or_dbentries: Database name or Specific entry identifier (string)
        option: Control the format or range of the returned results(string)

    Query example: {"target_db": "pathway", "source_db_or_dbentries": "hsa:10458", "option": ""}

    Returns:
        tab-delimited text
    """
    try:
        result = kegg_api.kegg_link(
            target_db=target_db, source_db=source_db_or_dbentries, option=option
        )
    except Exception as e:
        return {"error": f"An error occurred while querying kegg_link: {str(e)}"}
    return result


@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    prompt = """You have access to tools for searching KEGG, a database resource for understanding high-level functions and utilities of the biological system, such as the cell, the organism and the ecosystem, from molecular-level information, especially large-scale molecular datasets generated by genome sequencing and other high-throughput experimental technologies.
    Use the API tools to extract the relevant information.
    Fill in missing arguments with sensible values if the user hasn't provided them. """
    return prompt


if __name__ == "__main__":
    # Initialize and run the server
    # mcp.run(transport='sse')
    mcp.run(transport="stdio")
