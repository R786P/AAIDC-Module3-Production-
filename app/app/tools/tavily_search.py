# app/tools/tavily_search.py

import os
from langchain_community.tools.base import BaseTool # FIX: Ab BaseTool ko langchain_community se import karein
from tavily import TavilyClient

# --- Environment Check (TAVILY_API_KEY) ---
if 'TAVILY_API_KEY' not in os.environ:
    # यह चेक यहीं पर रहेगा
    raise ValueError("TAVILY_API_KEY environment variable not set.")

class TavilySearchResults(BaseTool): # FIX: Tool ko BaseTool se badla gaya
    """A tool that uses the Tavily Search API to find information."""
    
    # Tool properties
    name: str = "Tavily Search"
    description: str = (
        "Useful for searching the internet about current events, code dependencies, "
        "or latest industry practices. Input should be a single search query string."
    )
    
    # Private client instance
    _client: TavilyClient = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize client lazily or immediately
        self._client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    def _run(self, query: str) -> str:
        """
        Search the internet using Tavily.
        
        Args:
            query: The search query string.
        
        Returns:
            A string containing the summarized search results.
        """
        # Tavily search logic
        try:
            results = self._client.search(query=query, search_depth="advanced", max_results=5)
            
            context = []
            for result in results.get("results", []):
                # Only include the snippet and source title
                context.append(f"Source: {result.get('title')}, Snippet: {result.get('content')}")
            
            if not context:
                return "No useful search results found for the query."
                
            return "\n---\n".join(context)

        except Exception as e:
            return f"Error during Tavily search: {e}"

# --- Instance Creation (optional, for direct use in other modules) ---
# Note: Since this is imported via 'from app.tools.tavily_search import TavilySearchResults',
# this instance might not be strictly needed, but included for completeness if used directly.
# tavily_search_tool = TavilySearchResults(name="Tavily Search")
