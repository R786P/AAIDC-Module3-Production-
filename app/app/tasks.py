from crewai import Task
from .agents import researcher, writer, reviewer

def create_tasks(repository_url: str):
    """
    GitHub repository URL के लिए CrewAI tasks बनाता है।
    """
    
    # 1. Research Task: Researcher agent के लिए
    research_task = Task(
        description=f"""
        GitHub repository URL: {repository_url} का complete analysis करिए।
        
        Aapko yeh areas cover karne hain:
        1. Technology Stack Analysis: Dekhiye ki project mein kaun-kaun si programming languages, frameworks, aur libraries (dependencies) use ho rahi hain.
        2. Code Quality and Best Practices: Code structure, maintainability, aur security vulnerabilities ko check kariye.
        3. Project Health and Activity: Dekhiye ki project kitna active hai (recent commits, issues, pull requests).
        4. Actionable Suggestions: Kum se kum teen (3) practical aur professional suggestions dijiye jisse project ki performance, code quality, ya security immediately improve ho sake. 
        
        Hamesha Tavily Tool ka use karke latest industry standards ko verify kariye.
        """,
        expected_output="Project ka detailed analysis, teen (3) verified, actionable, aur professional suggestions ke saath. Output sirf technical aur objective tone mein hona chahiye.",
        agent=researcher,
    )

    # 2. Writing Task: Writer agent के लिए
    writing_task = Task(
        description="""
        Researcher ke detailed analysis aur suggestions ko leke, ek final, polished technical report banaiye.
        
        Report ko ek single, professional Markdown document mein format kariye.
        - Report mein koi bhi casual ya conversational language nahi honi chahiye.
        - Structure: Title, Introduction, Detailed Analysis Findings, aur Actionable Suggestions (Bullet points mein).
        """,
        expected_output="""
        Ek complete, well-formatted Markdown report jismein detailed analysis aur actionable suggestions hain.
        Report ka tone hamesha professional aur formal hona chahiye.
        """,
        agent=writer,
        context=[research_task],
    )
    
    # 3. Review Task: Reviewer agent के लिए
    review_task = Task(
        description="""
        Writer dwara banaye gaye final report ko review kariye.
        
        Aapko yeh confirm karna hai:
        1. Tone aur Professionalism: Poori report ka tone strictly professional aur formal hai.
        2. Clarity aur Correctness: Saari technical details aur suggestions sahi aur samajhne mein aasan hain.
        3. Completion: Report mein saare zaroori sections (Analysis, Suggestions) shamil hain.
        
        Agar koi bhi correction zaroori ho, to report ko theek karke final, ready-to-present version dijiye.
        """,
        expected_output="Final, error-free, aur professional-toned technical Markdown report, jo seedhe client ko bheja jaa sake. Koi bhi extra text ya commentary shamil na karein.",
        agent=reviewer,
        context=[writing_task],
    )
    
    return [research_task, writing_task, review_task]
