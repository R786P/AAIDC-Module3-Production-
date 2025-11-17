from crewai import Agent
from crewai_tools import BaseTool
from langchain_groq import ChatGroq
import os
from tavily import TavilyClient

# LLM Setup
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# Tavily client initialization
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Tool ko BaseTool class se define kiya gaya hai
class TavilySearchTool(BaseTool):
    name = "Tavily Web Search Tool"
    description = "Useful for searching the web for up-to-date information."
    
    def _run(self, query: str) -> str:
        return tavily.search(query, search_depth="advanced")["answer"]

# Agents Definition
researcher = Agent(
    role="Senior Researcher",
    goal="Find relevant info about the GitHub project",
    backstory="Expert in web research with 10+ years of experience",
    tools=[TavilySearchTool()], 
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Suggest improvements for the project",
    backstory="Writes clear, actionable, and user-friendly suggestions",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Validate suggestions against facts",
    backstory="Ensures accuracy, relevance, and professionalism",
    llm=llm,
    verbose=True
)
