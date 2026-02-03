# AI-Powered Todo Application

A sophisticated todo application built with Python, Streamlit, SQLite, and Google Gemini AI that helps you manage tasks efficiently with AI-powered features.

## Features

### Core Features
-  **Task Management**: Add, view, update, and delete tasks
-  **Deadline Tracking**: Set deadlines and get visual indicators for urgency
-  **Priority Levels**: Organize tasks by Low, Medium, or High priority
-  **Filter & Sort**: Filter by status and sort by deadline, priority, or date added
-  **Task Completion**: Mark tasks as complete with a simple checkbox

### AI-Powered Features (Using Gemini API)
-  **AI Task Breakdown**: Get intelligent breakdowns of complex tasks into manageable subtasks
-  **AI-Generated Email Reminders**: Receive personalized, context-aware reminder emails
-  **Smart Content**: AI analyzes your tasks and generates helpful, motivational content

### Email Features
-  **Automated Reminders**: Send reminder emails before task deadlines
-  **Professional Formatting**: HTML-formatted emails with attractive styling
-  **Configurable SMTP**: Easy email configuration for any SMTP provider

##  Installation

### Prerequisites
- Python 3.8 or higher
- A Google Gemini API key
- (Optional) An email account for sending reminders

### Step 1: Clone or Extract the Project
```bash
cd todo_app
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   ```

#### Getting a Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy the key to your `.env` file

#### Setting up Gmail for Email Reminders (Optional)
1. Enable 2-Factor Authentication on your Google account
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the app password in your `.env` file

### Step 4: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage Guide

### Adding a Task
1. Use the sidebar form to add a new task
2. Fill in:
   - Task title
   - Task description
   - Deadline date
   - Priority level
   - Your email (for reminders)
3. Click "Add Task"

### Managing Tasks
- **Mark Complete**: Click the checkbox next to any task
- **Delete Task**: Click the  Delete button
- **Send Reminder**: Click  to send an AI-generated reminder email
- **Task Breakdown**: Click  to get AI-powered subtask breakdown

### AI Task Breakdown
1. Go to the " AI Task Breakdown" tab
2. Enter a task title and description
3. Click "Generate Breakdown"
4. AI will provide:
   - Task analysis
   - Numbered subtasks
   - Time estimates
   - Dependencies
   - Success tips

### Email Reminders
- Manual: Click "Send Reminder" next to any task
- The AI generates a personalized email based on:
  - Task details
  - Deadline urgency
  - Priority level
- Emails are formatted professionally with HTML

## Project Structure

```
todo_app/
├── app.py                 # Main Streamlit application
├── database.py           # SQLite database operations
├── ai_features.py        # Gemini AI integration
├── email_sender.py       # Email sending functionality
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your actual credentials (not in repo)
├── todo_app.db          # SQLite database (auto-created)
└── README.md            # This file
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes |
| `SENDER_EMAIL` | Email for sending reminders | Optional |
| `SENDER_PASSWORD` | Email password/app password | Optional |
| `SMTP_SERVER` | SMTP server (default: smtp.gmail.com) | Optional |
| `SMTP_PORT` | SMTP port (default: 587) | Optional |

## Features in Detail

### Task Priority Color Coding
- 🟥 **High Priority**: Red indicator
- 🟧 **Medium Priority**: Orange indicator
- 🟦 **Low Priority**: Blue indicator

### Deadline Urgency Indicators
- 🔴 **Overdue**: Task deadline has passed
- 🟠 **Due Today**: Task is due today
- 🟡 **Due Soon**: Task due within 3 days
- 🟢 **On Track**: Task has more than 3 days

### AI Task Breakdown Example
For a task like "Build a mobile app", the AI will provide:
1. Analysis of the project scope
2. 5-8 specific subtasks (e.g., "Design UI mockups", "Set up backend")
3. Time estimates for each subtask
4. Dependencies between tasks
5. Pro tips for success

### AI Email Generation
The AI creates personalized emails that include:
- Friendly greeting
- Task reminder with context
- Urgency based on deadline
- Motivational message
- Encouraging sign-off

## Security Notes

1. **Never commit your `.env` file** - It contains sensitive credentials
2. **Use app-specific passwords** - Don't use your main email password
3. **Keep your API key private** - Don't share it or commit it to version control
4. The `.env.example` file shows the structure without real credentials

## Troubleshooting

### "GEMINI_API_KEY not configured"
- Make sure you've created a `.env` file 
- Verify your API key is correct
- Check that `.env` is in the same directory as `app.py`

### Email not sending
- Verify your email credentials in `.env`
- For Gmail, use an app-specific password
- Check that 2FA is enabled on your Google account
- Verify SMTP settings are correct

### Database errors
- The database is created automatically on first run
- Delete `todo_app.db` to reset the database
- Check file permissions in the project directory

## Assignment Requirements Checklist

 **Built with Python, SQLite, and Streamlit**
 **At least one AI feature using Gemini API**:
   - AI Task Breakdown
   - AI Email Generation
 **Additional Features**:
   - Email reminders before deadline
   - Deadline input required for tasks
   - Complex task breakdown using AI
 **Security**: API key not in source code (uses .env)


**Built using Streamlit, SQLite, and Google Gemini AI**
