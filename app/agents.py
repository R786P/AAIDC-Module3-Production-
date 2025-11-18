from crewai import Agent
from langchain_groq import ChatGroq
import os
# Saare crewai tools yahaan se aate hain, aur hum TavilyTool use karenge
from crewai_tools import TavilySearchTool 
from langchain_community.tools import tool

# LLM Setup (Groq - Free)
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model='gpt-3.5-turbo'
)

# Tools Definition (Tavily - Standard CrewAI/Langchain Tool)
# TavilySearchTool ko is tarah initialize kariye
tavily_search_tool = TavilySearchTool(
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

# Agents
researcher = Agent(
    role="Senior Researcher",
    goal="Find relevant info about the GitHub project",
    backstory="Expert in web research with 10+ years of experience",
    tools=[tavily_search_tool], # <-- Ab yeh BaseTool instance hai
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
