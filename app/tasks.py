from crewai import Task
from .agents import researcher, writer, reviewer
  def create_tasks(repo_url: str):
    research_task = Task(
        description=f"""
        Step 1: Read the actual GitHub repo content from {repo_url}
        Step 2: Then research similar projects and best practices
        Step 3: Compare the actual repo with best practices
        """,
        agent=researcher,
        expected_output="Detailed analysis of the actual repo + comparison with best practices"
    )
    agent=researcher,
    output_file="research_output_hindi.md"
    )

    # 2. Writing Task: Writer agent (Hindi report banayega)
    writing_task = Task(
        description="""
        Researcher ke Hindi analysis ko lekar ek final, polished technical report banaiye.
        
        Guidelines:
        - **Pura report Hindi mein hona chahiye**, lekin **technical shabdon ko English mein rakhein** (jaise: "README file", "API key", "vector database").
        - Report structure:
          * **शीर्षक (Title)**
          * **परिचय (Introduction)**
          * **विश्लेषण निष्कर्ष (Analysis Findings)**
          * **क्रियान्वयन योग्य सुझाव (Actionable Suggestions)** → bullet points mein
        - Bhasha sadharan, spasht aur vyavsayik (professional) honi chahiye.
        """,
        expected_output="""
        Ek complete Markdown report jo **Hindi mein ho**, lekin **technical terms English mein ho**.
        Report formal, clear aur client-ready hona chahiye.
        """,
        agent=writer,
        context=[research_task],
        output_file="final_report_hindi.md"
    )
    
    # 3. Review Task: Reviewer agent (Hindi report ko verify karega)
    review_task = Task(
        description="""
        Writer dwara banaye gaye Hindi report ko final review kariye.
        
        Check karein:
        1. **Bhasha**: Kya report sahi Hindi mein hai? Kya kahi koi English sentence galti se nahi likha gaya?
        2. **Technical Accuracy**: Kya technical terms sahi tareeke se English mein hain?
        3. **Professionalism**: Kya tone formal aur client-ready hai?
        4. **Completeness**: Kya sab sections present hain?
        
        Agar koi galti ho, toh usse sudhar kar ek final, ready-to-deliver version taiyaar karein.
        """,
        expected_output="""
        Ek final, error-free Hindi technical report jo seedhe client ko bheja ja sake.
        Report **Hindi mein hoga**, lekin **technical terms (jaise GitHub, LLM, API) English mein honge**.
        Koi bhi extra commentary nahi hoga — sirf report.
        """,
        agent=reviewer,
        context=[writing_task],
        output_file="reviewed_final_report_hindi.md"
    )
    
    return [research_task, writing_task, review_task]
