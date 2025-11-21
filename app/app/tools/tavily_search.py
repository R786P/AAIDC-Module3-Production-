import os
# FIX: 'crewai_tools' ki jagah ab hum 'langchain_core' se BaseTool lenge
from langchain_core.tools import BaseTool 
from tavily import TavilyClient
from pydantic import PrivateAttr

# Check API Key
if 'TAVILY_API_KEY' not in os.environ:
    raise ValueError("TAVILY_API_KEY environment variable not set.")

class TavilySearchResults(BaseTool):
    """
    A custom tool that uses the Tavily Search API.
    Inherits from LangChain's BaseTool to be compatible with CrewAI.
    """
    
    name: str = "Tavily Search"
    description: str = (
        "Search the web for current information, code documentation, "
        "or recent events. Input should be a search query string."
    )
    
    # Private attribute for the client (Pydantic v2 compatible)
    _client: TavilyClient = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

    def _run(self, query: str) -> str:
        try:
            # Perform the search
            results = self._client.search(query=query, search_depth="advanced", max_results=5)
            
            # Format the results
            context = []
            for result in results.get("results", []):
                context.append(f"Source: {result.get('title')} ({result.get('url')})\nSnippet: {result.get('content')}")
            
            if not context:
                return "No relevant search results found."
                
            return "\n\n---\n\n".join(context)
            
        except Exception as e:
            return f"Error performing search: {str(e)}"
