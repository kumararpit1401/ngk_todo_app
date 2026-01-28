import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import os
from email_sender import send_reminder_email
from ai_features import generate_task_breakdown, generate_reminder_email
from database import init_db, add_task, get_all_tasks, update_task_status, delete_task, get_task_by_id

# Page configuration
st.set_page_config(
    page_title="AI-Powered Todo App",
    page_icon="To-do-List",
    layout="wide"
)

# Initialize database
init_db()

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .task-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">AI-Powered Todo Application</h1>', unsafe_allow_html=True)

# Sidebar for adding tasks
with st.sidebar:
    st.header("➕ Add New Task")
    
    with st.form("add_task_form", clear_on_submit=True):
        task_title = st.text_input("Task Title", placeholder="Enter task title...")
        task_description = st.text_area("Task Description", placeholder="Enter task description...")
        
        # Deadline input
        min_date = datetime.now().date()
        task_deadline = st.date_input("Task Deadline", min_value=min_date)
        
        # Priority selection
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        # Email for reminders
        user_email = st.text_input("Your Email (for reminders)", placeholder="your.email@example.com")
        
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button:
            if task_title and task_description and user_email:
                # Add task to database
                add_task(task_title, task_description, str(task_deadline), priority, user_email)
                st.success(f"Task '{task_title}' added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all required fields!")

# Main content area
tab1, tab2, tab3 = st.tabs(["All Tasks", "AI Task Breakdown", "Email Reminders"])

with tab1:
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    with col1:
        filter_option = st.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed"]
        )
    with col2:
        sort_option = st.selectbox(
            "Sort by",
            ["Deadline", "Priority", "Date Added"]
        )
    
    # Get tasks from database
    tasks = get_all_tasks(filter_option, sort_option)
    
    if tasks:
        for task in tasks:
            task_id, title, description, deadline, priority, status, email, created_at = task
            
            # Calculate days until deadline
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            days_left = (deadline_date - datetime.now().date()).days
            
            # Color coding based on days left
            if days_left < 0:
                urgency_color = "🔴"
                urgency_text = f"Overdue by {abs(days_left)} days"
            elif days_left == 0:
                urgency_color = "🟠"
                urgency_text = "Due today!"
            elif days_left <= 3:
                urgency_color = "🟡"
                urgency_text = f"Due in {days_left} days"
            else:
                urgency_color = "🟢"
                urgency_text = f"Due in {days_left} days"
            
            # Priority emoji
            priority_emoji = {"Low": "🟦", "Medium": "🟧", "High": "🟥"}
            
            # Task card
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    checkbox_status = status == "Completed"
                    if st.checkbox(
                        f"**{title}**",
                        value=checkbox_status,
                        key=f"task_{task_id}"
                    ):
                        update_task_status(task_id, "Completed")
                        st.rerun()
                    elif not checkbox_status and status == "Completed":
                        update_task_status(task_id, "Pending")
                        st.rerun()
                    
                    st.write(f"📝 {description}")
                    st.caption(f"📅 Deadline: {deadline} {urgency_color} {urgency_text}")
                    st.caption(f"{priority_emoji[priority]} Priority: {priority}")
                    st.caption(f"📧 Email: {email}")
                
                with col2:
                    if st.button("Delete", key=f"del_{task_id}"):
                        delete_task(task_id)
                        st.success("Task deleted!")
                        st.rerun()
                
                with col3:
                    if st.button("Send Reminder", key=f"reminder_{task_id}"):
                        # Generate AI email
                        with st.spinner("Generating AI reminder email..."):
                            try:
                                email_content = generate_reminder_email(title, description, deadline, priority)
                                success = send_reminder_email(email, title, email_content)
                                
                                if success:
                                    st.success("Reminder email sent!")
                                else:
                                    st.error("Failed to send email. Check your configuration.")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                
                with col4:
                    if st.button("Breakdown", key=f"breakdown_{task_id}"):
                        st.session_state[f'show_breakdown_{task_id}'] = True
                
                # Show breakdown if requested
                if st.session_state.get(f'show_breakdown_{task_id}', False):
                    with st.expander("AI Task Breakdown", expanded=True):
                        with st.spinner("Generating task breakdown..."):
                            try:
                                breakdown = generate_task_breakdown(title, description)
                                st.markdown(breakdown)
                                if st.button("Close", key=f"close_breakdown_{task_id}"):
                                    st.session_state[f'show_breakdown_{task_id}'] = False
                                    st.rerun()
                            except Exception as e:
                                st.error(f"Error generating breakdown: {str(e)}")
                
                st.divider()
    else:
        st.info("No tasks found. Add a new task from the sidebar!")

with tab2:
    st.header("AI Task Breakdown Generator")
    st.write("Generate a detailed breakdown of any complex task using AI.")
    
    with st.form("breakdown_form"):
        breakdown_title = st.text_input("Task Title", placeholder="E.g., Build a mobile app")
        breakdown_description = st.text_area(
            "Task Description",
            placeholder="E.g., Create a fitness tracking mobile app with user authentication, workout logging, and progress charts"
        )
        
        if st.form_submit_button("Generate Breakdown"):
            if breakdown_title and breakdown_description:
                with st.spinner("AI is analyzing and breaking down your task..."):
                    try:
                        breakdown = generate_task_breakdown(breakdown_title, breakdown_description)
                        st.success("Task breakdown generated!")
                        st.markdown("---")
                        st.markdown(breakdown)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("Make sure your GEMINI_API_KEY is set in the .env file")
            else:
                st.warning("Please fill in both title and description")

with tab3:
    st.header("Email Reminder Settings")
    st.write("Configure automatic email reminders for upcoming tasks.")
    
    st.info("""
    **How Email Reminders Work:**
    - When you add a task with your email, you can send reminder emails manually
    - The AI generates personalized reminder emails based on your task details
    - Click 'Send Reminder' next to any task to get an AI-generated email reminder
    - Emails include task details, deadline urgency, and motivational content
    """)
    
    # Manual reminder test
    st.subheader("Email Reminder")
    
    with st.form("test_email_form"):
        test_email = st.text_input("Your Email", placeholder="your.email@example.com")
        test_task = st.text_input("Task Title", placeholder="Complete project report")
        
        if st.form_submit_button("Send Reminder"):
            if test_email and test_task:
                with st.spinner("Generating and sending reminder..."):
                    try:
                        email_content = generate_reminder_email(
                            test_task,
                            "This is a reminder email",
                            str((datetime.now() + timedelta(days=2)).date()),
                            "High"
                        )
                        success = send_reminder_email(test_email, test_task, email_content)
                        
                        if success:
                            st.success("Reminder sent successfully!")
                            st.info("Check your email inbox (and spam folder)")
                        else:
                            st.error("Failed to send email. Check your SMTP configuration in .env file")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please fill in all fields")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>AI-Powered Todo App | Built with Streamlit, SQLite & Gemini AI</p>
    </div>
""", unsafe_allow_html=True)
