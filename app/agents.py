from crewai import Agent
from langchain_groq import ChatGroq
import os

# Ensure GROQ_API_KEY is available
if 'GROQ_API_KEY' not in os.environ:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Using Llama 3 on Groq (assuming the last model was 'llama3-8b-8192')
groq_llm = ChatGroq(
    temperature=0.6, # Thoda kam temperature, taki less creative ho
    model="gemma-7b-it", 
)

# --- AGENT DEFINITIONS ---
researcher = Agent(
    role='Elite Senior Software Analyst and Code Quality Expert', # Role ko mazboot kiya
    goal='Provide verified, actionable, professional, and formal suggestions to improve the project repository.', # Goal ko strict kiya
    backstory=(
        "You are a leading expert in software architecture and code quality. "
        "Your responses must **ALWAYS** be delivered in a **highly professional, formal, and objective tone**. "
        "Never use casual, friendly, or conversational language (e.g., 'Hello!', 'Hope this helps!'). " # Nayi strict instruction
        "Your expertise lies in evaluating project structures, documentation, dependencies, and suggesting best practices."
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Professional Technical Writer and Report Editor',
    goal='Format the analysis findings into a highly professional, clear, and easy-to-read Markdown report.',
    backstory=(
        "You are an expert technical writer known for creating compelling and actionable reports. "
        "Maintain a **formal, objective, and professional tone** throughout the final report. " # Nayi strict instruction
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
        "Your final check must confirm that the report's tone is **strictly professional and formal**." # Nayi strict instruction
    ),
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)
