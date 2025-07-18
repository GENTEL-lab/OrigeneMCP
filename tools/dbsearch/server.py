from mcp.server.fastmcp import FastMCP

from tools.dbsearch.dbsearch_api import DBSearch

mcp = FastMCP(
    "dbsearch_mcp",
    stateless_http=True,
)

dbsearch = DBSearch()


@mcp.tool()
async def clinvar_get_best_refseqid_by_sequence(seq: str, retries: int = 3, wait: int = 5):
    """Find best matching RefSeq ID for a protein sequence using BLASTP.
    
    Args:
        seq (str): Protein sequence to search
        retries (int): Number of retry attempts if BLAST fails (default: 3)
        wait (int): Seconds to wait between retries (default: 5)
        
    Returns:
        Optional[str]: Matching RefSeq ID (e.g. "NP_123456") if found with 100% identity,
                      None if no exact match found or error occurs.
    """
    try:
        return dbsearch.clinvar_get_best_refseqid_by_sequence(seq, retries, wait)
    except Exception:
        return None

@mcp.tool()
async def clinvar_query_variant_significance(refseqid: str = None, variant: str = None, hgvs: str = None):
    """Query ClinVar for variant classification/significance.
    
    Args:
        refseqid (str): RefSeq protein ID (e.g. "NP_123456")
        variant (str): Protein variant in HGVS format (e.g. "P123L")
        hgvs (str): Full HGVS notation (e.g. "NP_123456.1:p.P123L")
        
    Returns:
        Union[dict, str]: 
            - dict: ClinVar germline_classification data if found
            - str: Error message if variant not found or error occurs
    """
    try:
        return dbsearch.clinvar_query_variant_significance(refseqid, variant, hgvs)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def clinvar_query_sequence_variants(sequence: str, variants: list[str]):
    """Query ClinVar for multiple variants on a protein sequence.
    
    Args:
        sequence (str): Reference protein sequence
        variants (list[str]): List of variant strings (e.g. ["P123L", "R456K"])
        
    Returns:
        dict: Mapping of variants to their ClinVar significance results
              Empty dict if no RefSeq ID found for sequence or error occurs
    """
    try:
        return dbsearch.clinvar_query_sequence_variants(sequence, variants)
    except Exception as e:
        return str(e)

@mcp.tool()
async def clinvar_find_single_mutation(mutant_seq: str):
    """Find single amino acid mutation between mutant and reference sequences.
    
    Args:
        mutant_seq (str): Mutant protein sequence
        
    Returns:
        Optional[dict]: Dictionary with mutation details if single mutation found:
            - ref_id: Reference RefSeq ID
            - hgvs: HGVS notation
            - variant: Variant string
            - pos: Mutation position
            - wildtype: Wildtype amino acid  
            - mutant: Mutant amino acid
            Returns None if no single mutation found or error occurs.
    """
    try:
        return dbsearch.clinvar_find_single_mutation(mutant_seq)
    except Exception as e:
        return str(e)

@mcp.tool()
async def get_genes_in_region(chrom: str, start: int, end: int):
    """
    Query Ensembl REST API to get genes within a specific genomic region.

    Args:
        chrom (str): Chromosome (e.g., 'chr10').
        start (int): Start coordinate.
        end (int): End coordinate.

    Returns:
        List[str]: List of gene names within the region.
    """
    return dbsearch.get_genes_in_region(chrom, start, end)

@mcp.tool()
async def ensembl_get_genes_by_band(query_band: str):
    """
    Extract genes in a cytogenetic band region (e.g., 'chr10q21').

    Args:
        query_band (str): Band query like 'chr10q21'.

    Returns:
        List[str]: List of gene names in the specified cytoband region.
    """
    return dbsearch.ensembl_get_genes_by_band(query_band)

@mcp.tool()
async def gsea_get_genelist_from_genesetname(genesetname: str):
    """
    Retrieve the list of genes from a specific gene set in the GSEA database.

    Args:
        genesetname (str): The name of the gene set to query (e.g., "CAMP_UP.V1_DN", "SCHERER_PBMC_APSV_WETVAX_AGE_18_40YO_5_TO_7DY_UP").
            This should be the identifier used in the GSEA database for the gene set.

    Returns:
        list: A list of gene symbols contained in the specified gene set.
                If the gene set is not found or an error occurs, an empty list is returned.
    """
    return dbsearch.gsea_get_genelist_from_genesetname(genesetname)

@mcp.tool()
async def gtrd_gene_to_entry(gene_name: str, organism: str = None):
    """
    Convert a gene symbol to UniProt protein entry ID(s) using GTRD API.
    
    Args:
        gene_name (str): Gene symbol, e.g. "TP53"
        organism (str): Optional NCBI Taxonomy ID (default: None uses API default)
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: The UniProt Entry ID (e.g. "P04637")
                
        Returns empty list if conversion fails or no results found.
        
    Example:
        >>> await gtrd_gene_to_entry("TP53")
        "P04637"
    """
    try:
        entry = dbsearch.gtrd_gene_to_entry(gene_name, organism)
        return entry
    except Exception as e:
        return str(e)

