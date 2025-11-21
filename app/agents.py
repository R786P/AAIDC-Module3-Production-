from app.tools import ReadGitHubReadmeTool
from langchain_groq import ChatGroq
import os

# LLM Setup (Groq - Free)
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# Tools (Tavily + GitHub Reader)
from crewai_tools import TavilySearchTool
tavily_tool = TavilySearchTool()

# GitHub Tool Import
from app.tools import ReadGitHubReadmeTool
github_reader = ReadGitHubReadmeTool()

# Agents
researcher = Agent(
    role="Senior Researcher",
    goal="Analyze the actual GitHub repo content AND find similar projects",
    backstory="Expert who reads repo content first, then researches",
    tools=[tavily_tool, github_reader],  # ✅ Both tools
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="सुझाव हिंदी में दें",
    backstory="आप हिंदी में स्पष्ट और क्रियाशील सुझाव लिखते हैं",
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
