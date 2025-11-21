import os
from langchain_core.tools import BaseTool 
from tavily import TavilyClient
from pydantic import PrivateAttr

if 'TAVILY_API_KEY' not in os.environ:
    raise ValueError("TAVILY_API_KEY environment variable not set.")

class TavilySearchResults(BaseTool):
    name: str = "Tavily Search"
    description: str = "Search the web for current information."
    _client: TavilyClient = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    def _run(self, query: str) -> str:
        try:
            results = self._client.search(query=query, search_depth="advanced", max_results=5)
            context = [f"Source: {r['url']}\nContent: {r['content']}" for r in results.get("results", [])]
            return "\n\n".join(context) if context else "No results found."
        except Exception as e:
            return f"Error: {str(e)}"