@mcp.tool() 
async def gtrd_entry_to_target_genes(entry: str, promoter_dir: str = None):
    """
    Retrieve target genes for a UniProt entry using GTRD promoter data.
    
    Args:
        entry (str): UniProt accession ID (e.g. "P04637")
        promoter_dir (str): Optional path to promoter files directory
        
    Returns:
        List[types.TextContent]: A list containing one TextContent object with:
            - text: JSON array of target gene symbols
                
        Returns empty list if no target genes found or error occurs.
        
    Example:
        >>> await gtrd_entry_to_target_genes("P04637")
        ["GENE1", "GENE2", ...]
    """
    try:
        target_genes = dbsearch.gtrd_entry_to_target_genes(entry, promoter_dir)
        return target_genes
    except Exception as e:
        return str(e)

@mcp.tool()
async def mirdb_get_geneset_by_mirname(mirname: str, candidates: list[str]):
    """
    Query the predicted target gene symbols for a specific human miRNA (e.g., hsa-miR-3140-5p) from the miRDB database.

    Args:
        mirname (str): The name of the human miRNA. It must follow one of the standard naming formats:
            - 3-part format: hsa-mir-8068
            - 4-part format: hsa-mir-3140-5p or hsa-let-7g-5p  
            All valid miRNA names must begin with the "hsa-" prefix.
        candidates (list[str]): The choice list of target gene symbols

   Returns:
        {
            "predicted_targets": ["HECTD1"],
            "not_predicted_targets": ["SPAG9", "SPATA31C2", "OR10J4"]
        }
    """
    return dbsearch.mirdb_get_geneset_by_mirname(mirname, candidates)

@mcp.tool()
async def mousemine_get_geneset_from_mpid(mpid: str):
    """
    Retrieve a list of mouse gene symbols associated with a given MGI phenotype ID (MPID)
    from the MouseMine keyword search results page.

    Args:
        mpid (str): Mouse Phenotype ID (e.g., "MP:0005386") to query in MouseMine.

    Returns:
        List[str]: A list of gene symbols (strings) associated with the given MPID.
                Only includes genes of type "Protein Coding Gene".

    Example:
        >>> self.mousemine_get_geneset_from_mpid("MP:0005386")
        ['Trp53', 'Cdkn1a', 'Brca1']
    """
    return dbsearch.mousemine_get_geneset_from_mpid(mpid)

@mcp.tool()
async def phipster_vpname2vpid(vpname: str):
    """
    Convert a viral protein name (vpname) to its corresponding VPID using the PHIPSTER vpid2name mapping API.

    Args:
        vpname (str): The **pure name** of the viral protein, with the virus species prefix removed.

    If the viral protein name is something like:
        `"Japanese encephalitis virus envelope protein"`

    You must pass only the **protein name part**:
        `"envelope protein"`

    Do NOT include the virus prefix:
        `"Japanese encephalitis virus"` ← This must be stripped off.

    Format examples of valid `vpname`:
        - "hypothetical protein (gene: A11R)"
        - "Kelch-like protein (gene: C9L)"
        - "envelope protein"
        - "72L protein (gene: 72L)"
        - "encoded endoprotease (Late protein 3)"

    Returns:
        The corresponding VPID as a string (e.g., "23488") if found, otherwise None.
        
        Example:
            "23488"
    """
    return dbsearch.phipster_vpname2vpid(vpname)

@mcp.tool()
async def phipster_get_hpid_list_by_vpid(vpid: str):
    """
    Retrieve a list of protein-protein interaction (PPI) records between a viral protein and human proteins 
    from the Phipster database by viral protein ID (VPID).

    Args:
        vpid: The viral protein ID to query interactions for.

    Returns:
    A list of hpid, each human protein id interaction the given viral protein.
        Example:
            ["23488", "23485", ...]
    """
    return dbsearch.phipster_get_hpid_list_by_vpid(vpid)

@mcp.tool()
async def phipster_hpid_list_to_hpname_list(hpid_list: list[int]):
    """
    Convert a list of hpid records to records human protein names, using the PHIPSTER database mapping.

    Args:
        hpid_list: A list of hpid

    Returns:
        A list of hpname by a corresponding 'humanprotein_name'.
        If a name is not found for a given ID, it will be labeled as 'Unknown_{id}'.
        
        Example:
        Input:
        [5095, 4427, 5539, 15404, 6385, 3727, 5161, 17652, 6447, 3758, 7540]
        Output:
        ['STAT3', 'CDK2', 'GSK3B', 'TRIB3', 'GRB2', 'SRC', 'STAT1', 'ARHGEF4', 'CSNK2A1', 'ITGA4', 'IL18']
    """
    return dbsearch.phipster_hpid_list_to_hpname_list(hpid_list)
