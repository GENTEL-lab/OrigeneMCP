from mcp.server.fastmcp import FastMCP

from tools.ensembl.ensembl_api import EnsemblClient


mcp = FastMCP(
    "ensembl_mcp",
    stateless_http=True,
)

ensembl_api = EnsemblClient()


DEFAULT_MAX_LENGTH = 10240


@mcp.tool()
async def get_lookup_symbol(symbol: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """
    Look up Ensembl gene information by external gene symbol.
    
    This function allows you to find Ensembl gene records using standard gene symbols
    (e.g., HGNC symbols for human genes).
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human, 'mus_musculus' for mouse)
        symbol: Official gene symbol (e.g., 'BRCA2', 'TP53', 'APOE')
        max_length: Maximum length of the response in approximate tokens (default: 8192)
    
    Query example: {"species": "homo_sapiens", "symbol": "BRCA2"}
    
    Returns:
        Dictionary containing comprehensive gene information including Ensembl ID, genomic location,
        biotype (e.g., protein_coding, lncRNA), description, and cross-references to external databases.
    """

    result = ensembl_api.get_lookup_symbol(species=species, symbol=symbol, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while looking up gene: {result['error']}"}
    return result

@mcp.tool()
async def get_homology_symbol(symbol: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """
    Find evolutionary homologs (orthologs and paralogs) for a gene identified by symbol.
    
    Retrieve homologous genes across different species, with alignment statistics and
    taxonomic information. Essential for comparative genomics and evolutionary studies.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        symbol: Official gene symbol (e.g., 'BRCA2', 'TP53', 'FOXP2')
        max_length: Maximum length of the response in approximate tokens (default: 8192)
    
    Query example: {"species": "homo_sapiens", "symbol": "FOXP2"}
    
    Returns:
        Dictionary containing homology information including:
        - Orthologs (genes in different species derived from a common ancestral gene)
        - Paralogs (genes derived from duplication within a genome)
        - Alignment statistics (identity, coverage)
        - Taxonomic information for each homolog
    """

    result = ensembl_api.get_homology_symbol(species=species, symbol=symbol, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting homology: {result['error']}"}
    return result

@mcp.tool()
async def get_sequence_region(region: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """
    Retrieve genomic DNA sequence for a specific chromosomal region.
    
    Extract the raw nucleotide sequence from a specific genomic location, which can be
    used for primer design, variant analysis, or sequence feature identification.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        region: Genomic region in format 'chromosome:start..end' (e.g., 'X:1000000..1000100',
                '7:55152337..55207337', 'MT:1..16569'). Coordinates are 1-based inclusive.
        max_length: Maximum length of the response in approximate tokens (default: 8192)
    
    Query example: {"species": "homo_sapiens", "region": "X:1000000..1000100"}
    
    Returns:
        Dictionary containing the DNA sequence as a string of nucleotides (A,C,G,T),
        along with metadata about the region, sequence length, and coordinate system.
    """

    result = ensembl_api.get_sequence_region(species=species, region=region, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting sequence: {result['error']}"}
    return result

@mcp.tool()
async def get_vep_hgvs(hgvs_notation: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """
    Predict the functional effects of variants using Variant Effect Predictor (VEP) with HGVS notation.
    
    Analyzes the molecular consequences of genetic variants on genes, transcripts, and protein sequences.
    VEP provides comprehensive annotation including protein changes, regulatory effects, conservation scores,
    and pathogenicity predictions.

    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        hgvs_notation: Variant in HGVS (Human Genome Variation Society) notation format 
                      (e.g., 'ENST00000269305.4:c.2309C>T', 'NM_000059.3:c.274G>A', 
                       'NC_000017.10:g.7676154G>T')
        max_length: Maximum length of the response in approximate tokens (default: 8192)

    Returns:
        Dictionary containing detailed variant effect predictions, including:
        - Affected genes and transcripts
        - Effect on protein sequence (missense, nonsense, etc.)
        - SIFT and PolyPhen pathogenicity scores
        - Conservation scores
        - Allele frequencies in population databases
        - Regulatory feature annotations
        - Clinical significance annotations
    """
    result = ensembl_api.get_vep_hgvs(species=species, hgvs_notation=hgvs_notation, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting variant effect: {result['error']}"}
    return result

@mcp.tool()
async def get_genetree_id(id: str, max_length: int = DEFAULT_MAX_LENGTH, species: str = "homo_sapiens"):
    """
    Retrieve a phylogenetic gene tree by its Ensembl stable identifier.
    
    Gene trees represent the evolutionary history of genes across species, showing
    orthologous and paralogous relationships. These trees are constructed using
    protein sequence alignments and phylogenetic algorithms.
    
    Args:
        id: Ensembl gene tree stable identifier (e.g., 'ENSGT00390000003602')
        max_length: Maximum length of the response in approximate tokens (default: 8192)
    
    Query example: {"id": "ENSGT00390000003602"}
    
    Returns:
        Dictionary containing gene tree information in a nested structure, including:
        - Taxonomy and sequence relationships
        - Branch lengths representing evolutionary distance
        - Bootstrap values indicating tree confidence
        - Sequence alignments used to build the tree
        - Member genes from different species
    """

    result = ensembl_api.get_genetree_id(id=id, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting gene tree: {result['error']}"}
    return result

@mcp.tool()
async def get_info_assembly(species: str, max_length: int = DEFAULT_MAX_LENGTH):
    """
    Retrieve genome assembly information for a species.
    
    Provides details about the reference genome assembly used in Ensembl, including
    assembly version, accession numbers, and overall structure. Essential for
    understanding coordinate systems and genome organization.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human, 
                 'mus_musculus' for mouse, 'danio_rerio' for zebrafish)
        max_length: Maximum length of the response in approximate tokens (default: 8192)
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        Dictionary containing comprehensive assembly information including:
        - Assembly name and version (e.g., 'GRCh38' for human)
        - Assembly accession (e.g., 'GCA_000001405.15')
        - Toplevel sequences (chromosomes, scaffolds, contigs)
        - Coordinate system information
        - Assembly date and source
        - Assembly statistics (sequence counts, lengths)
    """

    result = ensembl_api.get_info_assembly(species=species, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while getting assembly info: {result['error']}"}
    return result

@mcp.tool()
async def get_xrefs_symbol(symbol: str, species: str = "homo_sapiens"):
    """
    Get cross references for a gene symbol.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        symbol: Gene symbol (e.g. 'BRCA2')
    
    Query example: {"species": "homo_sapiens", "symbol": "BRCA2"}
    
    Returns:
        A list of dictionaries containing cross references to other databases.
    """

    try:
        result = ensembl_api.get_xrefs_symbol(species=species, symbol=symbol)
    except Exception as e:
        return {"error": f"An error occurred while getting cross references: {str(e)}"}
    return result

# Archive endpoints
@mcp.tool()
async def get_archive_id(id: str):
    """
    Get the latest version of an Ensembl stable identifier.
    
    Args:
        id: Ensembl stable identifier (e.g., 'ENSG00000139618')
    
    Query example: {"id": "ENSG00000139618"}
    
    Returns:
        A dictionary containing the latest version information for the given identifier.
    """

    try:
        result = ensembl_api.get_archive_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_archive_id(ids: list[str]):
    """
    Get the latest version for multiple Ensembl stable identifiers.
    
    Args:
        ids: A list of Ensembl stable identifiers.
    
    Query example: {"ids": ["ENSG00000139618", "ENSG00000168269"]}
    
    Returns:
        A dictionary where keys are the input IDs and values are dictionaries containing the latest version information for each ID.
    """

    try:
        result = ensembl_api.post_archive_id(ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Comparative Genomics endpoints
@mcp.tool()
async def get_cafe_genetree_id(id: str):
    """
    Retrieve a CAFE (Computational Analysis of gene Family Evolution) gene tree by ID.
    
    CAFE analyzes the evolution of gene family size across a phylogenetic tree,
    identifying expansions and contractions of gene families throughout evolution.
    This helps understand adaptation, functional diversification, and species-specific traits.
    
    Args:
        id: Ensembl gene tree stable identifier (e.g., 'ENSGT00390000003602')
    
    Query example: {"id": "ENSGT00390000003602"}
    
    Returns:
        Dictionary containing CAFE gene tree data including:
        - Gene family size changes across evolutionary time
        - Statistical significance of expansions/contractions
        - P-values for gene family size changes
        - Species tree topology with gene count information
    """

    try:
        result = ensembl_api.get_cafe_genetree_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_cafe_genetree_member_symbol(symbol: str, species: str = "homo_sapiens"):
    """
    Retrieve a CAFE gene tree for a gene identified by symbol.
    
    Get gene family evolution analysis (expansions/contractions) for a gene family
    that contains the specified gene. Identifies evolutionary patterns without
    needing to know the specific gene tree ID.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        symbol: Official gene symbol (e.g., 'BRCA2', 'TP53', 'OR4F5')
    
    Query example: {"species": "homo_sapiens", "symbol": "OR4F5"}
    
    Returns:
        Dictionary containing CAFE gene tree data including:
        - Gene family size changes across evolutionary time
        - Statistical significance of expansions/contractions
        - P-values for gene family size changes
        - Species tree topology with gene count information
    """

    try:
        result = ensembl_api.get_cafe_genetree_member_symbol(species=species, symbol=symbol)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_cafe_genetree_member_id(id: str, species: str = "homo_sapiens"):
    """
    Retrieve the gene tree containing a gene identified by its Ensembl ID.
    
    Find the phylogenetic tree showing evolutionary relationships for a gene of interest,
    identified using its Ensembl stable identifier. Useful for understanding gene evolution
    when you have the specific gene ID.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        id: Ensembl gene, transcript, or translation stable identifier
            (e.g., 'ENSG00000139618' for human BRCA2 gene)
    
    Query example: {"species": "homo_sapiens", "id": "ENSG00000139618"}
    
    Returns:
        Dictionary containing gene tree information in a nested structure, including:
        - Taxonomy and sequence relationships
        - Branch lengths representing evolutionary distance
        - Bootstrap values indicating tree confidence
        - Sequence alignments used to build the tree
        - Member genes from different species
    """

    try:
        result = ensembl_api.get_cafe_genetree_member_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_genetree_member_symbol(symbol: str, species: str = "homo_sapiens"):
    """
    Get gene tree by symbol.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        symbol: Gene symbol
    
    Query example: {"species": "homo_sapiens", "symbol": "BRCA2"}
    
    Returns:
        Dictionary containing gene tree information.
    """

    try:
        result = ensembl_api.get_genetree_member_symbol(species=species, symbol=symbol)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_alignment_region(region: str, species: str = "homo_sapiens"):
    """
    Retrieve genomic alignments between species for a specific region.
    
    Get multiple sequence alignments of genomic regions across species, showing
    evolutionary conservation and divergence. Crucial for identifying conserved
    functional elements like enhancers or detecting selection pressure.
    
    Args:
        species: Reference species name in snake_case format (e.g., 'homo_sapiens')
        region: Genomic region in format 'chromosome:start..end' (e.g., 'X:1000000..1000100')
                Coordinates are 1-based inclusive.
    
    Query example: {"species": "homo_sapiens", "region": "X:1000000..1000100"}
    
    Returns:
        Dictionary containing aligned sequences from multiple species in the specified region,
        with alignment blocks, scores, and coordinate mappings between genomes.
    """

    try:
        result = ensembl_api.get_alignment_region(species=species, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_homology_id(id: str, species: str = "homo_sapiens"):
    """
    Find evolutionary homologs (orthologs and paralogs) for a gene identified by Ensembl ID.
    
    Retrieve homologous genes across different species, with alignment statistics and
    taxonomic information. Essential for comparative genomics and evolutionary studies.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        id: Ensembl gene ID (e.g., 'ENSG00000139618' for human BRCA2 gene)
    
    Query example: {"species": "homo_sapiens", "id": "ENSG00000139618"}
    
    Returns:
        Dictionary containing homology information including:
        - Orthologs (genes in different species derived from a common ancestral gene)
        - Paralogs (genes derived from duplication within a genome)
        - Alignment statistics (identity, coverage)
        - Taxonomic information for each homolog
    """

    try:
        result = ensembl_api.get_homology_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Cross References endpoints
@mcp.tool()
async def get_xrefs_id(id: str):
    """
    Get cross references by ID.
    
    Args:
        id: Ensembl stable identifier
    
    Query example: {"id": "ENSG00000139618"}
    
    Returns:
        A list of dictionaries containing cross references to other databases.
    """

    try:
        result = ensembl_api.get_xrefs_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_xrefs_name(name: str, species: str = "homo_sapiens"):
    """
    Get cross references by name.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        name: External name
    
    Query example: {"species": "homo_sapiens", "name": "BRCA2"}
    
    Returns:
        A list of dictionaries containing cross references to other databases.
    """

    try:
        result = ensembl_api.get_xrefs_name(species=species, name=name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Information endpoints
@mcp.tool()
async def get_info_analysis(species: str = "homo_sapiens"):
    """
    List the analyses and data processing pipelines used for a species genome.
    
    Provides information about the computational methods and analyses used to generate
    Ensembl data for a species, including gene annotation methods, comparative genomics
    analyses, and variation data processing.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        Dictionary containing analysis information for the species, including:
        - Gene annotation methods and sources
        - Alignment algorithms used
        - Variation calling procedures
        - Regulatory feature detection methods
        - Comparative genomics pipeline details
    """

    try:
        result = ensembl_api.get_info_analysis(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_assembly_region_info(region_name: str, species: str = "homo_sapiens"):
    """
    Retrieve detailed information about a specific genomic region or chromosome.
    
    Get assembly metadata for a particular sequence within a genome assembly,
    such as chromosome length, scaffold composition, or contig information.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        region_name: Name of the toplevel sequence (e.g., '1' for chromosome 1, 
                     'X' for X chromosome, 'KZ622775.1' for a scaffold)
    
    Query example: {"species": "homo_sapiens", "region_name": "X"}
    
    Returns:
        Dictionary containing detailed information about the specified region, including:
        - Sequence length
        - Coordinate system
        - Assembly exceptions (if any)
        - Sequence composition
        - Associated metadata and attributes
    """

    try:
        result = ensembl_api.get_assembly_region_info(species=species, region_name=region_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_biotypes(species: str = "homo_sapiens"):
    """
    Retrieve the catalog of gene and transcript biotypes for a species.
    
    Biotypes classify genes and transcripts according to their biological nature,
    such as protein-coding, pseudogene, or various non-coding RNA categories.
    This information is crucial for filtering and interpreting genomic data.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        A list of dictionaries, where each dictionary describes an available biotype for the species.
    """

    try:
        result = ensembl_api.get_info_biotypes(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_compara_methods():
    """
    Get comparative analysis methods used in Ensembl Compara.
    
    Args:
    
    Query example: {}
    
    Returns:
        A dictionary containing the different classes of compara methods and the specific methods within each class.
    """

    try:
        result = ensembl_api.get_info_compara_methods()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_external_dbs(species: str):
    """
    Get external databases for a species.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        A list of dictionaries, where each dictionary contains information about an external database linked for the species.
    """

    try:
        result = ensembl_api.get_info_external_dbs(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Mapping endpoints
@mcp.tool()
async def get_map_cdna(id: str, region: str):
    """
    Map cDNA coordinates to genomic coordinates.
    
    Args:
        id: Transcript ID
        region: cDNA coordinates
    
    Query example: {"id": "ENST00000380152", "region": "100..300"}
    
    Returns:
        A dictionary containing a list of coordinate mapping results, where each result
        provides the genomic coordinates (chromosome, start, end, strand) for a
        segment of the input cDNA region.
    """

    try:
        result = ensembl_api.get_map_cdna(id=id, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_map_cds(id: str, region: str):
    """
    Map CDS coordinates to genomic coordinates.
    
    Args:
        id: Transcript ID
        region: CDS coordinates
    
    Query example: {"id": "ENST00000139618", "region": "1..200"}
    
    Returns:
        A dictionary containing a list of coordinate mapping results, where each result
        provides the genomic coordinates (chromosome, start, end, strand) for a
        segment of the input CDS region.
    """

    try:
        result = ensembl_api.get_map_cds(id=id, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_map_translation(id: str, region: str):
    """
    Map protein coordinates to genomic coordinates.
    
    Args:
        id: Translation ID
        region: Protein coordinates
    
    Query example: {"id": "ENSP00000265436", "region": "1..50"}
    
    Returns:
        A dictionary containing a list of coordinate mapping results, where each result
        provides the genomic coordinates (chromosome, start, end, strand) for a
        segment of the input protein region.
    """

    try:
        result = ensembl_api.get_map_translation(id=id, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Ontologies and Taxonomy endpoints
@mcp.tool()
async def get_ontology_ancestors(id: str):
    """
    Get ontology ancestors. Note: This tool is sensitive to the format of the input ID and may return a 400 Bad Request error for some valid-looking IDs. It is recommended to use IDs obtained directly from other Ensembl tools.
    
    Args:
        id: Ontology term ID (e.g., a GO term ID like 'GO:0006281').
    
    Query example: {"id": "GO:0006281"}
    
    Returns:
        A list of dictionaries, where each dictionary contains information about an ancestor ontology term.
    """

    try:
        result = ensembl_api.get_ontology_ancestors(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ontology_descendants(id: str):
    """
    Get ontology descendants. Note: This tool is sensitive to the format of the input ID and may return a 400 Bad Request error for some valid-looking IDs. It is recommended to use IDs obtained directly from other Ensembl tools.
    
    Args:
        id: Ontology term ID (e.g., a GO term ID like 'GO:0006281').
    
    Query example: {"id": "GO:0006281"}
    
    Returns:
        A list of dictionaries, where each dictionary contains information about a descendant ontology term.
    """

    try:
        result = ensembl_api.get_ontology_descendants(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ontology_id(id: str):
    """
    Get ontology by ID. Note: This tool is sensitive to the format of the input ID and may return a 400 Bad Request error for some valid-looking IDs. It is recommended to use IDs obtained directly from other Ensembl tools.
    
    Args:
        id: Ontology term ID (e.g., a GO term ID like 'GO:0006281').
    
    Query example: {"id": "GO:0006281"}
    
    Returns:
        Dictionary containing ontology information for the specified term, including its children and parents in the hierarchy.
    """

    try:
        result = ensembl_api.get_ontology_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ontology_name(name: str):
    """
    Get ontology by name.
    
    Args:
        name: Ontology term name
    
    Query example: {"name": "reproduction"}
    
    Returns:
        Dictionary containing ontology information for the matched term.
    """

    try:
        result = ensembl_api.get_ontology_name(name=name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Overlap endpoints
@mcp.tool()
async def get_overlap_id(id: str):
    """
    Get features overlapping a region defined by an identifier. Note: This tool is currently non-functional and returns a 400 Bad Request error for valid Ensembl IDs.
    
    Args:
        id: Ensembl stable identifier
    
    Query example: {"id": "ENST00000380152"}
    
    Returns:
        Dictionary containing overlapping features. Returns an error message upon failure.
    """

    try:
        result = ensembl_api.get_overlap_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_overlap_region(features:str, region: str, species: str = "homo_sapiens"):
    """
    Get features overlapping a genomic region. Note: This tool may fail with a 400 Bad Request error for valid queries.
    
    Args:
        features: The type of feature to retrieve. Multiple values are accepted if separated by coma (e.g. 'feature=gene;feature=transcript;'). Enum(band, gene, transcript, cds, exon, repeat, simple, misc, variation, somatic_variation, structural_variation, somatic_structural_variation, constrained, regulatory, motif, mane)
        species: Species name (e.g. 'homo_sapiens' for human)
        region: Genomic region (e.g. 'X:1..1000:1','X:1..1000:-1','X:1..1000')
    
    Query example: {"species": "homo_sapiens", "region": "X:1000000..1000100", "features": "gene"}
    
    Returns:
        Dictionary containing overlapping features. Returns an error message upon failure.
    """

    try:
        result = ensembl_api.get_overlap_region(features=features,species=species, region=region)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_overlap_translation(id: str):
    """
    Get features overlapping a translation.
    
    Args:
        id: Translation stable identifier
    
    Query example: {"id": "ENSP00000265436"}
    
    Returns:
        A list of dictionaries, where each dictionary contains information about a feature
        that overlaps with the genomic region of the specified translation ID.
    """

    try:
        result = ensembl_api.get_overlap_translation(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Phenotype endpoints
@mcp.tool()
async def get_phenotype_region(region: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """
    Retrieve phenotype associations for variants in a genomic region.
    
    Find diseases, traits, and phenotypes associated with genetic variants
    located within a specific genomic region. Useful for exploring disease
    associations in GWAS loci or candidate regions.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        region: Genomic region in format 'chromosome:start..end' 
                (e.g., '9:22125500..22136000', '17:7669000..7676000')
    
    Query example: {"species": "homo_sapiens", "region": "9:22125500..22136000"}
    
    Returns:
        A list of dictionaries containing phenotype annotations for variants in the region, including:
        - Associated diseases and traits
        - Specific variant locations and alleles
        - Source of the association (e.g., ClinVar, GWAS Catalog)
    """

    result = ensembl_api.get_phenotype_region(species=species, region=region, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while fetching phenotype data: {result['error']}"}
    return result

@mcp.tool()
async def get_phenotype_gene(gene: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """
    Retrieve phenotype associations for a specific gene.
    
    Find diseases, traits, and phenotypes associated with a gene of interest.
    These associations come from various sources including literature curation,
    GWAS studies, and clinical databases.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        gene: Gene stable ID or name (e.g., 'ENSG00000139618', 'BRCA2')
        max_length: Maximum length of the response in approximate tokens (default: 8192)
    
    Query example: {"species": "homo_sapiens", "gene": "BRCA2"}
    
    Returns:
        A list of dictionaries containing phenotype annotations for the gene, including:
        - Associated diseases and traits
        - Source of the association (e.g., ClinVar, GWAS Catalog)
        - Study references and citations
        - Variant details for genetic associations
        - Clinical significance where available
    """

    result = ensembl_api.get_phenotype_gene(species=species, gene=gene, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while fetching phenotype data: {result['error']}"}
    return result

@mcp.tool()
async def get_phenotype_accession(accession: str, species: str = "homo_sapiens", max_length: int = DEFAULT_MAX_LENGTH):
    """
    Retrieve genomic features associated with a specific phenotype ontology term.
    
    Find genes and variants linked to a specific disease or trait identified by
    an ontology accession (e.g., from the Human Phenotype Ontology or Experimental
    Factor Ontology).
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        accession: Phenotype ontology accession (e.g., 'HP:0001250' for seizure)
        max_length: Maximum length of the response in approximate tokens (default: 8192)
    
    Query example: {"species": "homo_sapiens", "accession": "HP:0001250"}
    
    Returns:
        A list of dictionaries containing phenotype annotations for the gene, including:
        - Associated diseases and traits
        - Source of the association (e.g., ClinVar, GWAS Catalog)
        - Study references and citations
        - Variant details for genetic associations
    """

    result = ensembl_api.get_phenotype_accession(species=species, accession=accession, max_length=max_length)
    if "error" in result:
        return {"error": f"An error occurred while fetching phenotype data: {result['error']}"}
    return result

# Sequence endpoints
@mcp.tool()
async def get_sequence_id(id: str):
    """
    Retrieve sequence associated with an Ensembl identifier.
    
    Get the nucleotide sequence for a gene or transcript, or the amino acid sequence for a protein.
    Useful for analyzing gene structure, transcript variants, or protein domains.
    
    Args:
        id: Ensembl stable identifier (e.g., 'ENSG00000139618' for BRCA2 gene DNA,
            'ENST00000380152' for transcript sequence, or 'ENSP00000369497' for protein sequence)
    
    Query example: {"id": "ENST00000380152"}
    
    Returns:
        Dictionary containing the sequence (nucleotide or amino acid) and metadata about
        the entity, including length, sequence type, and coordinate information.
    """

    try:
        result = ensembl_api.get_sequence_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# VEP endpoints
@mcp.tool()
async def get_vep_id(id: str, species: str = "homo_sapiens"):
    """
    Predict the functional effects of variants using Variant Effect Predictor (VEP) with variant identifier.
    
    Retrieves comprehensive variant annotation using known variant IDs (e.g., dbSNP rs identifiers).
    Provides molecular consequences, population frequencies, and pathogenicity predictions.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        id: Variant identifier (e.g., 'rs6025' for Factor V Leiden, 'rs429358' for APOE variant)
    
    Query example: {"species": "homo_sapiens", "id": "rs6025"}
    
    Returns:
        Dictionary containing detailed variant effect predictions, including:
        - Affected genes and transcripts
        - Effect on protein sequence (missense, nonsense, etc.)
        - SIFT and PolyPhen pathogenicity scores
        - Conservation scores
        - Allele frequencies in population databases
        - Regulatory feature annotations
        - Clinical significance annotations
    """

    try:
        result = ensembl_api.get_vep_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_vep_region(region: str, allele: str, species: str = "homo_sapiens"):
    """
    Predict the functional effects of variants using Variant Effect Predictor (VEP) with genomic coordinates.
    
    Analyzes variants specified by chromosome location and alternate allele.
    Particularly useful for novel variants or those without established identifiers.

    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        region: Genomic region in format 'chromosome:position' or 'chromosome:start-end'
                (e.g., '9:22125503', '1:230710048-230710048')
        allele: The variant allele sequence (alternate allele) that replaces the reference sequence

    Returns:
        Dictionary containing detailed variant effect predictions, including:
        - Affected genes and transcripts
        - Effect on protein sequence (missense, nonsense, etc.)
        - SIFT and PolyPhen pathogenicity scores
        - Conservation scores
        - Allele frequencies in population databases
        - Regulatory feature annotations
        - Clinical significance annotations
    """
    try:
        result = ensembl_api.get_vep_region(species=species, region=region, allele=allele)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Variation endpoints
@mcp.tool()
async def get_variation(id: str, species: str = "homo_sapiens"):
    """
    Retrieve detailed information about a genetic variant by its identifier.
    
    Provides comprehensive data about a known genetic variant, including its
    genomic location, alleles, frequency in populations, phenotype associations,
    and links to external databases.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        id: Variant identifier (e.g., 'rs6025' for Factor V Leiden, 'rs429358' for APOE variant)
    
    Query example: {"species": "homo_sapiens", "id": "rs6025"}
    
    Returns:
        Dictionary containing detailed variant information including:
        - Genomic location and alleles
        - Population frequencies across different populations
        - Clinical significance and phenotype associations
        - Consequence predictions for transcripts
        - Citations and references
        - External database links (dbSNP, ClinVar, etc.)
    """

    try:
        result = ensembl_api.get_variation(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_variant_recoder(id: str, species: str = "homo_sapiens"):
    """
    Translate between different variant nomenclature systems and representations.
    
    Convert variant identifiers between different formats (e.g., rsID, HGVS notation,
    genomic coordinates). Useful for integrating variant data from different sources
    or analysis tools.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        id: Variant identifier in any supported format (e.g., 'rs6025',
            'ENST00000367640.3:c.1601G>A', '1:g.169519049G>T')
    
    Query example: {"species": "homo_sapiens", "id": "rs6025"}
    
    Returns:
        Dictionary containing the variant represented in various nomenclature systems:
        - dbSNP rsIDs
        - HGVS notations (genomic, transcript, protein)
        - Genomic coordinates in VCF format
        - SPDI notation (Sequence Position Deletion Insertion)
    """

    try:
        result = ensembl_api.get_variant_recoder(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Additional Information endpoints
@mcp.tool()
async def get_info_data():
    """
    Get data release information.
    
    Query example: {}

    Returns:
        Dictionary containing data release information.
    """
    try:
        result = ensembl_api.get_info_data()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_eg_version():
    """
    Get Ensembl Genomes version.
    
    Args:
    
    Query example: {}
    
    Returns:
        Dictionary containing version information.
    """

    try:
        result = ensembl_api.get_info_eg_version()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_divisions():
    """
    Get Ensembl divisions.
    
    Args:
    
    Query example: {}
    
    Returns:
        A list containing the names of the main Ensembl divisions.
    """

    try:
        result = ensembl_api.get_info_divisions()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes(genome_name: str):
    """
    Find information about a given genome.
    
    Args:
        genome_name: Name of the genome (e.g., 'homo_sapiens')
    
    Query example: {"genome_name": "homo_sapiens"}
    
    Returns:
        A dictionary containing detailed genome information.
    """

    try:
        result = ensembl_api.get_info_genomes(genome_name=genome_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_accession(accession: str):
    """
    Find information about genomes containing a specified INSDC accession. Note: The underlying data is sparse, and many valid accessions may result in a null return.
    
    Args:
        accession: INSDC accession (e.g., 'GCA_000001635.9').
    
    Query example: {"accession": "GCA_000001635.9"}
    
    Returns:
        A dictionary containing genome information for the specified accession. Returns null if no information is found.
    """

    try:
        result = ensembl_api.get_info_genomes_accession(accession=accession)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_assembly(assembly_id: str):
    """
    Find information about a genome with a specified assembly. Note: This tool may fail with a 400 Bad Request error for valid assembly IDs.
    
    Args:
        assembly_id: Assembly identifier
    
    Query example: {"assembly_id": "71511"}
    
    Returns:
        Dictionary containing genome information. Returns an error message upon failure.
    """

    try:
        result = ensembl_api.get_info_genomes_assembly(assembly_id=assembly_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_division(division_name: str):
    """
    Find information about all genomes in a given division.
    
    Args:
        division_name: Division name (e.g., 'EnsemblVertebrates')
    
    Query example: {"division_name": "EnsemblVertebrates"}
    
    Returns:
        A list of dictionaries, where each dictionary contains information about a genome in the specified division.
    """

    try:
        result = ensembl_api.get_info_genomes_division(division_name=division_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_genomes_taxonomy(taxon_name: str):
    """
    Find information about all genomes beneath a given node of the taxonomy.
    
    Args:
        taxon_name: Taxon name (e.g., 'Primates')
    
    Query example: {"taxon_name": "Primates"}
    
    Returns:
        A list of JSON strings, where each string is a dictionary containing genome information for a species within the specified taxon.
    """

    try:
        result = ensembl_api.get_info_genomes_taxonomy(taxon_name=taxon_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_ping():
    """
    Checks if the service is alive.
    
    Args:
    
    Query example: {}
    
    Returns:
        Dictionary containing ping status (1 indicates alive).
    """

    try:
        result = ensembl_api.get_info_ping()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_rest():
    """
    Shows the current version of the Ensembl REST API.
    
    Args:
    
    Query example: {}
    
    Returns:
        Dictionary containing REST API version information.
    """

    try:
        result = ensembl_api.get_info_rest()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_software():
    """
    Shows the current version of the Ensembl API used by the REST server.
    
    Args:
    
    Query example: {}
    
    Returns:
        Dictionary containing software version information.
    """

    try:
        result = ensembl_api.get_info_software()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_species():
    """
    List all available species in the Ensembl database.
    
    Provides a comprehensive catalog of all organisms available in Ensembl,
    including their scientific names, common names, and assembly information.
    Useful for discovery and exploration of available genomic data.
    
    Args:
    
    Query example: {}
    
    Returns:
        A list of dictionaries, where each dictionary contains information about an available species.
    """

    try:
        result = ensembl_api.get_info_species()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_variation(species: str):
    """
    List all variation data sources used for a species in Ensembl.
    
    Provides information about the databases, studies, and projects that contributed
    variation data (SNPs, indels, structural variants) to Ensembl for a species.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
    
    Query example: {"species": "homo_sapiens"}
    
    Returns:
        A list of dictionaries, where each dictionary contains information about a variation data source for the species.
    """

    try:
        result = ensembl_api.get_info_variation(species=species)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_variation_consequence_types():
    """
    Lists all variant consequence types used by Ensembl.
    
    Args:
    
    Query example: {}
    
    Returns:
        A list of JSON strings, where each string is a dictionary containing information about a variant consequence type.
    """

    try:
        result = ensembl_api.get_info_variation_consequence_types()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_variation_populations(species: str, population_name: str = None):
    """
    List all variation populations for a species, or list all individuals in a specific population.
    
    Args:
        species: Species name (e.g., 'homo_sapiens' for human).
        population_name: Optional population name to get individuals. If not provided, all populations for the species are returned.
    
    Query example for all populations: {"species": "homo_sapiens"}
    Query example for individuals in a population: {"species": "homo_sapiens", "population_name": "1000GENOMES:phase_3:ACB"}
    
    Returns:
        A list of dictionaries containing population information, or a dictionary containing individual information for a specific population.
    """

    try:
        result = ensembl_api.get_info_variation_populations(species=species, population_name=population_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Linkage Disequilibrium endpoints
@mcp.tool()
async def get_ld(species: str, id: str, population_name: str):
    """
    Computes and returns LD values between the given variant and all other variants in a window.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        id: Variant identifier
        population_name: Population name
    
    Query example: {"species": "homo_sapiens", "id": "rs6025", "population_name": "1000GENOMES:phase_3:EUR"}
    
    Returns:
        A list of JSON strings, where each string is a dictionary containing LD values (d_prime, r2)
        between the query variant and another nearby variant.
    """

    try:
        result = ensembl_api.get_ld(species=species, id=id, population_name=population_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ld_pairwise(species: str, id1: str, id2: str):
    """
    Computes and returns LD values between the given variants.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        id1: First variant identifier
        id2: Second variant identifier
    
    Query example: {"species": "homo_sapiens", "id1": "rs6025", "id2": "rs2213868"}
    
    Returns:
        A list of JSON strings, where each string is a dictionary containing LD values
        for the pair of variants in a specific population.
    """

    try:
        result = ensembl_api.get_ld_pairwise(species=species, id1=id1, id2=id2)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ld_region(species: str, region: str, population_name: str):
    """
    Computes and returns LD values between all pairs of variants in the defined region.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        region: Genomic region
        population_name: Population name
    
    Query example: {"species": "homo_sapiens", "region": "1:169549800-169549900", "population_name": "1000GENOMES:phase_3:EUR"}
    
    Returns:
        A list of JSON strings, where each string is a dictionary containing LD values
        for a pair of variants within the specified region and population. May return
        an empty list if no variant pairs with LD data are found in the region.
    """

    try:
        result = ensembl_api.get_ld_region(species=species, region=region, population_name=population_name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Lookup endpoints
@mcp.tool()
async def get_lookup_id(id: str):
    """
    Look up details for any Ensembl stable identifier.
    
    Retrieve comprehensive information about any Ensembl entity (gene, transcript, protein, etc.)
    using its stable identifier.
    
    Args:
        id: Ensembl stable identifier (e.g., 'ENSG00000139618' for human BRCA2 gene,
            'ENST00000380152' for a transcript, or 'ENSP00000369497' for a protein)
    
    Query example: {"id": "ENSG00000139618"}
    
    Returns:
        Dictionary containing detailed information about the entity, including its type,
        location, relationships to other entities, and cross-references.
    """

    try:
        result = ensembl_api.get_lookup_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_lookup_id(ids: list[str]):
    """
    
    Look up details for multiple Ensembl stable identifiers in a single request.
    
    Batch retrieval of information for multiple Ensembl entities (genes, transcripts, proteins, etc.).
    
    Args:
        ids: List of Ensembl stable identifiers (e.g., ['ENSG00000139618', 'ENSG00000141510']
            for human BRCA2 and TP53 genes)
    
    Returns:
        Dictionary mapping each input ID to its corresponding entity information.
        Identifiers that are not found will be excluded from the results.
    
    Query example: {"ids": ["ENSG00000157764", "ENSG00000248378"]}
    """

    try:
        result = ensembl_api.post_lookup_id(ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_lookup_symbol(symbols: list[str], species: str = "homo_sapiens"):
    """
    
    Look up multiple gene symbols in a single request.
    
    Batch retrieval of Ensembl gene information for multiple external gene symbols.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        symbols: List of official gene symbols (e.g., ['BRCA2', 'TP53', 'APOE'])
    
    Returns:
        Dictionary mapping each input symbol to its corresponding gene information.
        Symbols that are not found will be excluded from the results.
    
    Query example: {"species": "homo_sapiens", "symbols": ["BRCA2"]}
    """

    try:
        result = ensembl_api.post_lookup_symbol(species=species, symbols=symbols)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Mapping endpoints
@mcp.tool()
async def get_map(asm_one: str, region: str, asm_two: str, species: str = "homo_sapiens"):
    """
    Map coordinates between assemblies.

    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        asm_one: Source assembly
        region: Genomic region in source assembly
        asm_two: Target assembly

    Returns:
        Dictionary containing mapped coordinates.
    """
    try:
        result = ensembl_api.get_map(species=species, asm_one=asm_one, region=region, asm_two=asm_two)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Ontology endpoints
@mcp.tool()
async def get_ontology_ancestors_chart(id: str):
    """
    
    Reconstruct the entire ancestry of a term from is_a and part_of relationships.
    
    Args:
        id: Ontology term ID
    
    Returns:
        Dictionary containing ancestor chart information.
    
    Query example: {"id": "GO:0005667"}
    """

    try:
        result = ensembl_api.get_ontology_ancestors_chart(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Taxonomy endpoints
@mcp.tool()
async def get_taxonomy_classification(id: str):
    """
    
    Return the taxonomic classification of a taxon node.
    
    Args:
        id: Taxonomy ID
    
    Returns:
        Dictionary containing taxonomic classification.
    
    Query example: {"id": "9606"}
    """

    try:
        result = ensembl_api.get_taxonomy_classification(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_taxonomy_id(id: str):
    """
    
    Search for a taxonomic term by its identifier or name
    
    Args:
        id: Taxonomy ID or name
    
    Returns:
        Dictionary containing taxonomy information.
    
    Query example: {"id": "9606"}
    """

    try:
        result = ensembl_api.get_taxonomy_id(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_taxonomy_name(name: str):
    """
    
    Search for a taxonomic id by a non-scientific name.
    
    Args:
        name: Non-scientific name
    
    Returns:
        Dictionary containing taxonomy information.
    
    Query example: {"name": "Homo sapiens"}
    """

    try:
        result = ensembl_api.get_taxonomy_name(name=name)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Regulation endpoints
@mcp.tool()
async def get_species_binding_matrix(binding_matrix_stable_id: str, species: str = "homo_sapiens"):
    """
    
    Return the specified binding matrix
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        binding_matrix_stable_id: Binding matrix stable ID
    
    Returns:
        Dictionary containing binding matrix information.
    
    Query example: {"species": "homo_sapiens", "binding_matrix_stable_id": "ENSPFM0001"}
    """

    try:
        result = ensembl_api.get_species_binding_matrix(species=species, binding_matrix_stable_id=binding_matrix_stable_id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Sequence endpoints
@mcp.tool()
async def post_sequence_id(ids: list[str]):
    """
    
    Request multiple types of sequence by a stable identifier list.
    
    Efficiently fetch sequences for multiple genes, transcripts, or proteins in a single request.
    
    Args:
        ids: List of Ensembl stable identifiers (e.g., ['ENSG00000139618', 'ENSG00000141510'])
    
    Returns:
        Dictionary mapping each identifier to its corresponding sequence and metadata.
    
    Query example: {"ids": ["ENSG00000157764", "ENSG00000248378"]}
    """

    try:
        result = ensembl_api.post_sequence_id(ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_sequence_region(regions: list[dict], species: str = "homo_sapiens"):
    """
    Get sequences by multiple regions.

    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        regions: List of genomic regions

    Returns:
        Dictionary containing sequences.
    """
    try:
        result = ensembl_api.post_sequence_region(species=species, regions=regions)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Transcript Haplotypes endpoints
@mcp.tool()
async def get_transcript_haplotypes(id: str, species: str = "homo_sapiens"):
    """
    
    Computes observed transcript haplotype sequences based on phased genotype data.
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        id: Transcript ID
    
    Returns:
        Dictionary containing transcript haplotype information.
    
    Query example: {"species": "homo_sapiens", "id": "ENST00000288602"}
    """

    try:
        result = ensembl_api.get_transcript_haplotypes(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# VEP endpoints
@mcp.tool()
async def post_vep_hgvs(hgvs_notations: list[str], species: str = "homo_sapiens"):
    """
    
    Batch predict the functional effects of multiple variants using VEP with HGVS notation.
    
    Efficiently analyze multiple variants in a single request using the Variant Effect Predictor.
    Ideal for analyzing sets of variants from sequencing data or genetic studies.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        hgvs_notations: List of variants in HGVS notation format
                        (e.g., ['ENST00000269305.4:c.2309C>T', 'NM_000059.3:c.274G>A'])
    
    Returns:
        List of dictionaries, each containing detailed variant effect predictions for one input variant.
    
    Query example: {"species": "human", "hgvs_notations": ["ENST00000366667:c.803C>T", "9:g.22125504G>C"]}
    """

    try:
        result = ensembl_api.post_vep_hgvs(species=species, hgvs_notations=hgvs_notations)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_vep_id(ids: list[str], species: str = "homo_sapiens"):
    """
    
    Batch predict the functional effects of multiple variants using VEP with variant identifiers.
    
    Efficiently analyze multiple known variants in a single request using the Variant Effect Predictor.
    Ideal for analyzing sets of common variants or SNP panel data.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        ids: List of variant identifiers (e.g., ['rs6025', 'rs429358'])
    
    Returns:
        List of dictionaries, each containing detailed variant effect predictions for one input variant.
    
    Query example: {"species": "human", "ids": ["rs56116432", "COSM476", "__VAR(sv_id)__"]}
    """

    try:
        result = ensembl_api.post_vep_id(species=species, ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_vep_region(variants: list[dict], species: str = "homo_sapiens"):
    """
    Get variant effect predictions by multiple regions.

    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        variants: List of variant definitions

    Returns:
        Dictionary containing variant effect predictions.
    """
    try:
        result = ensembl_api.post_vep_region(species=species, variants=variants)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# Variation endpoints
@mcp.tool()
async def post_variant_recoder(ids: list[str], species: str = "homo_sapiens"):
    """
    
    Translate a list of variant identifiers, HGVS notations or genomic SPDI notations to all possible variant IDs, HGVS and genomic SPDI
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        ids: List of variant identifiers
    
    Returns:
        Dictionary containing variant identifier translations.
    
    Query example: {"species": "human", "ids": ["rs56116432", "rs1042779"]}
    """

    try:
        result = ensembl_api.post_variant_recoder(species=species, ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_variation_pmcid(pmcid: str, species: str = "homo_sapiens"):
    """
    
    Fetch variants by publication using PubMed Central reference number (PMCID)
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        pmcid: PubMed Central reference number
    
    Returns:
        Dictionary containing variation information.
    
    Query example: {"species": "human", "pmcid": "PMC5002951"}
    """

    try:
        result = ensembl_api.get_variation_pmcid(species=species, pmcid=pmcid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_variation_pmid(pmid: str, species: str = "homo_sapiens"):
    """
    
    Fetch variants by publication using PubMed reference number (PMID)
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        pmid: PubMed reference number
    
    Returns:
        Dictionary containing variation information.
    
    Query example: {"species": "human", "pmid": "26318936"}
    """

    try:
        result = ensembl_api.get_variation_pmid(species=species, pmid=pmid)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_variation(ids: list[str], species: str = "homo_sapiens"):
    """
    
    Uses a list of variant identifiers (e.g. rsID) to return the variation features including optional genotype, phenotype and population data
    
    Args:
        species: Species name (e.g. 'homo_sapiens' for human)
        ids: List of variation identifiers
    
    Returns:
        Dictionary containing variation information.
    
    Query example: {"species": "human", "ids": ["rs56116432", "COSM476", "__VAR(sv_id)__"]}
    """

    try:
        result = ensembl_api.post_variation(species=species, ids=ids)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

# GA4GH endpoints
@mcp.tool()
async def get_ga4gh_beacon():
    """
    
    Get Beacon information.
    
    Returns:
        Dictionary containing Beacon information.
    
    Args:None
    
    Query example:{}
    """

    try:
        result = ensembl_api.get_ga4gh_beacon()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_beacon_query(params: dict):
    """
    Query Beacon.

    Args:
        params: Query parameters

    Returns:
        Dictionary containing Beacon response.
    """
    try:
        result = ensembl_api.get_ga4gh_beacon_query(params=params)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_beacon_query(data: dict):
    """
    Query Beacon with POST.

    Args:
        data: Query data

    Returns:
        Dictionary containing Beacon response.
    """
    try:
        result = ensembl_api.post_ga4gh_beacon_query(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_features(id: str):
    """
    Get GA4GH features by ID.

    Args:
        id: Feature identifier

    Returns:
        Dictionary containing feature information.
    """
    try:
        result = ensembl_api.get_ga4gh_features(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_features_search(data: dict):
    """
    
    Get a list of sequence annotation features in GA4GH format
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing feature information.
    
    Query example: {"data": {"parentId": "ENST00000408937.7", "pageSize": 2, "featureSetId": "", "featureTypes": ["cds"], "start": 197859, "end": 220023, "referenceName": "X"}}
    """

    try:
        result = ensembl_api.post_ga4gh_features_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_callsets_search(data: dict):
    """
    
    Search GA4GH callsets.
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing callset information.
    
    Query example: {"data": {"variantSetId": 1, "pageSize": 3, "name": "HG00099"}}
    """

    try:
        result = ensembl_api.post_ga4gh_callsets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_callsets(id: str):
    """
    
    Get the GA4GH record for a specific CallSet given its identifier
    
    Args:
        id: Callset identifier
    
    Returns:
        Dictionary containing callset information.
    
    Query example: {"id": "1:NA19777"}
    """

    try:
        result = ensembl_api.get_ga4gh_callsets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_datasets_search(data: dict):
    """
    
    Get a list of datasets in GA4GH format
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing dataset information.
    
    Query example: {"data": {}}
    """

    try:
        result = ensembl_api.post_ga4gh_datasets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_datasets(id: str):
    """
    
    Get the GA4GH record for a specific dataset given its identifier
    
    Args:
        id: Dataset identifier
    
    Returns:
        Dictionary containing dataset information.
    
    Query example: {"id": "6e340c4d1e333c7a676b1710d2e3953c"}
    """

    try:
        result = ensembl_api.get_ga4gh_datasets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_featuresets_search(data: dict):
    """
    
    Search GA4GH feature sets.
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing feature set information.
    
    Query example: {"data": {"datasetId": "Ensembl", "pageToken": "", "pageSize": 2}}
    """

    try:
        result = ensembl_api.post_ga4gh_featuresets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_featuresets(id: str):
    """
    
    Return the GA4GH record for a specific featureSet given its identifier
    
    Args:
        id: Feature set identifier
    
    Returns:
        Dictionary containing feature set information.
    
    Query example: {"id": "Ensembl.114.GRCh38"}
    """

    try:
        result = ensembl_api.get_ga4gh_featuresets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_variants(id: str):
    """
    
    Get GA4GH variant by ID.
    
    Args:
        id: Variant identifier
    
    Returns:
        Dictionary containing variant information.
    
    Query example: {"id": "1:rs1333049"}
    """

    try:
        result = ensembl_api.get_ga4gh_variants(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variantannotations_search(data: dict):
    """
    
    Return variant annotation information in GA4GH format for a region on a reference sequence
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing variant annotation information.
    
    Query example: {"data": {"pageSize": 2, "variantAnnotationSetId": "Ensembl", "referenceId": "9489ae7581e14efcad134f02afafe26c", "start": 25221400, "end": 25221500}}
    """

    try:
        result = ensembl_api.post_ga4gh_variantannotations_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variants_search(data: dict):
    """
    
    Return variant call information in GA4GH format for a region on a reference sequence
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing variant information.
    
    Query example: {"data": {"variantSetId": 1, "callSetIds": ["1:NA19777", "1:HG01242", "1:HG01142"], "referenceName": 22, "start": 17190024, "end": 17671934, "pageToken": "", "pageSize": 3}}
    """

    try:
        result = ensembl_api.post_ga4gh_variants_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variantsets_search(data: dict):
    """
    
    Search GA4GH variant sets.
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing variant set information.
    
    Query example: {"data": {"datasetId": "6e340c4d1e333c7a676b1710d2e3953c", "pageToken": "", "pageSize": 2}}
    """

    try:
        result = ensembl_api.post_ga4gh_variantsets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_variantsets(id: str):
    """
    
    Return the GA4GH record for a specific VariantSet given its identifier
    
    Args:
        id: Variant set identifier
    
    Returns:
        Dictionary containing variant set information.
    
    Query example: {"id": "1"}
    """

    try:
        result = ensembl_api.get_ga4gh_variantsets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_references_search(data: dict):
    """
    
    Return a list of reference sequences in GA4GH format
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing reference information.
    
    Args:
        data: Data (object)
    
    Query example: {"data": {"referenceSetId": "GRCh38", "pageSize": 10}}
    """

    try:
        result = ensembl_api.post_ga4gh_references_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_references(id: str):
    """
    
    Return data for a specific reference in GA4GH format by id
    
    Args:
        id: Reference identifier
    
    Returns:
        Dictionary containing reference information.
        
    Query example: {"id": "9489ae7581e14efcad134f02afafe26c"}
    """

    try:
        result = ensembl_api.get_ga4gh_references(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_referencesets_search(data: dict):
    """
    
    Search GA4GH reference sets.
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing following fields:
        referenceSets:Contains all available reference genome collections(Array)
        nextPageToken:paging marker
    
    Args:
        data: Data (object)
    
    Query example: {"data": {}}
    """

    try:
        result = ensembl_api.post_ga4gh_referencesets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_referencesets(id: str):
    """
    
    Search data for a specific reference set in GA4GH format by ID
    
    Args:
        id: Reference set identifier
    
    Returns:
        Dictionary containing following fields:
        id:Unique identifiers (short names) for genomes
        name:Human-readable name, usually the same as id
        assemblyId:Official Genome Assembly ID
        ncbiTaxonId:NCBI Species ID
        description:Full name of the genome description
    
    Args:
        id: Id (string)
    
    Query example: {"id": "GRCh38", "sourceURI": null, "assemblyId": "GRCh38", "isDerived": "true", "ncbiTaxonId": "9606", "sourceAccessions": ["GCA_000001405.18"], "description": "Homo sapiens GRCh38", "name": "GRCh38", "md5checksum": "4c30331c23188932dba64cb1845d18f5"}
    """

    try:
        result = ensembl_api.get_ga4gh_referencesets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def post_ga4gh_variantannotationsets_search(data: dict):
    """
    
    Return a list of annotation sets in GA4GH format
    
    Args:
        data: Search parameters
    
    Returns:
        Dictionary containing variant annotation set information.
    
    Args:
        data: Data (object)
    
    Query example: {"data": {"variantSetId": "Ensembl"}}
    """

    try:
        result = ensembl_api.post_ga4gh_variantannotationsets_search(data=data)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_ga4gh_variantannotationsets(id: str):
    """
      
    Return meta data for a specific annotation set in GA4GH format by ID
    
      Args:
          id: Variant annotation set identifier
    
      Returns:
          Dictionary containing variant annotation set information.
    
      Query example: {"id": "Ensembl"}
    """

    try:
        result = ensembl_api.get_ga4gh_variantannotationsets(id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_genetree_member_id(id: str, species: str = "homo_sapiens"):
    """
    
    Retrieve the gene tree containing a gene identified by its Ensembl ID.Find the phylogenetic tree showing evolutionary relationships for a gene of interest,
    identified using its Ensembl stable identifier. Useful for understanding gene evolution
    when you have the specific gene ID.
    
    Args:
        species: Species name in snake_case format (e.g., 'homo_sapiens' for human)
        id: Ensembl gene, transcript, or translation stable identifier
            (e.g., 'ENSG00000139618' for human BRCA2 gene)
    
    Returns:
        Dictionary containing gene tree information in a nested structure, including:
        - Taxonomy and sequence relationships
        - Branch lengths representing evolutionary distance
        - Bootstrap values indicating tree confidence
        - Sequence alignments used to build the tree
        - Member genes from different species
    
    Query example: {"species": "human", "id": "ENSG00000167664"}
    """

    try:
        result = ensembl_api.get_genetree_member_id(species=species, id=id)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_biotypes_groups(group: str, object_type: str):
    """
    
     With :group argument provided, list the properties of biotypes within that group. Object type (gene or transcript) can be provided for filtering.
    
    Args:
        group: Biotype group
        object_type: Object type (gene or transcript)
    
    Returns:
        Dictionary containing following fields:
        object_type:The type of object that represents this biotype
        biotype_group:High-level groupings of organism types indicating functional categories of genes (e.g., coding, non-coding, pseudogenes, etc.)
        name:Ensembl internal name
        so_term:Sequence Ontology (SO) Standard term for the biological functional description of genes/transcripts.
        so_acc:Corresponds to the unique identifier of so_term in the sequence ontology (Accession)
        
    
    Query example: {"group": "coding", "object_type": "gene"}
    """

    try:
        result = ensembl_api.get_info_biotypes_groups(group=group, object_type=object_type)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_biotypes_name(name: str, object_type: str):
    """
    
    List the properties of biotypes with a given name. Object type (gene or transcript) can be provided for filtering.
    
    Args:
        name: Biotype name
        object_type: Object type (gene or transcript)
    
    Returns:
        Dictionary containing following fields:
        object_type:The type of object that represents this biotype
        biotype_group:High-level groupings of organism types indicating functional categories of genes (e.g., coding, non-coding, pseudogenes, etc.)
        so_term:Sequence Ontology (SO) Standard term for the biological functional description of genes/transcripts.
        so_acc:Corresponds to the unique identifier of so_term in the sequence ontology (Accession)
        name:Abbreviations for biological types, consistent with the nomenclature used within Ensembl
        
    Query example: {"name": "protein_coding", "object_type": "gene"}
    """

    try:
        result = ensembl_api.get_info_biotypes_name(name=name, object_type=object_type)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_compara_species_sets(method: str):
    """
    
    List all collections of species analysed with the specified compara method.
    
    Args:
        method: Comparative analysis method
    
    Returns:
        Dictionary containing species set information.
    
    Query example: {"method": "EPO"}
    """

    try:
        result = ensembl_api.get_info_compara_species_sets(method=method)
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.tool()
async def get_info_comparas():
    """
    
    Get all available comparative genomics databases and their data release.
    
    Args:None
    
    Query example:{}
    
    Returns:
        Dictionary containing following fields:
            release: the version or release number of the Ensembl Compara database 
            name:Names of subgroups of species groups or comparative genomic analyses in the database
    """

    try:
        result = ensembl_api.get_info_comparas()
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    return result

@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    prompt = """You have access to tools for querying the Ensembl REST API.
    Use these tools to get information about genes, sequences, variants, and more.
    The API provides access to genomic data across multiple species.
    For species names, use the format 'homo_sapiens' for human, 'mus_musculus' for mouse, etc.
    For regions, use the format 'chromosome:start..end' (e.g. 'X:1000000..1000100').
    For variants, use proper HGVS notation (e.g. 'ENST00000003084:c.1431_1433delTTC').
    """
    return prompt