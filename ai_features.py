import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")

def generate_task_breakdown(task_title, task_description):
    """
    Generate a detailed breakdown of a complex task using Gemini AI
    
    Args:
        task_title: The title of the task
        task_description: Detailed description of the task
    
    Returns:
        A formatted string with task breakdown
    """
    if not GEMINI_API_KEY:
        return "❌ Error: GEMINI_API_KEY not configured. Please add it to your .env file."
    
    try:
        # Use the gemini-flash-lite-latest model as requested
        model = genai.GenerativeModel('gemini-flash-lite-latest')
        
        prompt = f"""You are a productivity expert. Break down the following task into clear, actionable subtasks.

Task Title: {task_title}
Task Description: {task_description}

Please provide:
1. A brief analysis of the task
2. 5-8 specific, actionable subtasks (numbered)
3. Estimated time for each subtask
4. Any dependencies between subtasks
5. Tips for successful completion

Format your response in a clear, organized markdown format."""
        
        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        return f"❌ Error generating task breakdown: {str(e)}\n\nPlease check your API key and internet connection."

def generate_reminder_email(task_title, task_description, deadline, priority):
    """
    Generate a personalized reminder email using Gemini AI
    
    Args:
        task_title: The title of the task
        task_description: Description of the task
        deadline: Deadline date string
        priority: Priority level (Low/Medium/High)
    
    Returns:
        A formatted email message
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not configured. Please add it to your .env file."
    
    try:
        # Use the gemini-flash-lite-latest model as requested
        model = genai.GenerativeModel('gemini-flash-lite-latest')
        
        prompt = f"""Generate a friendly but professional email reminder for the following task:

Task: {task_title}
Description: {task_description}
Deadline: {deadline}
Priority: {priority}

The email should:
1. Start with a friendly greeting
2. Remind about the task and its importance
3. Mention the deadline and urgency (Priority: {priority})
4. Provide a brief motivational message
5. End with an encouraging note
6. Keep it concise (max 150 words)
7. It should end with Kumar Arpit

Write the email in a warm, encouraging tone."""
        
        response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        return f"Error generating email: {str(e)}"

def generate_task_suggestions(completed_tasks_list):
    """
    Generate suggestions for new tasks based on completed tasks
    
    Args:
        completed_tasks_list: List of completed task titles
    
    Returns:
        A list of suggested tasks
    """
    if not GEMINI_API_KEY:
        return ["Error: GEMINI_API_KEY not configured"]
    
    try:
        model = genai.GenerativeModel('gemini-flash-lite-latest')
        
        tasks_text = "\n".join([f"- {task}" for task in completed_tasks_list])
        
        prompt = f"""Based on these completed tasks:

{tasks_text}

Suggest 3-5 logical next tasks or related tasks that would be good to tackle next. 
Consider natural progressions, related skills, and complementary activities.

Return only the task titles as a simple bullet list."""
        
        response = model.generate_content(prompt)
        
        # Parse response into list
        suggestions = [line.strip('- ').strip() for line in response.text.split('\n') if line.strip()]
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    except Exception as e:
        return [f"Error generating suggestions: {str(e)}"]
