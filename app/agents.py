from crewai import Agent
from langchain_groq import ChatGroq
import os

# LLM Setup (Groq - Free)
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# Tools (Tavily - free web search)
from tavily import TavilyClient
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query: str) -> str:
    return tavily.search(query, search_depth="advanced")["answer"]

# Agents
researcher = Agent(
    role="Senior Researcher",
    goal="Find relevant info about the GitHub project",
    backstory="Expert in web research with 10+ years of experience",
    tools=[tavily_search],
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Suggest improvements for the project",
    backstory="Writes clear, actionable suggestions",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Validate suggestions against facts",
    backstory="Ensures accuracy and relevance",
    llm=llm,
    verbose=True
)
