from crewai import Agent
from langchain_groq import ChatGroq
import os

# Ensure GROQ_API_KEY is available in Render environment variables
if 'GROQ_API_KEY' not in os.environ:
    raise ValueError("GROQ_API_KEY environment variable not set.")

groq_llm = ChatGroq(
    temperature=0.7,
    model="mixtral-8x7b-32768", 
)

# --- AGENT DEFINITIONS ---
researcher = Agent(
    role='Software Analyst',
    goal='Provide verified and actionable suggestions to improve the project repository.',
    backstory='You are a leading expert in software analysis and code quality, skilled at evaluating project structures, documentation, and dependencies.',
    llm=groq_llm,
    # Tools parameter hata diya gaya hai
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Professional Technical Writer',
    goal='Format the analysis findings into a professional, clear, and easy-to-read Markdown report.',
    backstory='You are an expert technical writer known for creating compelling and actionable reports that guide software teams.',
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)

reviewer = Agent(
    role='Quality Assurance Specialist',
    goal='Review the final report for correctness, clarity, and ensure all suggestions are actionable and accurate.',
    backstory='You are a meticulous QA specialist with an eye for detail, ensuring no errors slip into the final report.',
    llm=groq_llm,
    verbose=True,
    allow_delegation=False
)
