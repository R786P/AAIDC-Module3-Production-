from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crewai import Crew
import os

templates = Jinja2Templates(directory="app/app/templates")

from .agents import researcher, reviewer, writer
from .tasks import create_tasks

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_project(request: Request, repository_url: str = Form(...)):
    
    context = {"request": request, "repository_url": repository_url}
    
    try:
        tasks = create_tasks(repository_url)
        
        project_crew = Crew(
            agents=[researcher, writer, reviewer],
            tasks=tasks,
            verbose=True, 
        )

        analysis_result = project_crew.kickoff()
        
        context["output"] = analysis_result
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        
        if "insufficient_quota" in str(e).lower():
            error_message = "Error: API Quota Exceeded. Please check your OpenAI billing or switch to a different LLM (like Groq or Gemini) in agents.py."
        
        context["error_message"] = error_message
        context["output"] = None

    return templates.TemplateResponse("index.html", context)
