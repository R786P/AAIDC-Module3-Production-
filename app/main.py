from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crewai import Crew
import os

# Templates folder ab 'app/templates' mein hai
templates = Jinja2Templates(directory="app/app/templates")

# Agents aur tasks ko app package se import karein
from .agents import researcher, reviewer, writer # Directory Fix: .agents se import
from .tasks import create_tasks # tasks.py ko bhi app/ mein hona chahiye

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the index.html page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_project(request: Request, repository_url: str = Form(...)):
    """Handle form submission and run the AI Crew."""
    
    context = {"request": request, "repository_url": repository_url}
    
    try:
        tasks = create_tasks(repository_url)
        
        project_crew = Crew(
            agents=[researcher, writer, reviewer],
            tasks=tasks,
            verbose=True, # VERBOSE FIX
        )

        analysis_result = project_crew.kickoff()
        context["output"] = analysis_result
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        
        if "quota" in str(e).lower() or "not found" in str(e).lower():
            error_message = f"Error: LLM/API issue: {str(e)}. Check GROQ_API_KEY and model name."
        
        context["error_message"] = error_message
        context["output"] = None

    return templates.TemplateResponse("index.html", context)
