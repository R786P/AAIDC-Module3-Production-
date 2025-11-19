# src/app/tools/tavily_search.py

import os
import requests
from crewai_tools import BaseTool  # Optional, only if you're using CrewAI tool wrapping

class TavilySearchTool(BaseTool):
    name = "tavily_search_tool"
    description = "Real-time information retrieval from Tavily search API"
    
    def _run(self, query: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY is not set in the environment!")
        
        response = requests.post(
            "https://api.tavily.com/search",  # Or the actual Tavily endpoint
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "query": query,
                "include_answers": True,
                "include_links": True,
            }
        )
        
        if response.status_code != 200:
            return f"Error from Tavily API: {response.status_code} - {response.text}"

        data = response.json()
        # Customize this as needed
        return data.get("answer", "No answer found.")

# Exportable tool instance
tavily_search_tool = TavilySearchTool()
