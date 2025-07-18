from mcp.server.fastmcp import FastMCP

from tools.ucsc.ucsc_api import UCSCAPI


mcp = FastMCP(
    "ucsc_mcp",
    stateless_http=True,
)
ucsc_api = UCSCAPI()

@mcp.tool()
async def list_genomes():
    """
    Get all supported genome assemblies from UCSC Genome Browser.
    
    Args:
    
    Query example: {}
    
    Returns:
        Dictionary containing all supported genome assemblies from UCSC Genome Browser, with metadata (downloadTime, dataTime) and detailed genome info.
    """

    try:
        return ucsc_api.list_genomes()
    except Exception as e:
        return {"error": f"Failed to list genomes: {str(e)}"}

@mcp.tool()
async def list_tracks(genome: str):
    """
    List all tracks for a specific genome assembly.
    
    Args:
        genome: Genome assembly name (e.g., 'hg38') (string)
    
    Query example: {"genome": "hg38"}
    
    Returns:
        Dictionary containing all tracks for the specified genome.
    """

    try:
        return ucsc_api.list_tracks(genome)
    except Exception as e:
        return {"error": f"Failed to list tracks: {str(e)}"}

@mcp.tool()
async def list_hub_tracks(hub_url: str, genome: str):
    """
    List all tracks in a specific track hub for a genome.
    
    Args:
        hub_url: URL of the track hub (string)
        genome: Genome assembly name (string)
    
    Query example: {
        "hub_url": "http://hgdownload.soe.ucsc.edu/hubs/GCA/009/914/755/GCA_009914755.4/hub.txt",
        "genome": "hg38"
    }
    
    Returns:
        Dictionary containing tracks in the hub
    """

    try:
        return ucsc_api.list_hub_tracks(hub_url, genome)
    except Exception as e:
        return {"error": f"Failed to list hub tracks: {str(e)}"}

@mcp.tool()
async def list_chromosomes(genome: str):
    """
    List all chromosomes for a genome assembly.
    
    Args:
        genome: Genome assembly name (string)
    
    Query example: {"genome": "hg38"}
    
    Returns:
        A dictionary containing chromosome information, including a 'chromosomes' key mapping chromosome names to their lengths (in base pairs), along with metadata such as download time and chromosome count.
    """

    try:
        return ucsc_api.list_chroms(genome)
    except Exception as e:
        return {"error": f"Failed to list chromosomes: {str(e)}"}

@mcp.tool()
async def list_public_hubs():
    """
    Get list of all public UCSC track hubs.
    
    Args:
        None
    
    Query example: {}
    
    Returns:
        A dictionary containing a list of public UCSC track hubs under the 'publicHubs' key, where each hub is described by fields such as hubUrl, shortLabel, longLabel, registrationTime, dbCount, dbList, and descriptionUrl, along with metadata like download time.
    """

    try:
        return ucsc_api.list_hubs()
    except Exception as e:
        return {"error": f"Failed to list public hubs: {str(e)}"}

@mcp.tool()
async def get_chromosome_sequence(genome: str, chrom: str):
    """
    Get sequence for an entire chromosome.
    
    Args:
        genome: Genome assembly name (string)
        chrom: Chromosome name (e.g., 'chr1') (string)
    
    Query example: {"genome": "hg38", "chrom": "chr1"}
    
    Returns:
        [Return description based on test results]
    """

    try:
        return ucsc_api.get_chrom_sequence(genome, chrom)
    except Exception as e:
        return {"error": f"Failed to get chromosome sequence: {str(e)}"}

@mcp.tool()
async def get_sequence(
    genome: str,
    chrom: str,
    start: int = None,
    end: int = None,
    revcomp: bool = False,
    hub_url: str = None
):
    """
    Get DNA sequence for a genomic region.
    
    Args:
        genome: Genome assembly name (string)
        chrom: Chromosome name (string)
        start: Start position (optional) (integer or null)
        end: End position (optional) (integer or null)
        revcomp: Return reverse complement (default: False) (boolean)
        hub_url: Track hub URL (optional) (string or null)
    
    Query example: {"genome": "hg38", "chrom": "chr1", "start": 1000, "end": 2000, "revcomp": false, "hub_url": null}
    
    Returns:
        A dictionary containing the DNA sequence for the specified genomic region under the 'dna' key, along with metadata such as genome, chromosome, start, end, and download time. The sequence may contain 'N' for unknown or masked bases.
    """

    try:
        return ucsc_api.get_sequence(genome, chrom, start, end, revcomp, hub_url)
    except Exception as e:
        return {"error": f"Failed to get sequence: {str(e)}"}

@mcp.tool()
async def get_track_data(
    genome: str,
    track: str,
    chrom: str = None,
    start: int = None,
    end: int = None,
    max_items: int = None
):
    """
    Get data from a specific track for a genomic region.
    
    Args:
        genome: Genome assembly name (string)
        track: Track name (string)
        chrom: Chromosome name (string or null)
        start: Start position (integer or null)
        end: End position (integer or null)
        max_items: Maximum number of items to return (integer or null)
    
    Query example: {"genome": "hg38", "track": "knownGene", "chrom": "chr1", "start": 100000, "end": 200000, "max_items": 100}
    
    Returns:
        A dictionary containing metadata about the track and a list of gene objects within the specified genomic region. Each gene object includes detailed information such as chromosome coordinates, gene name, strand, exon structure, and various annotations.
    """

    try:
        return ucsc_api.get_track_data(genome, track, chrom, start, end, max_items)
    except Exception as e:
        return {"error": f"Failed to get track data: {str(e)}"}

@mcp.tool()
async def get_cytoband(genome: str, chrom: str = None):
    """
    Get cytoband (chromosome banding) information for a specified genome and chromosome.
    
    Args:
        genome: Genome assembly name (string, required)
        chrom: Chromosome name (string or null, optional, default=null)
    
    Query example: {"genome": "hg38", "chrom": "chr1"}
    
    Returns:
        A dictionary containing cytoband information, including a list of cytoband records for the specified genome and chromosome (if provided). Each record typically includes fields such as chromosome name, start and end positions, band name, and Giemsa stain level.
    """

    try:
        return ucsc_api.get_cytoband(genome, chrom)
    except Exception as e:
        return {"error": f"Failed to get cytoband data: {str(e)}"}

@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    return """You have access to tools for querying the UCSC Genome Browser API.
    Use these tools to retrieve genomic data including sequences, tracks, and annotations.
    Provide genome assembly names (e.g. hg38) when required."""
