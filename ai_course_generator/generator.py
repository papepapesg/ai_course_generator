"""Core course generation functionality."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from groq import Groq
from .utils.config import load_config, save_master_prompt
from .utils.email import send_course_email

def generate_master_subject_prompt(subject: str) -> Optional[str]:
    """Generate a comprehensive prompt for a master subject using Groq API."""
    try:
        config = load_config()
        client = Groq(api_key=config["groq"]["api_key"])
        
        completion = client.chat.completions.create(
            model=config["groq"]["model"],
            messages=[
                {"role": "system", "content": config["groq"]["system_prompt"]},
                {"role": "user", "content": config["content"]["master_subject_prompt"].format(subject=subject)}
            ]
        )
        
        prompt = completion.choices[0].message.content
        if prompt:
            save_master_prompt(prompt)
        return prompt
            
    except Exception as e:
        print(f"Error generating master subject prompt: {str(e)}")
        return None

def generate_course_content(master_prompt: str) -> Optional[str]:
    """Generate a course on a random topic using the master prompt."""
    try:
        config = load_config()
        client = Groq(api_key=config["groq"]["api_key"])
        
        completion = client.chat.completions.create(
            model=config["groq"]["model"],
            messages=[
                {"role": "system", "content": config["groq"]["system_prompt"]},
                {"role": "user", "content": master_prompt}
            ]
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating course content: {str(e)}")
        return None

def save_course_content(content: str) -> Optional[str]:
    """Save the course content to a file."""
    try:
        config = load_config()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(config["output"]["directory"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"course_{timestamp}.html"
        with open(output_file, "w") as f:
            f.write(content)
        
        return str(output_file)
    except Exception as e:
        print(f"Error saving course content: {str(e)}")
        return None

def generate_course() -> bool:
    """Generate a complete course and send it via email."""
    try:
        config = load_config()
        master_prompt = config["content"]["current_master_prompt"]
        if not master_prompt:
            print("No master prompt found. Please generate one first using --generate-prompt")
            return False
        
        content = generate_course_content(master_prompt)
        if not content:
            return False
        
        file_path = save_course_content(content)
        if not file_path:
            return False
        
        return send_course_email(content)
    except Exception as e:
        print(f"Error generating course: {str(e)}")
        return False
