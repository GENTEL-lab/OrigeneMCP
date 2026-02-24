"""
TCGA MCP Server
===============
Provides TCGA gene analysis tools via MCP protocol.
"""

from mcp.server.fastmcp import FastMCP
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

try:
    # When imported as package
    from .tcga_api import TCGA_API
    from .tcga_deg_api import TCGA_DEG_API, APIConfig
    from .tcga_immune_api import TCGA_Immune_API, ImmuneAPIConfig
except ImportError:
    # When running script directly
    from tcga_api import TCGA_API
    from tcga_deg_api import TCGA_DEG_API, APIConfig
    from tcga_immune_api import TCGA_Immune_API, ImmuneAPIConfig


# ==================== Load Config ====================

def load_config() -> dict:
    """Load config from local.conf.toml (priority) or default.conf.toml"""
    root_dir = Path(__file__).parent.parent.parent
    
    # Priority: local.conf.toml > default.conf.toml
    config_paths = [
        root_dir / "local.conf.toml",
        root_dir / "default.conf.toml",
        Path(__file__).parent.parent / "local.conf.toml",
        Path(__file__).parent.parent / "default.conf.toml",
        Path("local.conf.toml"),
        Path("default.conf.toml"),
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            with open(config_path, "rb") as f:
                return tomllib.load(f)
    return {}


config = load_config()


# ==================== Initialize ====================

mcp = FastMCP("tcga_mcp", stateless_http=True)
tcga_api = TCGA_API()

# Initialize DEG API if configured
tcga_deg_api = None
if config.get("tcga_llm_api_key"):
    tcga_deg_api = TCGA_DEG_API(APIConfig(
        llm_api_key=config.get("tcga_llm_api_key", ""),
        llm_api_base=config.get("tcga_llm_api_base", "https://api.openai-proxy.org/v1"),
        output_dir=config.get("tcga_output_dir", "./output")
    ))

# Initialize Immune Correlation API if configured
tcga_immune_api = None
if config.get("tcga_llm_api_key"):
    tcga_immune_api = TCGA_Immune_API(ImmuneAPIConfig(
        llm_api_key=config.get("tcga_llm_api_key", ""),
        llm_api_base=config.get("tcga_llm_api_base", "https://api.openai-proxy.org/v1"),
        data_dir=str(Path(__file__).parent / "data")
    ))


# ==================== Tools ====================

@mcp.tool()
async def get_gene_specific_expression_in_cancer_type(gene: str):
    """
    Analyze the tissue-specific expression pattern of a given gene across different cancer types
    using the Firebrowse API (TCGA mRNASeq). It computes mean expression per cancer (cohort),
    calculates z-score of mean expression, and returns cancer types where the gene is highly
    or lowly expressed.

    Args:
        gene: Gene symbol, such as "TP53", "BRCA1", "EGFR"

    Returns:
        A dictionary with two keys:
        - high_expression_cancers: List of cancer types where the gene is highly expressed (z > 1)
        - low_expression_cancers: List of cancer types where the gene is lowly expressed (z < -1)
        
    Query example: {"gene": "TP53"}
    """
    try:
        result = tcga_api.get_gene_specific_expression_in_cancer_type(gene=gene)
    except Exception as e:
        return [{"error": f"An error occurred while search gene: {str(e)}"}]
    return result


@mcp.tool()
async def tcga_differential_expression_analysis(query: str):
    """
    Perform complete TCGA differential expression analysis from a natural language query.
    
    This tool:
    1. Uses LLM to parse your query and extract cancer type + genes
    2. Downloads real RNA-seq data from GDC/TCGA
    3. Performs Tumor vs Normal differential expression analysis (PyDESeq2)
    4. Generates publication-quality figures (volcano plot, PCA, heatmap, boxplot)
    
    Args:
        query: Natural language question, e.g., "Analyze TP53 and EGFR expression in lung adenocarcinoma"

    Returns:
        Complete analysis results including:
        - parsed_params: Extracted cancer type and genes from your query
        - analysis_summary: Sample counts, DEG statistics
        - results: Target genes stats, top upregulated/downregulated genes
        - figures: Publication-quality visualizations as base64 images
        - llm_summary: Professional summary of findings
        - workflow_steps: Detailed analysis pipeline log

    Notes:
        - Analysis typically takes 2-5 minutes depending on data availability
        - Default uses 15 samples per group (Tumor/Normal)
        - Significance thresholds: FDR < 0.05, |log2FC| > 1
    """
    if tcga_deg_api is None:
        return {"error": "TCGA DEG API not configured. Please set tcga_llm_api_key in default.conf.toml"}
    
    try:
        result = tcga_deg_api.run(query)
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
    return result


@mcp.tool()
async def list_tcga_cancer_types():
    """
    List all supported TCGA cancer types.
    
    Use this when user asks what cancers are available for analysis.
    
    Returns:
        List of cancer types with TCGA ID, English name, and Chinese name.
    """
    if tcga_deg_api is None:
        return {"error": "TCGA DEG API not configured. Please set tcga_llm_api_key in default.conf.toml"}
    
    return tcga_deg_api.get_supported_cancer_types()


@mcp.tool()
async def tcga_immune_correlation_analysis(query: str):
    """
    Analyze correlation between a gene and immune cell infiltration in TCGA data,
    and recommend the most relevant immune cell type.
    
    This tool:
    1. Uses LLM to parse your natural language query and extract gene + cancer type
    2. Downloads gene expression data from UCSC Xena (TCGA)
    3. Loads immune cell infiltration data (CIBERSORT, 22 cell types)
    4. Performs Spearman correlation analysis
    5. Recommends the most relevant immune cell type among T cells, Macrophage, DC, NK cells
    6. Generates professional summary using LLM
    
    Args:
        query: Natural language question, e.g.:
            - "Analyze GPR160 and immune cells in liver cancer, recommend the most relevant immune cell"
            - "Analyze GPR160 correlation with immune cells in liver cancer and recommend the most relevant immune cell"
            - "Is TP53 associated with T cell infiltration in lung adenocarcinoma?"

    Returns:
        Complete analysis results including:
        - parsed_params: Extracted gene and cancer type from your query
        - analysis_info: Sample count, cell types analyzed, method used
        - recommendation: Recommended immune cell type with correlation, p-value, and reason
        - major_immune_cells: Correlation results for T cells, Macrophage, DC, NK cells
        - top_correlations: Top positive and negative correlations
        - summary: Professional analysis summary

    Example queries:
        - "Analyze GPR160 and immune cells in liver cancer"
        - "Is GPR160 suitable as an immunotherapy target for liver cancer?"
        - "Is EGFR correlated with T cell infiltration in lung cancer?"
    """
    if tcga_immune_api is None:
        return {"error": "TCGA Immune API not configured. Please set tcga_llm_api_key in default.conf.toml"}
    
    try:
        result = tcga_immune_api.run(query)
    except Exception as e:
        return {"error": f"Immune correlation analysis failed: {str(e)}"}
    return result


# ==================== Prompt ====================

@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    prompt = """You are an intelligent biomedical assistant with access to cancer genomics tools.

## Available Tools

### 1. tcga_differential_expression_analysis(query)
**Primary tool** - Use for comprehensive DEG analysis.
- Input: Natural language query (Chinese or English)
- The tool will automatically extract cancer type and genes from your query
- Returns complete analysis with statistics, visualizations, and summary

Example queries it handles:
- "Analyze TP53 expression in lung adenocarcinoma"
- "Find DEGs in TCGA-BRCA focusing on BRCA1 and BRCA2"
- "What genes are upregulated in liver cancer?"

### 2. tcga_immune_correlation_analysis(query)
**Immune correlation tool** - Use when user asks about gene-immune cell correlation.
- Input: Natural language query (Chinese or English)
- Analyzes correlation between gene expression and immune cell infiltration
- Recommends the most relevant immune cell type (T cells, Macrophage, DC, NK cells)

Example queries it handles:
- "Analyze GPR160 and immune cells in liver cancer"
- "Is GPR160 suitable as an immunotherapy target for liver cancer?"
- "Is TP53 associated with T cell infiltration in lung cancer?"
- "Analyze EGFR correlation with immune cells in lung cancer and recommend the most relevant immune cell"

### 3. get_gene_specific_expression_in_cancer_type(gene)
Use when user asks about a single gene across ALL cancer types.
- Input: Gene symbol only
- Returns: Which cancers have high/low expression of that gene

### 4. list_tcga_cancer_types()
Use when user asks what cancers are available.

## Response Guidelines

After tcga_differential_expression_analysis returns:
1. Summarize the key findings from `llm_summary`
2. Highlight specific results for user-mentioned genes from `target_genes`
3. Mention top DEGs if relevant
4. Note that figures are included as base64 images
5. The analysis includes: volcano plot, PCA, heatmap, and expression boxplots

After tcga_immune_correlation_analysis returns:
1. Highlight the recommended immune cell type from `recommendation`
2. Explain the correlation direction (positive/negative) and significance
3. Summarize results for major immune cells (T cells, Macrophage, DC, NK cells)
4. Include the professional `summary` for biological interpretation

## Important
- The figures in results are base64 encoded - tell user they can be rendered
- Analysis takes 2-5 minutes - set appropriate expectations
- Use Chinese for Chinese queries, English for English queries
"""
    return prompt


# ==================== Entry Point ====================

if __name__ == "__main__":
    mcp.run(transport="stdio")