from crewai import Agent
from langchain_groq import ChatGroq
# सही Import: TavilySearchResults को import करें
from app.tools.tavily_search import TavilySearchResults
import os

# --- LLM CONFIGURATION ---
if 'GROQ_API_KEY' not in os.environ:
    raise ValueError("GROQ_API_KEY environment variable not set.")

groq_llm = ChatGroq(
    temperature=0.6,
    model="llama2-70b-4096",
)

# --- TOOL INSTANTIATION ---
tavily_search_tool = TavilySearchResults(name="Tavily Search")

# --- AGENT DEFINITIONS ---
researcher = Agent(
    role='Elite Senior Software Analyst',
    goal='Provide verified, actionable suggestions for the project.',
    backstory=(
        "You are a leading expert in software architecture. "
        "Always maintain a professional tone. "
        "You MUST use the Tavily Search Tool to verify dependencies."
    ),
    llm=groq_llm,
    tools=[tavily_search_tool], 
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Professional Technical Writer',
    goal='Format analysis into a professional markdown report.',
    backstory="You are an expert technical writer.",
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)

reviewer = Agent(
    role='Quality Assurance Specialist',
    goal='Review the final report for accuracy.',
    backstory="You are a meticulous QA specialist.",
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)
