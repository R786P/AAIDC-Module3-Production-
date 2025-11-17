from crewai import Agent
from langchain_groq import ChatGroq
import os
from crewai_tools import TavilyTool 

# LLM Setup
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# Tools Definition
tavily_search_tool = TavilyTool(api_key=os.getenv("TAVILY_API_KEY"))

# Agents Definition
researcher = Agent(
    role="Senior Researcher",
    goal="Find relevant info about the GitHub project",
    backstory="Expert in web research with 10+ years of experience",
    tools=[tavily_search_tool], 
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
