import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    # Choose the packages you want to use
    tool_packages = [
        "chembl", "kegg", "string", "search", "pubchem", "ncbi",
        "uniprot", "tcga", "ensembl", "ucsc", "fda_drug", "pdb",
        "monarch", "clinicaltrials", "dbsearch", "opentargets", "depmap"
    ]
    tool_packages = [server+'_mcp' for server in tool_packages]

    mcp_servers = {
        package: {
            "transport": "streamable_http",
            "url": f"http://127.0.0.1:8788/{package}/mcp/"
        } for package in tool_packages
    }

    client = MultiServerMCPClient(mcp_servers)
    tools = await client.get_tools()
    print(f"✅ Found {len(tools)} mcp tools")
    tool_map = {tool.name: tool for tool in tools}

    tool_name = "get_general_info_by_protein_or_gene_name"
    tool = tool_map[tool_name]
    result = await tool.ainvoke({"query": "TP53"})
    print('=' * 80)
    print(f'Tool name: {tool_name}')
    print(str(result)[:200])
    
    tool_name = "tavily_search"
    tool = tool_map[tool_name]
    result = await tool.ainvoke({"query": "What is the relationship between TP53 and cancer?"})
    print('=' * 80)
    print(f'Tool name: {tool_name}')
    print(str(result))
    

if __name__ == "__main__":
    asyncio.run(main())