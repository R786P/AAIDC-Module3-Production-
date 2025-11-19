from langchain_community.tools.tavily_search import TavilySearchResults
import os

if 'TAVILY_API_KEY' not in os.environ:
    raise ValueError("TAVILY_API_KEY environment variable not set.")

tavily_search_tool = TavilySearchResults(name="Tavily Search")
