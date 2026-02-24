from tavily import TavilyClient


class TavilySearchEngine:
    def __init__(self, api_key: str):
        self.tavily_cli = TavilyClient(api_key=api_key)
    
    def run(self, query: str):
        results = self.tavily_cli.search(
            query=query,
            # search_depth='advanced',
            max_results=5,
            topic="general",
            include_answer=True
        )
        return results