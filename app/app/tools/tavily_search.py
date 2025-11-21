from crewai_tools import Tool
from tavily import TavilyClient
import os

class TavilySearchResults(Tool):
    name = "Tavily Search Results"
    description = "Search the web for information using Tavily API"

    def _run(self, query: str) -> str:
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        return tavily.search(query, search_depth="advanced")["answer"]
