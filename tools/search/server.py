
from asyncio import to_thread

from mcp.server.fastmcp import FastMCP

from tools.search.tavily_search import TavilySearchEngine
from tools.search.jina_search import JinaSearchEngine
from deploy.config import conf


mcp = FastMCP(
    "search_mcp",
    stateless_http=True,
)


tavily_api = TavilySearchEngine(conf["tavily_api_key"])
jina_api = JinaSearchEngine(conf["jina_api_key"])


@mcp.tool()
async def tavily_search(query: str):
    """
    Run the search engine with a given query, retrieving and filtering results.
    """
    if not conf["tavily_api_key"]:
        return "Tavily API key is not set in the configuration."
    
    try:
        results = await to_thread(tavily_api.run, query)
    except Exception as e:
        results = f"Tool tavily_search execution failed for query: {query}, error: {e}"
    return results


@mcp.tool()
async def jina_search(query: str):
    """
    Run the jina DeepSearch engine with a given query, retrieving and filtering results.
    """
    if not conf["jina_api_key"]:
        return "Jina API key is not set in the configuration."
    
    try:
        results = await to_thread(jina_api.run, query)
    except Exception as e:
        results = f"Tool jina_search execution failed for query: {query}, error: {e}"
    return results