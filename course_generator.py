import yaml
import os
import requests
import argparse
from rich.console import Console
from rich.markdown import Markdown
import resend
from datetime import datetime
import sys
from groq import Groq
import re

def load_config():
    """Load configuration from YAML file."""
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def save_master_prompt(prompt):
    """Save the master prompt to config.yaml."""
    config = load_config()
    config['content']['current_master_prompt'] = prompt
    
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)

CONFIG = load_config()

# Set API keys globally
resend.api_key = CONFIG['email']['api_key']
groq_client = Groq(api_key=CONFIG['groq']['api_key'])

def generate_master_subject_prompt(subject):
    """Generate a comprehensive prompt for a master subject using Groq API."""
    try:
        completion = groq_client.chat.completions.create(
            model=CONFIG['groq']['model'],
            messages=[
                {"role": "system", "content": CONFIG['groq']['system_prompt']},
                {"role": "user", "content": CONFIG['content']['master_subject_prompt'].format(subject=subject)}
            ]
        )
        return completion.choices[0].message.content
            
    except Exception as e:
        print(f"Error generating master subject prompt: {str(e)}")
        return None

def generate_course_content(master_prompt):
    """Generate a course on a random topic using the master prompt."""
    try:
        completion = groq_client.chat.completions.create(
            model=CONFIG['groq']['model'],
            messages=[
                {"role": "system", "content": CONFIG['groq']['system_prompt']},
                {"role": "user", "content": master_prompt}
            ]
        )
        return completion.choices[0].message.content
            
    except Exception as e:
        return f"""<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
<h1 style="color: red;">Error Generating Content</h1>
<p>Unfortunately, there was an error generating the content: {str(e)}</p>
<p>Please check your Groq API key and make sure it's valid.</p>
</body>
</html>"""

def send_course_email(html_content):
    """Send the generated course content via email using Resend."""
    try:
        # Extract the topic from the HTML content
        topic_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content)
        topic = topic_match.group(1) if topic_match else "Course Topic"
        
        # Truncate topic if it's too long
        max_topic_length = 50
        truncated_topic = topic[:max_topic_length] + "..." if len(topic) > max_topic_length else topic
        
        params = {
            "from": f"Course Generator <{CONFIG['email']['from_email']}>",
            "to": [CONFIG['email']['recipient_email']],
            "subject": f"{CONFIG['email']['subject_prefix']}: {truncated_topic}",
            "html": html_content
        }
        
        email = resend.Emails.send(params)
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def generate_course():
    """Generate a course using the master prompt from config."""
    if not CONFIG['email']['api_key'] or CONFIG['email']['api_key'] == "re_xxxxxxxxxxxx":
        console = Console()
        console.print("[red]Error: Resend API key not configured![/red]")
        console.print("Please update your config.yaml with your Resend API key.")
        return

    if not CONFIG['groq']['api_key'] or CONFIG['groq']['api_key'] == "gsk_xxxxx":
        console = Console()
        console.print("[red]Error: Groq API key not configured![/red]")
        console.print("Please update your config.yaml with your Groq API key.")
        return
        
    console = Console()
    
    # Get the master prompt from config
    master_prompt = CONFIG['content'].get('current_master_prompt')
    if not master_prompt:
        console.print("[red]Error: No master prompt found in config.yaml![/red]")
        console.print("First generate a master prompt using: python togaf_refresh.py --generate-prompt 'subject'")
        return
    
    # Generate the course content
    console.print("\n[blue]Generating course content...[/blue]")
    html_content = generate_course_content(master_prompt)
    
    # Create output directory if it doesn't exist
    os.makedirs(CONFIG['output']['directory'], exist_ok=True)
    
    # Get current date in configured format
    current_date = datetime.now().strftime(CONFIG['output']['date_format'])
    
    # Save to HTML file with date
    filename = os.path.join(
        CONFIG['output']['directory'],
        CONFIG['output']['filename_pattern'].format(date=current_date)
    )
    
    with open(filename, 'w') as f:
        f.write(html_content)
    
    console.print(f"\n[blue]Saved to: {filename}[/blue]\n")
    
    # Send email
    success, message = send_course_email(html_content)
    if success:
        console.print(f"[green]{message}[/green]")
    else:
        console.print(f"[red]{message}[/red]")

def test_email():
    """Test the email configuration by sending a test email."""
    console = Console()
    console.print("\n[yellow]Testing email configuration...[/yellow]")
    
    if not CONFIG['email']['api_key'] or CONFIG['email']['api_key'] == "re_xxxxxxxxxxxx":
        console.print("[red]Error: Resend API key not configured![/red]")
        console.print("Please update your config.yaml with your Resend API key.")
        return
        
    test_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Test Email</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #2c3e50;">Test Email</h1>
        <p>This is a test email from your course generator.</p>
        <h2 style="color: #2c3e50;">Current configuration:</h2>
        <ul>
            <li>From: {from_email}</li>
            <li>To: {recipient_email}</li>
            <li>API Key: {api_key_preview}...</li>
        </ul>
        <p>If you receive this email, your email configuration is working correctly!</p>
    </body>
    </html>
    """.format(
        from_email=CONFIG['email']['from_email'],
        recipient_email=CONFIG['email']['recipient_email'],
        api_key_preview=CONFIG['email']['api_key'][:10]
    )
    
    success, message = send_course_email(test_content)
    if success:
        console.print("[green]Test email sent successfully![/green]")
        console.print(f"Check your inbox at: {CONFIG['email']['recipient_email']}")
    else:
        console.print(f"[red]{message}[/red]")
        console.print("\nPlease check your configuration in config.yaml:")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate courses using AI with master prompts')
    parser.add_argument('--generate-prompt', type=str, help='Generate a master prompt for a subject (e.g., "TOGAF")')
    parser.add_argument('--test-email', action='store_true', help='Send a test email to verify email configuration')
    args = parser.parse_args()
    
    console = Console()
    
    if args.test_email:
        test_email()
    elif args.generate_prompt:
        # Generate and display the master prompt
        console.print(f"\n[blue]Generating master prompt for: {args.generate_prompt}[/blue]")
        master_prompt = generate_master_subject_prompt(args.generate_prompt)
        if master_prompt:
            console.print("[green]Master prompt generated successfully![/green]\n")
            console.print(Markdown(master_prompt))
            
            # Ask for user confirmation
            console.print("\n[yellow]Would you like to save this master prompt to config.yaml? (y/n)[/yellow]")
            response = input().lower().strip()
            
            if response == 'y':
                save_master_prompt(master_prompt)
                console.print("[green]Master prompt saved to config.yaml![/green]")
                console.print("\nYou can now generate courses by running:")
                console.print("python togaf_refresh.py")
            else:
                console.print("[yellow]Master prompt was not saved. You can try generating another one.[/yellow]")
    else:
        # Generate a course using the master prompt from config
        generate_course()
