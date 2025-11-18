from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crewai import Crew
import os

templates = Jinja2Templates(directory="app/templates/tools")

# Import agents and tasks from the app package
from .agents import researcher, reviewer, writer
from .tasks import create_tasks

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
        # 1. Create Tasks based on the URL input
        tasks = create_tasks(repository_url)
        
        # 2. Initialize the Crew
        project_crew = Crew(
            agents=[researcher, writer, reviewer],
            tasks=tasks,
            verbose=True, # VERBOSE FIX
        )

        # 3. Run the analysis
        analysis_result = project_crew.kickoff()
        
        # 4. Display Result
        context["output"] = analysis_result
        
    except Exception as e:
        # 5. Handle Errors (e.g., Quota, API Key, Model Not Found)
        error_message = f"An error occurred: {str(e)}"
        
        # Specific messages for known errors
        if "insufficient_quota" in str(e).lower():
            error_message = "Error: API Quota Exceeded. Please check your billing or API Key."
        elif "model not found" in str(e).lower() or "invalid_request_error" in str(e).lower():
             error_message = "Error: LLM Model Not Found or temporarily unavailable. Groq is currently unstable; you may need to try a different model (like llama3-8b-8192) in agents.py."
        
        context["error_message"] = error_message
        context["output"] = None

    return templates.TemplateResponse("index.html", context)
