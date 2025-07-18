from asyncio import to_thread
from typing import Union
from mcp.server.fastmcp import FastMCP

from tools.ncbi.ncbi_api import NCBIAPI


mcp = FastMCP(
    "ncbi_mcp", 
    stateless_http=True
)
ncbi_api = NCBIAPI()


@mcp.tool()
async def get_gene_metadata_by_gene_name(name: str, species: str = 'human'):
    """
    Get a gene summary by gene symbol. By default, in paged JSON format.
    
    The returned JSON contains detailed gene information including:
    - Basic gene info: gene ID, symbol, description, tax ID, species name
    - Gene type and orientation
    - Reference standards and genomic locations
    - Chromosome location
    - External database IDs (HGNC, Swiss-Prot, Ensembl, OMIM)
    - Gene synonyms
    - Transcript and protein counts
    - Gene summary/description
    - Gene Ontology annotations:
        - Molecular functions (e.g. DNA binding, transcription regulation)
        - Biological processes (e.g. apoptosis, cell cycle regulation)
        - Cellular components (e.g. nucleus, cytoplasm)

    Args:
        name: Gene name/symbol to search for
        species: Species to search within (default: 'human')

    Returns:
        Text response containing gene metadata in JSON format

    Raises:
        requests.exceptions.RequestException: If the API request fails
        
    Query example: {"name": "BRCA1", "species": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_metadata_by_gene_name, name, species)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_ids(gene_ids: Union[int, list[int]]):
    """
    Get gene information by gene IDs.
    
    Args:
        gene_ids: A single Gene ID or a list of Gene IDs
        
    Returns:
        json format response including gene information
        
    Query example: {"gene_ids": [59067, 50615]}
    
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_ids, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_accession(accessions: Union[str, list[str]]):
    """
    Get gene information by accession.
    
    Args:
        accessions: A single Accession or a list of Accessions
        
    Returns:
        json format response including gene information
        
    Query example: {"accessions": ["NP_068575.1", "NP_851564.1"]}
    
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_accession, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_accession_dataset_report(accessions: Union[str, list[str]]):
    """
    Get dataset reports by accession IDs
    
    Args:
        accessions: A single Accession or a list of Accessions
    
    Query example: {"accessions": ["NP_068575.1", "NP_851564.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_accession_dataset_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_accession_product_report(accessions: Union[str, list[str]]):
    """
    Get gene product reports by accession IDs
    
    Args:
        accessions: A single Accession or a list of Accessions
        
    Query example: {"accessions": ["NP_068575.1", "NP_851564.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_accession_product_report, accessions)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_gene_download_summary_by_id(gene_ids: Union[int, list[int]]):
    """Get gene download summary by GeneID
    
    Args:
        gene_ids: A single Gene ID or a list of Gene IDs
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_download_summary_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_links_by_id(gene_ids: Union[int, list[int]]):
    """Get gene links by gene ID
    
    Args:
        gene_ids: A single Gene ID or a list of Gene IDs
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_links_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_dataset_report_by_locus_tag(locus_tags: Union[str, list[str]]):
    """Get gene dataset reports by locus tag
    
    Args:
        locus_tags: A single Locus tag or a list of Locus tags
        
    Query example: {"locus_tags": ["b0001", "b0002"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_dataset_report_by_locus_tag, locus_tags)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_product_report_by_locus_tag(locus_tags: Union[str, list[str]]):
    """Get gene product reports by locus tags
    
    Args:
        locus_tags: A single Locus tag or a list of Locus tags
        
    Query example: {"locus_tags": ["b0001", "b0002"]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_product_report_by_locus_tag, locus_tags)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_symbol_dataset_report(symbols: str, taxon: str = 'human'):
    """Get dataset reports by taxons
    
    Args:
        symbols: Gene symbol
        taxon: Taxon
        
    Query example: {"symbols": "TP53", "taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_symbol_dataset_report, symbols, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_symbol_product_report(symbols: str, taxon: str = 'human'):
    """Get product reports by taxon
    
    Args:
        symbols: Gene symbol
        taxon: Taxon
        
    Query example: {"symbols": "TP53", "taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_symbol_product_report, symbols, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_taxon_dataset_report(taxon: str):
    """Get gene dataset reports by taxonomic identifier
    
    Args:
        taxon: Taxon
        
    Query example: {"taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_taxon_dataset_report, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_taxon_product_report(taxon: str):
    """Get gene product reports by taxonomic identifier
    
    Args:
        taxon: Taxon
        
    Query example: {"taxon": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_taxon_product_report, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_dataset_report_by_id(gene_ids: Union[int, list[int]]):
    """Get gene information by dataset report
    
    Args:
        gene_ids: A single Gene ID or a list of Gene IDs
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_dataset_report_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

# Genome related endpoints
@mcp.tool()
async def get_genome_annotation_report(accession: str):
    """
    Get genome annotation reports by genome accession.
    
    Args:
        accession: Genome accession
        
    Returns:
        json format response including annotation reports
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_annotation_report, accession)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_genome_annotation_summary(accession: str):
    """
    Get genome annotation report summary information.
    
    Args:
        accession: Genome accession
        
    Returns:
        json format response including annotation summary
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_annotation_summary, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_revision_history(accession: str):
    """Get revision history for assembly by accession
    
    Args:
        accession: Genome accession
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_revision_history, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_sequence_reports(accession: str):
    """Get sequence reports by accessions
    
    Args:
        accession: Genome accession
        
    Query example: {"accession": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_sequence_reports, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def check_genome_accessions(accessions: Union[str, list[str]]):
    """Check the validity of genome accessions
    
    Args:
        accessions: Genome accessions
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.check_genome_accessions, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_accession(accessions: Union[str, list[str]]):
    """Get dataset reports by accessions
    
    Args:
        accessions: Genome accessions
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_accession, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_download(accessions: Union[str, list[str]]):
    """Get a genome dataset by accession
    
    Args:
        accessions: Genome accessions
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_download, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_download_summary(accessions: Union[str, list[str]]):
    """Preview genome dataset download
    
    Args:
        accessions: Genome accessions
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_download_summary, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_links(accessions: Union[str, list[str]]):
    """Get assembly links by accessions
    
    Args:
        accessions: Genome accessions
        
    Query example: {"accessions": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_links, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_assembly_name(assembly_names: Union[str, list[str]]):
    """Get dataset reports by assembly name
    
    Args:
        assembly_names: Assembly names
        
    Query example: {"assembly_names": "GCF_000001635.27"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_assembly_name, assembly_names)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_bioproject(bioprojects: Union[str, list[str]]):
    """Get dataset reports by bioproject
    
    Args:
        bioprojects: Bioprojects
        
    Query example: {"bioprojects": ["PRJNA489243", "PRJNA31257"]}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_bioproject, bioprojects)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_biosample(biosample_ids: Union[str, list[str]]):
    """Get dataset reports by biosample id
    
    Args:
        biosample_ids: Biosample IDs
        
    Query example: {"biosample_ids": ["SAMN15960293"]}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_biosample, biosample_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_sequence_assemblies(accession: str):
    """Get assembly accessions for a sequence accession
    
    Args:
        accession: Sequence accession
        
    Query example: {"accession": "NC_000001.11"}
    """
    try:
        return await to_thread(ncbi_api.get_sequence_assemblies, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_taxon(taxons: str):
    """Get dataset reports by taxons
    
    Args:
        taxons: Taxons
        
    Query example: {"taxons": "human"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_taxon, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_dataset_report_by_wgs(wgs_accessions: Union[str, list[str]]):
    """Get dataset reports by wgs accession
    
    Args:
        wgs_accessions: WGS accessions
        
    Query example: {"wgs_accessions": ["JAHLSK02", "JAAKGM02"]}
    """
    try:
        return await to_thread(ncbi_api.get_genome_dataset_report_by_wgs, wgs_accessions)
    except Exception as e:
        return f"Error: {e}"

# Virus related endpoints
@mcp.tool()
async def get_virus_annotation_report(accessions: Union[str, list[str]]):
    """
    Get virus annotation report by accessions.
    
    Args:
        accessions: Virus accessions
        
    Returns:
        json format response including annotation report
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_virus_annotation_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def check_virus_accessions(accessions: Union[str, list[str]]):
    """Check virus accessions validity
    
    Args:
        accessions: Virus accessions
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.check_virus_accessions, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_virus_dataset_report(accessions: Union[str, list[str]]):
    """Get virus dataset report by accessions
    
    Args:
        accessions: Virus accessions
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_virus_dataset_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_virus_genome_download(accessions: Union[str, list[str]]):
    """Download virus genome by accessions
    
    Args:
        accessions: Virus accessions
        
    Query example: {"accessions": ["NC_038294.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_virus_genome_download, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_virus_by_taxon_annotation_report(taxon: str):
    """Get virus annotation report by taxon
    
    Args:
        taxon: Virus taxon
        
    Query example: {"taxon": "SARS-COV-2"}
    """
    try:
        return await to_thread(ncbi_api.get_virus_by_taxon_annotation_report, taxon)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_virus_by_taxon_genome(taxon: str):
    """Get virus genome by taxon
    
    Args:
        taxon: Virus taxon
        
    Query example: {"taxon": "2697049"}
    """
    try:
        return await to_thread(ncbi_api.get_virus_by_taxon_genome, taxon)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_virus_by_taxon_genome_table(taxon: str):
    """Get virus genome table by taxon
    
    Args:
        taxon: Virus taxon
        
    Query example: {"taxon": "2697049"}
    """
    try:
        return await to_thread(ncbi_api.get_virus_by_taxon_genome_table, taxon)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_version():
    """
    Get current version of all services.
    
    Returns:
        json format response including version information
    """
    try:
        return await to_thread(ncbi_api.get_version)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
async def get_taxonomy_related_ids(tax_id: int):
    """Get related taxonomy IDs
    
    Args:
        tax_id: Taxonomy ID
        
    Query example: {"tax_id": 9606}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_related_ids, tax_id)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_download(tax_ids: Union[int, list[int]]):
    """Download taxonomy data
    
    Args:
        tax_ids: Taxonomy IDs
        
    Query example: {"tax_ids": [9606, 9605]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_download, tax_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_links(taxon: str):
    """Get taxonomy links
    
    Args:
        taxon: Taxonomy ID
        
    Query example: {"taxon": "9606"}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_links, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy(taxons: Union[str, list[str]]):
    """
    Get taxonomy information.
    
    Args:
        taxons: Taxonomy IDs
        
    Returns:
        json format response including taxonomy information
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_dataset_report(taxons: Union[str, list[str]]):
    """
    Get taxonomy dataset report.
    
    Args:
        taxons: Taxonomy IDs
        
    Returns:
        json format response including dataset report
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_dataset_report, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_filtered_subtree(taxons: Union[str, list[str]]):
    """Get filtered taxonomy subtree
    
    Args:
        taxons: Taxonomy IDs
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_filtered_subtree, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_name_report(taxons: Union[str, list[str]]):
    """Get taxonomy name report
    
    Args:
        taxons: Taxonomy IDs
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_name_report, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_taxonomy_taxon_suggest(taxon_query: str):
    """Get taxonomy suggestions
    
    Args:
        taxon_query: Taxonomy query
        
    Query example: {"taxon_query": "hum"}
    """
    try:
        return await to_thread(ncbi_api.get_taxonomy_taxon_suggest, taxon_query)
    except Exception as e:
        return f"Error: {e}"

# BioSample endpoint
@mcp.tool()
async def get_biosample_report(accessions: Union[str, list[str]]):
    """
    Get biosample report.
    
    Args:
        accessions: BioSample accessions
        
    Returns:
        json format response including biosample report
        
    Query example: {"accessions": ["SAMN15960293"]}
    """
    try:
        return await to_thread(ncbi_api.get_biosample_report, accessions)
    except Exception as e:
        return f"Error: {e}"

# Organelle related endpoints
@mcp.tool()
async def get_organelle_download(accessions: Union[str, list[str]]):
    """Download organelle data
    
    Args:
        accessions: Organelle accessions
        
    Query example: {"accessions": ["NC_001643.1", "NC_002082.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_organelle_download, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_organelle_dataset_report(accessions: Union[str, list[str]]):
    """
    Get organelle dataset report.
    
    Args:
        accessions: Organelle accessions
        
    Returns:
        json format response including dataset report
        
    Query example: {"accessions": ["NC_001643.1", "NC_002082.1"]}
    """
    try:
        return await to_thread(ncbi_api.get_organelle_dataset_report, accessions)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_organelle_by_taxon_dataset_report(taxons: Union[str, list[str]]):
    """
    Get organelle dataset report by taxon.
    
    Args:
        taxons: Taxonomy IDs
        
    Returns:
        json format response including dataset report
        
    Query example: {"taxons": ["9606", "9605"]}
    """
    try:
        return await to_thread(ncbi_api.get_organelle_by_taxon_dataset_report, taxons)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_product_report_by_id(gene_ids: Union[int, list[int]]):
    """Get gene product report by gene ID
    
    Args:
        gene_ids: Gene IDs
        
    Query example: {"gene_ids": [59067, 50615]}
    """
    try:
        return await to_thread(ncbi_api.get_gene_product_report_by_id, gene_ids)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_orthologs(gene_id: int):
    """Get gene orthologs by gene ID
    
    Args:
        gene_ids: Gene IDs
        
    Query example: {"gene_ids": 59067}
    """
    try:
        return await to_thread(ncbi_api.get_gene_orthologs, gene_id)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_by_taxon(taxon: str):
    """Get gene information by taxon
    
    Args:
        taxon: Taxon
        
    Query example: {"taxon": "9606"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_by_taxon, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_gene_counts_by_taxon(taxon: str):
    """Get gene counts by taxon
    
    Args:
        taxon: Taxon
        
    Query example: {"taxon": "9606"}
    """
    try:
        return await to_thread(ncbi_api.get_gene_counts_by_taxon, taxon)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_chromosome_summary(taxon: str, annotation_name: str):
    """Get chromosome summary by taxon and annotation name
    
    Args:
        taxon: Taxon
        annotation_name: Annotation name
        
    Query example: {"taxon": "9606", "annotation_name": "GCF_028858705.1-RS_2023_03"}
    """
    try:
        return await to_thread(ncbi_api.get_chromosome_summary, taxon, annotation_name)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_genome_by_accession(accession: str):
    """Get genome information by accession
    
    Args:
        accession: Genome accession
        
    Query example: {"accession": "GCF_028858705.1"}
    """
    try:
        return await to_thread(ncbi_api.get_genome_by_accession, accession)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
async def get_prokaryote_gene_dataset_by_refseq_protein_accession(refseq_protein_accession: str):
    """Get a prokaryote gene dataset by RefSeq protein accession
    
    Args:
        refseq_protein_accession: RefSeq protein accession
        
    Query example: {"refseq_protein_accession": "WP_015878339.1"}
    """
    try:
        return await to_thread(ncbi_api.get_prokaryote_gene_dataset_by_refseq_protein_accession, refseq_protein_accession)
    except Exception as e:
        return f"Error: {e}"

