from crewai import Agent
from langchain_groq import ChatGroq
from .tools.tavily_search import tavily_search_tool
import os

# --- LLM CONFIGURATION ---
# Dhyan rahe: GROQ_API_KEY environment variables mein set hona chahiye
if 'GROQ_API_KEY' not in os.environ:
    raise ValueError("GROQ_API_KEY environment variable not set.")

groq_llm = ChatGroq(
    temperature=0.6,
    model="llama2-70b-4096", # Stable Groq model
)

# --- AGENT DEFINITIONS ---
researcher = Agent(
    role='Elite Senior Software Analyst and Code Quality Expert', 
    goal='Provide verified, actionable, professional, and formal suggestions to improve the project repository.',
    backstory=(
        "You are a leading expert in software architecture and code quality. "
        "Your responses must **ALWAYS** be delivered in a **highly professional, formal, and objective tone**. "
        "Never use casual, friendly, or conversational language. "
        "You **MUST** use the Tavily Search Tool to verify all dependencies and latest practices before reporting."
    ),
    llm=groq_llm,
    tools=[tavily_search_tool],
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Professional Technical Writer and Report Editor',
    goal='Format the analysis findings into a highly professional, clear, and easy-to-read Markdown report.',
    backstory=(
        "You are an expert technical writer known for creating compelling and actionable reports. "
        "Maintain a **formal, objective, and professional tone** throughout the final report. "
        "Ensure the final document is well-structured and free of any casual dialogue."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)

reviewer = Agent(
    role='Quality Assurance Specialist',
    goal='Review the final report for correctness, clarity, and ensure all suggestions are actionable and accurate.',
    backstory=(
        "You are a meticulous QA specialist with an eye for detail, ensuring no errors slip into the final report. "
        "Your final check must confirm that the report's tone is **strictly professional and formal**."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)
