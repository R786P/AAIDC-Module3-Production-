
from crewai import Agent
from langchain_groq import ChatGroq
import os
# Zaroori naya import: crewai_tools se 'tool' function import kiya gaya hai
from crewai_tools import tool 

# LLM Setup (Groq - Free)
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# Tools (Tavily - free web search)
from tavily import TavilyClient
# TavilyClient ko globally initialize kiya gaya hai
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# @tool decorator use kiya gaya hai
# Yeh function ko CrewAI ke liye ek valid Tool object mein badal deta hai.
@tool("Tavily Web Search Tool") 
def tavily_search(query: str) -> str:
    """Useful for searching the web for up-to-date information."""
    return tavily.search(query, search_depth="advanced")["answer"]

# Agents
researcher = Agent(
    role="Senior Researcher",
    goal="Find relevant info about the GitHub project",
    backstory="Expert in web research with 10+ years of experience",
    tools=[tavily_search], # Ab yeh sahi format mein hai
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
