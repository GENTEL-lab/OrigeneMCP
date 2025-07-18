from mcp.server.fastmcp import FastMCP

from tools.tcga.tcga_api import TCGA_API


mcp = FastMCP("tcga_mcp", stateless_http=True)
tcga_api = TCGA_API()


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

@mcp.prompt()
def system_prompt():
    """System prompt for client."""
    prompt ="""You are an intelligent biomedical assistant with access to cancer genomics tools.
    When a user asks about the expression pattern of a specific gene across cancer types, 
    your goal is to identify which cancer types show high or low expression of that gene.
    Fill in missing arguments with sensible values if the user hasn't provided them such as the gene. 
    Answer clearly and concisely, and cite the gene symbol mentioned."""
    return prompt

