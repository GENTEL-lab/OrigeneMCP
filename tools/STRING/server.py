from mcp.server.fastmcp import FastMCP

from tools.STRING.string_api import StringAPI


mcp = FastMCP(
    "string_mcp",
    stateless_http=True,
)
string_api = StringAPI()


@mcp.tool()
async def mapping_identifiers(genes: list[str], species: int):
    """
    Maps common protein names, synonyms and UniProt identifiers into STRING identifiers
    
    Args:
        genes: A list of names of the genes, required (array)
        species: A number of NCBI/STRING taxon (integer)
    
    Query example: {"genes": ["TP53", "BRCA1"], "species": 9606}
    
    Returns:
        List of dictionaries containing STRING identifiers for genes
    """

    try:
        result = string_api.mapping_identifiers(identifiers=genes, species=species)
    except Exception as e:
        return [{"error": f"An error occurred while mapping identifiers: {str(e)}"}]
    return result


@mcp.tool()
async def get_string_network_interaction(
    identifiers: list[str],
    species: int,
    required_score: int,
    add_nodes: int,
    network_type: str,
    show_query_node_labels: int,
):
    """
    Retrieve STRING interaction network for one or multiple proteins in various text formats.
    It will tell you the combined score and all the channel specific scores for the set of proteins.
    You can also extend the network neighborhood by setting "add_nodes", which will add, to your network, new interaction partners in order of their confidence.
    
    Args:
        identifiers: required parameter for a list of multiple items (array)
        species: A number of NCBI/STRING taxon (e.g. 9606 for human, or STRG0A10090 for house mouse) (integer)
        required_score:  Filtering low-quality interactions ,a number between 0 and 1000 (integer)
        add_nodes: Number of associated genes added in addition to the initial query genesAdd Nodes (integer)
        network_type: network type: functional (default), physical (string)
        show_query_node_labels: Whether to label the query gene in the result (1 for yes, 0 for no) (integer)
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "required_score": 700, "add_nodes": 5, "network_type": "physical", "show_query_node_labels": 1}
    
    Returns:
        A dictionary containing the following fields:
        stringId_A:     STRING identifier (protein A)
        stringId_B:     STRING identifier (protein B)
        preferredName_A: common protein name (protein A)
        preferredName_B: common protein name (protein B)
        ncbiTaxonId: NCBI taxon identifier
        score:  combined score
        nscore: gene neighborhood score
        fscore: gene fusion score
        pscore: phylogenetic profile score
        ascore: coexpression score
        escore: experimental score
        dscore: database score
        tscore: textmining score
    """

    try:
        result = string_api.get_string_network_interaction(
            identifiers=identifiers,
            species=species,
            required_score=required_score,
            add_nodes=add_nodes,
            network_type=network_type,
            show_query_node_labels=show_query_node_labels,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting STRING network interaction: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_all_interaction_partners_of_the_protein_set(
    identifiers: list[str],
    species: int,
    limit: int,
    required_score: int,
    network_type: str,
):
    """
    This method provides the interactions between your provided set of proteins and all the other STRING proteins.
    As STRING network usually has a lot of low scoring interactions, you may want to limit the number of retrieved interaction per protein using "limit" parameter.
    
    Args:
        identifiers:required parameter for a list of multiple items
        species:NCBI/STRING taxon (e.g. 9606 for human, or STRG0AXXXXX).
        limit:  limits the number of interaction partners retrieved per protein (most confident interactions come first)
        required_score: threshold of significance to include a interaction, a number between 0 and 1000 (default depends on the network)
        network_type:   network type: functional (default), physical
        
    Returns:
        A dictionary containing the following fields:
        stringId_A:     STRING identifier (protein A)
        stringId_B:     STRING identifier (protein B)
        preferredName_A:common protein name (protein A)
        preferredName_B:common protein name (protein B)
        ncbiTaxonId:NCBI taxon identifier
        score:  combined score
        nscore: gene neighborhood score
        fscore: gene fusion score
        pscore: phylogenetic profile score
        ascore: coexpression score
        escore: experimental score
        dscore: database score
        tscore: textmining score
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "limit": 20, "required_score": 700, "network_type": "physical"}
    """

    try:
        result = string_api.get_all_interaction_partners_of_the_protein_set(
            identifiers=identifiers,
            species=species,
            required_score=required_score,
            limit=limit,
            network_type=network_type,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting all interaction partners of the protein set: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_similarity_scores_of_the_protein_set(identifiers: list[str], species: int):
    """
    STRING internally uses the Smith-Waterman bit scores as a proxy for protein homology.
    Using this API you can retrieve these scores between the proteins in a selected species.
    They are symmetric,meaning A->B is equal to B->A.
    The bit score cut-off below which we do not store or report homology is 50.
    
    Args:
        identifiers:required parameter for a list of multiple items
        species:NCBI/STRING taxon (e.g. 9606 for human, or STRG0AXXXXX)
        
    Returns:
        A dictionary containing the following fields:
        ncbiTaxonId_A:  NCBI taxon identifier (protein A)
        stringId_A:     STRING identifier (protein A)
        ncbiTaxonId_B:  NCBI taxon identifier (protein B)
        stringId_B:     STRING identifier (protein B)
        bitscore: Smith-Waterman alignment bit score
    
    Query example: {"identifiers": ["Syp", "Dlg4", "Grin2b"], "species": 10090}
    """

    try:
        result = string_api.get_similarity_scores_of_the_protein_set(
            identifiers=identifiers, species=species
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting similarity scores of the protein set: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_best_similarity_hits_between_species(identifiers: list[str], species: int, species_b: list[int]):
    """
    Retrieve the similarity from your input protein(s) to the best (most) similar protein from each STRING species.
    
    Args:
        identifiers:required parameter for a list of multiple items
        species:Specify the species of the input identifier (e.g. 9606 for human, or STRG0AXXXXX)
        species_b: a list of NCBI taxon identifiers of the target species to be compared ,seperated by "%0d" (e.g. human, fly and yeast would be "9606%0d7227%0d4932")
        
    Returns:
        A dictionary containing the following fields:
        ncbiTaxonId_A:  NCBI taxon identifier (protein A)
        stringId_A:     STRING identifier (protein A)Taxonomy ID of the target species to be compared
        ncbiTaxonId_B:  NCBI taxon identifier (protein B)
        stringId_B:     STRING identifier (protein B)
        bitscore:       Smith-Waterman alignment bit score
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "species_b": [10090, 10116]}
    """

    try:
        result = string_api.get_best_similarity_hits_between_species(
            identifiers=identifiers, species=species, species_b=species_b
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting best similarity hits of the protein set between species: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_functional_enrichment(identifiers: list[str], species: int, background_string_identifiers: str):
    """
    STRING maps several databases onto its proteins, this includes: Gene Ontology, KEGG pathways, UniProt Keywords, PubMed publications, Pfam domains, InterPro domains, and SMART domains.
    The STRING enrichment API method allows you to retrieve functional enrichment for any set of input proteins.
    It will tell you which of your input proteins have an enriched term and the term's description.
    The API provides the raw p-values, as well as, False Discovery Rate (B-H corrected p-values).
    Args:
        identifiers:required parameter for a list of multiple items
        background_string_identifiers:	using this parameter you can specify the background proteome of your experiment. Only STRING identifiers will be recognised (each must be seperated by "%0d") e.g. '7227.FBpp0077451%0d7227.FBpp0074373'. You can map STRING identifiers using mapping identifiers method.
        species:NCBI/STRING taxon (e.g. 9606 for human, or STRG0AXXXXX)
    Returns:
        category:term category (e.g. GO Process, KEGG pathways)
        term:enriched term (GO term, domain or pathway)
        number_of_genes:number of genes in your input list with the term assigned
        number_of_genes_in_background:total number of genes in the background proteome with the term assigned
        ncbiTaxonId:NCBI taxon identifier
        inputGenes:	gene names from your input
        preferredNames:	common protein names (in the same order as your input Genes)
        p_value:raw p-value
        fdr:False Discovery Rate
        description:description of the enriched term
    """
    try:
        result = string_api.get_functional_enrichment(
            identifiers=identifiers,
            species=species,
            background_string_identifiers=background_string_identifiers,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting functional enrichment for proteins: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_functional_annotation(identifiers: list[str], species: int, allow_pubmed: int, only_pubmed: int):
    """
    STRING maps several databases onto its proteins, this includes: Gene Ontology, KEGG pathways, UniProt Keywords, PubMed publications, Pfam domains, InterPro domains, and SMART domains.
    
    Args:
        identifiers:required parameter for a list of multiple items
        species:NCBI/STRING taxon (e.g. 9606 for human, or STRG0AXXXXX see: STRING organisms).
        allow_pubmed: 1 to print also the PubMed annotations in addition to other categories, default is 0
        only_pubmed: 1 to print only PubMed annotations, default is 0
    
    Returns:
        A dictionary containing the following fields:
        category:term category (e.g. GO Process, KEGG pathways)
        term:enriched term (GO term, domain or pathway)
        number_of_genes:number of genes in your input list with the term assigned
        ratio_in_set:ratio of the proteins in your input list with the term assigned
        ncbiTaxonId:NCBI taxon identifier
        inputGenes:gene names from your input
        preferredNames:common protein names (in the same order as your input Genes)
        description:description of the enriched term
    
    Query example: {"identifiers": ["TP53", "BRCA1"], "species": 9606, "allow_pubmed": 1, "only_pubmed": 0}
    """

    try:
        result = string_api.get_functional_annotation(
            identifiers=identifiers,
            species=species,
            allow_pubmed=allow_pubmed,
            only_pubmed=only_pubmed,
        )
    except Exception as e:
        return [
            {
                "error": f"An error occurred while getting functional annotation for proteins: {str(e)}"
            }
        ]
    return result


@mcp.tool()
async def get_ppi_enrichment(identifiers: list[str], species: int):
    """
    Get protein-protein interaction enrichment for list of genes denoted by their STRING identifiers
    
    Args:
        identifiers: A list of STRING identifiers of the genes
        species: A number of NCBI/STRING taxon (e.g. 9606 for human, or STRG0A10090 for house mouse)
    
    Returns:
        A dictionary containing the following fields:
        number_of_nodes: number of proteins in your network
        number_of_edges: number of edges in your network
        average_node_degree: mean degree of the node in your network
        local_clustering_coefficient: average local clustering coefficient
        expected_number_of_edges: expected number of edges based on the nodes degrees
        p_value: significance of your network having more interactions than expected
    
    Query example: {"identifiers": ["Pax6", "Sox2", "Nanog"], "species": 10090}
    """

    try:
        result = string_api.get_ppi_enrichment(identifiers=identifiers, species=species)
    except Exception as e:
        return {"error": f"An error occurred while getting ppi enrichment: {str(e)}"}
    return result


@mcp.prompt()
def system_prompt() -> str:
    """System prompt for client."""
    prompt = """You have access to tools for searching STRING: functional proteins association networks.
    Use the API tools to extract the relevant information.
    Fill in missing arguments with sensible values if the user hasn't provided them such as the STRING identifiers. """
    return prompt
