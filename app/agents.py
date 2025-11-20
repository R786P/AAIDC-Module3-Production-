from crewai import Agent
from langchain_groq import ChatGroq
import os

# LLM Setup (Groq - Free)
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# Tools (Tavily - free web search)
from crewai_tools import TavilySearchTool
tavily_tool = TavilySearchTool()

# Agents
from .tools import read_github_readme  # New tool
researcher = Agent(
    role="Senior Researcher",
    goal="Analyze the actual GitHub repo content AND find similar projects",
    backstory="Expert who reads repo content first, then researches",
    tools=[tavily_tool, read_github_readme],  # Both tools
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="प्रोजेक्ट में सुधार के लिए स्पष्ट और क्रियाशील सुझाव हिंदी में लिखें",
    backstory="आप हिंदी में विस्तृत, उपयोगी और आसानी से समझने वाले सुझाव देते हैं",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="सुझावों को तथ्यों के खिलाफ सत्यापित करें और हिंदी में प्रतिक्रिया दें",
    backstory="आप सटीकता, प्रासंगिकता और हिंदी में स्पष्टता सुनिश्चित करते हैं",
    llm=llm,
    verbose=True
)
