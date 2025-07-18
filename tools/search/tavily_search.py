
from langchain_tavily import TavilySearch


class TavilySearchEngine:
    def __init__(self, api_key: str):
        self.tavily_tool = TavilySearch(
            tavily_api_key=api_key,
            max_results=5,
            topic="general",
            include_answer=True
        )
    
    def run(self, query: str):
        results = self.tavily_tool.invoke(query)
        return results
