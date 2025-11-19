from crewai import Agent, Tool
from langchain_groq import ChatGroq
import os

# ======================
# 1. LLM Setup (Groq)
# ======================
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

# ======================
# 2. Tavily Search Function
# ======================
from tavily import TavilyClient
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query: str) -> str:
    """Performs a web search using Tavily API and returns a concise answer."""
    try:
        response = tavily.search(query, search_depth="advanced")
        return response.get("answer", "No answer found.")
    except Exception as e:
        return f"Search failed: {str(e)}"

# ======================
# 3. Define Tools
# ======================
# 🔍 Web Search Tool
web_search_tool = Tool(
    name="Web Search",
    description="Search the web for up-to-date information about GitHub projects, best practices, or AI tools.",
    func=tavily_search,
    args_schema=None
)

# ======================
# 4. Define Agents
# ======================
researcher = Agent(
    role="Senior Researcher",
    goal="Find relevant info about the GitHub project and similar repositories",
    backstory="Expert in web research with 10+ years of experience in open-source projects",
    tools=[web_search_tool],  # ✅ Now a proper Tool object
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Suggest clear, actionable improvements for the project",
    backstory="Writes user-friendly, professional suggestions for GitHub READMEs and structure",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Validate suggestions against facts and ensure accuracy",
    backstory="Ensures all suggestions are grounded in reality and relevant to the user's repo",
    llm=llm,
    verbose=True
)
