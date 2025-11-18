from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crewai import Crew
from .agents import researcher, writer, reviewer
from .tasks import create_tasks

app = FastAPI(title="Repo_AI_Agent")
templates = Jinja2Templates(directory="app/app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, repo_url: str = Form(...)):
    try:
        tasks = create_tasks(repo_url)
        crew = Crew(
            agents=[researcher, writer, reviewer],
            tasks=tasks,
            verbose=2
        )
        result = crew.kickoff()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": str(result),
            "repo_url": repo_url
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"❌ Error: {str(e)}",
            "repo_url": repo_url
        })
