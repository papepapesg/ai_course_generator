"""Email utilities for sending course content."""

import resend
from datetime import datetime
from pathlib import Path
from typing import Optional
from .config import load_config

def send_course_email(html_content: str) -> bool:
    """Send the generated course content via email using Resend."""
    try:
        config = load_config()
        resend.api_key = config["email"]["api_key"]
        
        params = {
            "from": config["email"]["from_email"],
            "to": config["email"]["recipient_email"],
            "subject": f"Your AI-Generated Course - {datetime.now().strftime('%Y-%m-%d')}",
            "html": html_content
        }
        
        response = resend.Emails.send(params)
        return bool(response.id)
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def test_email() -> bool:
    """Send a test email to verify email configuration."""
    try:
        html_content = """
        <h1>AI Course Generator - Test Email</h1>
        <p>If you're receiving this email, your email configuration is working correctly!</p>
        <p>You can now use the AI Course Generator to create and receive courses.</p>
        """
        return send_course_email(html_content)
    except Exception as e:
        print(f"Error sending test email: {str(e)}")
        return False
