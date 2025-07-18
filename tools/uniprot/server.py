from mcp.server.fastmcp import FastMCP

from tools.uniprot.uniprot_api import UNIPROTAPI


mcp = FastMCP(
    "uniprot_mcp", 
    stateless_http=True
)
uniprot_api = UNIPROTAPI()


@mcp.tool()
async def get_general_info_by_protein_or_gene_name(query: str, sepcies: str = 'Homo sapiens'):
    """
    Get general information of a protein or gene by name from UniProt database.
    
    Args:
        name: Protein or gene name.
        sepcies: Species name.
    
    Query example: {"query": "TP53"}
        
    Returns:
        JSON string with general information of the protein or gene.
    """
    try:
        result = uniprot_api.get_general_info_by_protein_or_gene_name(query=query, species=sepcies)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result
    

@mcp.tool()
async def get_uniprotkb_entry_by_accession(accession: str):
    """
    Search UniProtKB by protein entry accession to return all data associated with that entry.
    
    Args:
        accession: UniProtKB accession ID (string, required)
    
    Query example: {"accession": "P68871"}
    
    Returns:
        A JSON string containing all data associated with the specified UniProtKB entry, including entry type, primary and secondary accession IDs, UniProtKB ID, annotation score, organism details, protein description, gene names, functional comments, and additional annotations such as sequence and database cross-references.
    """

    try:
        result = uniprot_api.get_uniprotkb_entry_by_accession(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniprotkb_entries(query: str):
    """
    Stream all UniProtKB entries associated with the search term in a single download.
    
    Args:
        query: Search term for UniProtKB entries, such as a protein name or keyword (e.g., "hemoglobin") (string, required)
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        A JSON string containing a list of UniProtKB entries matching the search query. Each entry includes the entry type, primary and secondary accession IDs, UniProtKB ID, entry audit information, annotation score, organism details, protein description (recommended name, alternative names, and contained molecules), gene names, functional comments, and additional annotations such as sequence and features.
    """

    try:
        result = uniprot_api.stream_uniprotkb_entries(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_uniprotkb_entries(query: str):
    """
    Search UniProtKB entries using a query, returns paginated list.
    
    Args:
        query: Search term for UniProtKB entries, such as a protein name or keyword (e.g., "hemoglobin") (string, required)
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        A JSON string containing a paginated list of UniProtKB entries matching the search query. Each entry includes the entry type, primary accession ID, UniProtKB ID, organism details, protein description (recommended name, alternative names, and contained molecules), gene names, functional comments, and additional features such as tissue specificity.
    """

    try:
        result = uniprot_api.search_uniprotkb_entries(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniref_cluster_by_id(uniref_id: str):
    """
    Search UniRef entry by id to return all data associated with that entry.
    
    Args:
        uniref_id: UniRef cluster ID (string, required)
    
    Query example: {"uniref_id": "UniRef90_P68871"}
    
    Returns:
        A JSON string containing all data associated with the specified UniRef cluster, including cluster ID, name, member count, update date, entry type, common taxonomy, representative member (with sequence and UniProtKB accessions), and a list of cluster members with their respective organism and sequence details.
    """

    try:
        result = uniprot_api.get_uniref_cluster_by_id(uniref_id=uniref_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniref_cluster_members_by_id(uniref_id: str):
    """
    Search UniRef entry by member id to return all data associated with that entry.
    
    Args:
        uniref_id: UniRef cluster ID (string, required)
    
    Query example: {"uniref_id": "UniRef90_P68871"}
    
    Returns:
        A JSON string containing a list of members in the specified UniRef cluster. Each member includes the member ID type, member ID, organism name and taxonomic ID, sequence length, protein name, UniProtKB accessions, related UniRef50/100 and UniParc IDs, and sequence details (value, length, molecular weight, CRC64 checksum, MD5 hash).
    """

    try:
        result = uniprot_api.get_uniref_cluster_members_by_id(uniref_id=uniref_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniref_light_cluster_by_id(uniref_id: str):
    """
    Search light UniRef entry by id to return all data associated with that entry.
    
    Args:
        uniref_id: UniRef cluster ID (string, required)
    
    Query example: {"uniref_id": "UniRef90_P68871"}
    
    Returns:
        A JSON string containing lightweight data for the specified UniRef cluster, including cluster ID, name, update date, entry type, common taxonomy, member and organism counts, representative member details (with sequence and UniProtKB accessions), seed ID, member ID types, a list of member IDs, and partial organism information.
    """

    try:
        result = uniprot_api.get_uniref_light_cluster_by_id(uniref_id=uniref_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniref_clusters(query: str):
    """
    Stream all UniRef clusters associated with the search term in a single download.
    
    Args:
        query: Search term for UniRef clusters, such as a protein name or keyword (e.g., "hemoglobin") (string, required)
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        A JSON string containing a list of UniRef clusters matching the search query. Each cluster includes the cluster ID, name, update date, entry type, common taxonomy, member and organism counts, representative member details (with sequence and UniProtKB accessions), seed ID, member ID types, member IDs, and organism details.
    """

    try:
        result = uniprot_api.stream_uniref_clusters(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_uniref_clusters(query: str):
    """
    Search UniRef clusters using a query, returns paginated list.
    
    Args:
        query: Search term for UniRef clusters, such as a protein name or keyword (e.g., "hemoglobin") (string, required)
    
    Query example: {"query": "hemoglobin"}
    
    Returns:
        A JSON string containing a paginated list of UniRef clusters matching the search query. Each cluster includes the cluster ID, name, update date, entry type, common taxonomy, member and organism counts, representative member details (with sequence and UniProtKB accessions), seed ID, member ID types, member IDs, and organism details.
    """

    try:
        result = uniprot_api.search_uniref_clusters(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniparc_entry_by_upi(uniparc_id: str):
    """
    Search UniParc entry by id (UPI) to return all data associated with that entry.
    
    Args:
        uniparc_id: UniParc UPI ID (string, required)
    
    Query example: {"uniparc_id": "UPI00000015C9"}
    
    Returns:
        A JSON string containing all data associated with the specified UniParc entry, including the UniParc ID, protein sequence (value, length, molecular weight, CRC64 checksum, MD5 hash), and sequence features from databases like Pfam, PROSITE, and InterPro.
    """

    try:
        result = uniprot_api.get_uniparc_entry_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniparc_light_entry_by_upi(uniparc_id: str):
    """
    Search UniParc entry by id (UPI) to return all data associated with that entry (light version).
    
    Args:
        uniparc_id: UniParc UPI ID (string, required)
    
    Query example: {"uniparc_id": "UPI00000015C9"}
    
    Returns:
        A JSON string containing lightweight data for the specified UniParc entry, including the UniParc ID, protein sequence (value, length, molecular weight, CRC64 checksum, MD5 hash), cross-reference count, common taxons, UniProtKB accessions, and sequence features from databases like Pfam, PROSITE, and InterPro.
    """

    try:
        result = uniprot_api.get_uniparc_light_entry_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_uniparc_cross_references_by_upi(uniparc_id: str):
    """
    Get a page of database cross-reference entries by a UPI.
    
    Args:
        uniparc_id: UniParc UPI ID (string, required)
    
    Query example: {"uniparc_id": "UPI000035B535"}
    
    Returns:
        A JSON string containing a paginated list of database cross-reference entries for the specified UniParc UPI, including database types, accession IDs, activity status, and associated properties like protein names and taxonomy.
    """

    try:
        result = uniprot_api.get_uniparc_cross_references_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniparc_cross_references_by_upi(uniparc_id: str):
    """
    Stream database cross-reference entries for a specified UniParc UPI.
    
    Args:
        uniparc_id: UniParc UPI ID (string, required)
    
    Query example: {"uniparc_id": "UPI000041C017"}
    
    Returns:
        A JSON string containing streamed cross-reference entries, each linking the UniParc ID to source database accession numbers, including details such as database type, accession, version, activity status, and taxonomy information.
    """

    try:
        result = uniprot_api.stream_uniparc_cross_references_by_upi(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_uniparc_entries(uniparc_id: str):
    """
    Stream all UniParc entries associated with the specified search term in a single download.
    
    Args:
        uniparc_id: Search term for UniParc entries, typically a UniParc UPI ID (string, required)
    
    Query example: {"uniparc_id": "UPI0000086E9C"}
    
    Returns:
        A JSON string containing a list of UniParc entries matching the search term. Each entry includes the UniParc ID, sequence details (value, length, molecular weight, CRC64 checksum, MD5 hash), cross-reference count, UniProtKB accessions, common taxons, and sequence features from databases like Pfam, InterPro, and PROSITE.
    """

    try:
        result = uniprot_api.stream_uniparc_entries(uniparc_id=uniparc_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_uniparc_entries(entry: str):
    """
    Search UniParc entries using a query, returns paginated list.
    
    Args:
        entry: Search term for UniParc entries, typically in the format "field:value" (e.g., "protein:hemoglobin") (string, required)
    
    Query example: {"entry": "protein:hemoglobin"}
    
    Returns:
        A JSON string containing a paginated list of UniParc entries matching the search query. Each entry includes the UniParc ID, sequence details (value, length, molecular weight, CRC64 checksum, MD5 hash), cross-reference count, UniProtKB accessions, common taxons, sequence features from databases like Pfam and PROSITE, and cross-reference creation/update dates.
    """

    try:
        result = uniprot_api.search_uniparc_entries(entry=entry)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_gene_centric_by_accession(accession: str):
    """
    
    Retrieve a GeneCentric entry by UniProtKB accession.
    
    Args:
        accession: UniProtKB accession ID (string)
    
    
    Query example: {"accession": "P12345"}
    
    Returns:
        A list of dictionaries containing:
    Gene Name: The standardized gene symbol associated with the protein
    Protein Name: The descriptive name of the protein
    UniProtKB ID: The UniProt accession number (primary identifier)
    Proteome ID: The identifier for the proteome entry containing the protein
    Organism: Species name
    Taxon ID: NCBI taxonomy identifier of the organism
    Entry Type: UniProt entry status
    Protein Existence: Evidence level for the protein
    Flag Type: Additional annotation ('Precursor' indicates precursor status)
    Sequence:
    -Length: Number of amino acids
    -Molecular Weight: Approximate mass in Daltons
    -CRC64: Checksum for the sequence
    -MD5: MD5 hash of the sequence
    -Sequence Version: Version number of the sequence in UniProt
    """

    try:
        result = uniprot_api.get_gene_centric_by_accession(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_gene_centric_by_proteome(upid: str):
    """
    
    Search GeneCentric entry by Proteome ID to return all data associated with that entry.
    
    Args:
        upid: UniProt Proteome ID (string)
    
    
    Query example: {"upid": "UP000005640"}
    
    Returns:
        List of dictionaries containing:
    Gene Name: The gene symbol
    Protein Name: The full name or description of the protein
    UniProtKB ID: The UniProt identifier for the canonical protein
    Proteome ID: The proteome identifier where the protein belongs
    Organism: The species name 
    Taxon ID: NCBI taxonomy ID 
    Entry Type: Status of the UniProt entry
    Protein Existence: Evidence level 
    Flag Type: Annotation detail like "Precursor" or "Fragment"
    Sequence:
    -Length: Amino acid count
    -Molecular Weight: In Daltons
    -CRC64: Checksum
    -MD5: MD5 hash
    -Sequence Version: The version number of the sequence
    """

    try:
        result = uniprot_api.get_gene_centric_by_proteome(upid=upid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_gene_centric(accession: str):
    """
    
    Stream GeneCentric entries matching a query (max 10M entries).
    Args:
        accession (str): Search term for GeneCentric entries.
    Returns:
        JSON string with all matching GeneCentric entries.
    
    Query example: {"accession": "gene:PAX6"}
    """

    try:
        result = uniprot_api.stream_gene_centric(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_gene_centric(accession: str):
    """
    
    Search GeneCentric entries with pagination.
    Args:
        accession (str): Search term for GeneCentric entries.
    Returns:
        JSON string with paginated GeneCentric entries.
    
    Query example: {"accession": "gene:TP53"}
    """

    try:
        result = uniprot_api.search_gene_centric(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_proteome_by_id(upid: str):
    """
    
    Retrieve a proteome by UniProt Proteome ID.
    Args:
        upid (str): UniProt Proteome ID.
    Returns:
        JSON string with proteome data.
    
    Query example: {"upid": "UP000002311"}
    """

    try:
        result = uniprot_api.get_proteome_by_id(upid=upid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def stream_proteomes(query: str):
    """
    Stream Proteome entries matching a query (max 10M entries).
    Args:
        query (str): Search term for proteomes.
    Returns:
        JSON string with all matching proteomes.
    """
    try:
        result = uniprot_api.stream_proteomes(query=query)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def search_proteomes(query: str, size: int = 50):
    """
    Search Proteome entries with pagination.
    Args:
        query (str): Search term for proteomes.
        size (int, optional): Number of entries per page. Default is 50.
    Returns:
        JSON string with paginated proteome entries.
    """
    try:
        result = uniprot_api.search_proteomes(query=query, size=size)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.prompt()
def system_prompt():
    """System prompt for UniProt MCP server client."""
    prompt = """You have access to tools for searching UniProt: protein knowledgebase and related resources.\nUse the API tools to extract the relevant information.\nFill in missing arguments with sensible values if the user hasn't provided them."""
    return prompt

