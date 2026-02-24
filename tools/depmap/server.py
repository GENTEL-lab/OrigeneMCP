"""
DepMap MCP Server
=================
Provides DepMap cancer cell line analysis tools via MCP protocol.
"""

from mcp.server.fastmcp import FastMCP
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

try:
    # When imported as package
    from .depmap_api import DepMapAPI
except ImportError:
    # When running script directly
    from depmap_api import DepMapAPI


# ==================== Load Config ====================


def load_config() -> dict:
    """Load config from default.conf.toml"""
    # Search for config file in parent directories
    config_path = Path(__file__).parent.parent.parent / "default.conf.toml"
    if not config_path.exists():
        config_path = Path(__file__).parent.parent / "default.conf.toml"
    if not config_path.exists():
        config_path = Path("default.conf.toml")

    if config_path.exists():
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    return {}


config = load_config()


# ==================== Initialize ====================

mcp = FastMCP("depmap_mcp", stateless_http=True)


# Initialize DepMap API with data directory
# Use relative path based on this script's location (./data directory)
def get_data_dir():
    """Get data directory path, supporting relative paths"""
    config_data_dir = config.get("depmap_data_dir", None)

    if config_data_dir is None:
        # Default: use ./data relative to this script
        return Path(__file__).parent / "data"

    data_path = Path(config_data_dir)

    # If it's a relative path, resolve it relative to the config file location
    if not data_path.is_absolute():
        # Config file is at project root (OrigeneMCP/default.conf.toml)
        config_base = Path(__file__).parent.parent.parent
        data_path = config_base / config_data_dir

    return data_path


depmap_data_dir = get_data_dir()
depmap_api = None

try:
    depmap_api = DepMapAPI(data_dir=depmap_data_dir)
except Exception as e:
    print(f"Warning: Failed to initialize DepMap API: {e}")
    print("DepMap tools will return errors until properly configured.")


# ==================== Tools ====================


@mcp.tool()
async def depmap_get_dependency(gene: str, cancer_type: str):
    """
    Analyze gene dependency (essentiality) in specific cancer type using CRISPR knockout data.

    This tool reveals how essential a gene is for cancer cell survival. Lower Chronos scores
    indicate stronger dependency (cell death upon knockout).

    Args:
        gene: Gene symbol (e.g., "ERBB2", "KRAS", "TP53")
        cancer_type: Cancer type (e.g., "Breast", "Pancreas", "Lung")

    Returns:
        Comprehensive dependency analysis including:
        - chronos_score_mean: Average dependency score (more negative = more essential)
        - probability_mean: Probability of being a true dependency
        - lethal_ratio: Percentage of cell lines where knockout is lethal
        - top_5_sensitive_lines: Cell lines most dependent on this gene
        - conclusion: Natural language summary with statistical details

    Example query: {"gene": "ERBB2", "cancer_type": "Breast"}
    """
    if depmap_api is None:
        return {
            "success": False,
            "error": "DepMap API not initialized. Please configure depmap_data_dir in config.",
        }

    try:
        result = depmap_api.get_dependency(gene=gene, cancer_type=cancer_type)
        return result
    except Exception as e:
        return {"success": False, "error": f"Error in dependency analysis: {str(e)}"}


@mcp.tool()
async def depmap_get_expression(gene: str, cancer_type: str):
    """
    Analyze gene expression levels in specific cancer type using RNA-seq data (logTPM).

    This tool shows how highly a gene is expressed across cancer cell lines, which helps
    assess target availability for drug development.

    Args:
        gene: Gene symbol (e.g., "ERBB2", "EGFR", "CD19")
        cancer_type: Cancer type (e.g., "Breast", "Lung", "Leukemia")

    Returns:
        Expression analysis including:
        - mean: Average expression level (logTPM)
        - median: Median expression level
        - expression_level: Categorical level (high/moderate/low)
        - top_5_high_expression: Cell lines with highest expression
        - conclusion: Detailed summary with detection rate, std dev, and peak expression

    Example query: {"gene": "ERBB2", "cancer_type": "Breast"}
    """
    if depmap_api is None:
        return {
            "success": False,
            "error": "DepMap API not initialized. Please configure depmap_data_dir in config.",
        }

    try:
        result = depmap_api.get_expression(gene=gene, cancer_type=cancer_type)
        return result
    except Exception as e:
        return {"success": False, "error": f"Error in expression analysis: {str(e)}"}


