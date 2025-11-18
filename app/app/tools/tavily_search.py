from langchain_community.tools.tavily_search import TavilySearchResults
import os

# Zaroori: Environment Variable check karein
if 'TAVILY_API_KEY' not in os.environ:
    raise ValueError("TAVILY_API_KEY environment variable not set.")

# Tavily tool ko initialize karna
# 'Tavily Search' tool ka naam Agent ko batata hai ki use kab internet use karna hai
tavily_search_tool = TavilySearchResults(name="Tavily Search")
