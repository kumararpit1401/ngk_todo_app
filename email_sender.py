import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_reminder_email(recipient_email, task_title, email_body):
    """
    Send a reminder email to the specified recipient
    
    Args:
        recipient_email: Email address of the recipient
        task_title: Title of the task (used in subject)
        email_body: The content of the email (AI-generated)
    
    Returns:
        True if email sent successfully, False otherwise
    """
    # Get SMTP configuration from environment variables
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    
    # Check if credentials are configured
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Warning: Email credentials not configured in .env file")
        return False
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"⏰ Task Reminder: {task_title}"
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        
        # Create plain text and HTML versions
        text = email_body
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
              <h2 style="color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 10px;">
                📋 Task Reminder
              </h2>
              <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                {email_body.replace(chr(10), '<br>')}
              </div>
              <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
                <p style="font-size: 12px;">
                  This is an automated reminder from your AI-Powered Todo App
                </p>
              </div>
            </div>
          </body>
        </html>
        """
        
        # Attach both versions
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        
        print(f"Email sent successfully to {recipient_email}")
        return True
    
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your email and password")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def test_email_configuration():
    """
    Test if email configuration is properly set up
    
    Returns:
        True if configuration is valid, False otherwise
    """
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return False
    
    return True