@mcp.tool()
async def depmap_get_mutation(gene: str, cancer_type: str):
    """
    Analyze gene mutation patterns in specific cancer type.

    This tool identifies mutation frequency, types, and hotspots, which helps understand
    the genetic alterations driving cancer and identify potential biomarkers.

    Args:
        gene: Gene symbol (e.g., "TP53", "KRAS", "BRAF")
        cancer_type: Cancer type (e.g., "Pancreas", "Colorectal", "Melanoma")

    Returns:
        Mutation analysis including:
        - frequency: Mutation frequency (0-1)
        - mutated_count: Number of cell lines with mutations
        - total_cell_lines: Total cell lines analyzed
        - frequency_category: Classification (frequently/recurrently/rarely mutated)
        - variant_types: Top mutation types with counts
        - hotspots: Top protein changes (mutation hotspots)
        - conclusion: Summary with dominant variant type and most common hotspot

    Example query: {"gene": "KRAS", "cancer_type": "Pancreas"}
    """
    if depmap_api is None:
        return {
            "success": False,
            "error": "DepMap API not initialized. Please configure depmap_data_dir in config.",
        }

    try:
        result = depmap_api.get_mutation(gene=gene, cancer_type=cancer_type)
        return result
    except Exception as e:
        return {"success": False, "error": f"Error in mutation analysis: {str(e)}"}


@mcp.tool()
async def depmap_comprehensive_analysis(gene: str, cancer_type: str):
    """
    Perform comprehensive DepMap analysis including dependency, expression, and mutation.

    This is the most complete analysis tool that combines all three dimensions of cancer
    genomics data to provide a holistic view of a gene's role in a specific cancer type.

    Use this when you need a complete picture for target validation or mechanistic insights.

    Args:
        gene: Gene symbol (e.g., "ERBB2", "KRAS")
        cancer_type: Cancer type (e.g., "Breast", "Pancreas")

    Returns:
        Combined analysis with three sections:
        - dependency: Complete dependency analysis
        - expression: Complete expression analysis
        - mutation: Complete mutation analysis

    Example query: {"gene": "ERBB2", "cancer_type": "Breast"}
    """
    if depmap_api is None:
        return {
            "success": False,
            "error": "DepMap API not initialized. Please configure depmap_data_dir in config.",
        }

    try:
        result = depmap_api.get_comprehensive_analysis(
            gene=gene, cancer_type=cancer_type
        )
        return result
    except Exception as e:
        return {"success": False, "error": f"Error in comprehensive analysis: {str(e)}"}


# ==================== Prompt ====================


@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    prompt = """You are an intelligent biomedical assistant with access to DepMap cancer cell line analysis tools.

## DepMap Data Overview

DepMap (Dependency Map) is a comprehensive cancer genomics resource containing:
- **CRISPR Dependency Data**: Gene essentiality screens across 1000+ cancer cell lines
- **Expression Data**: RNA-seq expression profiles (logTPM)
- **Mutation Data**: Genomic alterations and mutation hotspots

## Available Tools

### 1. depmap_comprehensive_analysis(gene, cancer_type)
**Primary tool** - Use for complete analysis of a gene in a cancer type.
- Returns dependency, expression, and mutation data in one call
- Best for target validation and comprehensive gene characterization

### 2. depmap_get_dependency(gene, cancer_type)
Use when focus is on gene essentiality/dependency:
- Identifies if gene is essential for cancer cell survival
- Shows cell lines most sensitive to gene knockout
- Reveals potential drug targets (high dependency = good target)

### 3. depmap_get_expression(gene, cancer_type)
Use when focus is on gene expression:
- Shows expression levels across cell lines
- Identifies high-expressing cell lines
- Helps assess target availability

### 4. depmap_get_mutation(gene, cancer_type)
Use when focus is on mutations:
- Reveals mutation frequency and types
- Identifies mutation hotspots
- Shows genetic alterations in cancer

## Cancer Type Names

Common cancer types include:
- Breast, Lung, Pancreas, Colorectal, Liver, Stomach
- Ovarian, Prostate, Kidney, Bladder, Melanoma
- Leukemia, Lymphoma, Glioma, Neuroblastoma
- And many more (use exact names from DepMap)

## Response Guidelines

After receiving analysis results:

1. **For Dependency Analysis:**
   - Interpret Chronos scores (< -0.5 = strong dependency)
   - Highlight lethal ratio and sensitive cell lines
   - Explain implications for drug targeting

2. **For Expression Analysis:**
   - Interpret expression levels (high > 6, low < 1 logTPM)
   - Note detection rate and variability
   - Discuss target availability

3. **For Mutation Analysis:**
   - Explain mutation frequency and significance
   - Highlight dominant variant types
   - Discuss hotspots and their implications

4. **For Comprehensive Analysis:**
   - Synthesize all three dimensions
   - Provide integrated interpretation
   - Suggest therapeutic implications

## Important Notes

- All conclusions are auto-generated with statistical details
- Top cell lines are ranked by sensitivity/expression
- Use gene symbols (not gene IDs)
- Cancer type names are case-sensitive
- Results are based on cancer cell line models (in vitro data)

## Example Queries

- "Analyze ERBB2 dependency in Breast cancer"
- "What is KRAS expression in Pancreas cancer?"
- "Show me TP53 mutations in Lung cancer"
- "Give me a comprehensive analysis of EGFR in Lung cancer"
"""
    return prompt


# ==================== Entry Point ====================

if __name__ == "__main__":
    mcp.run(transport="stdio")
