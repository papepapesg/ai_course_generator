"""Command-line interface for the AI Course Generator."""

import argparse
from .generator import generate_master_subject_prompt, generate_course
from .utils.email import test_email
from rich.console import Console

console = Console()

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Generate courses using AI with master prompts')
    parser.add_argument('--generate-prompt', type=str, 
                       help='Generate a master prompt for a subject (e.g., "TOGAF")')
    parser.add_argument('--test-email', action='store_true', 
                       help='Send a test email to verify email configuration')
    args = parser.parse_args()

    try:
        if args.generate_prompt:
            prompt = generate_master_subject_prompt(args.generate_prompt)
            if prompt:
                console.print("[green]✓[/green] Master prompt generated successfully!")
                console.print(prompt)
            else:
                console.print("[red]✗[/red] Failed to generate master prompt.")
                return 1
        elif args.test_email:
            if test_email():
                console.print("[green]✓[/green] Test email sent successfully!")
            else:
                console.print("[red]✗[/red] Failed to send test email.")
                return 1
        else:
            if generate_course():
                console.print("[green]✓[/green] Course generated and sent successfully!")
            else:
                console.print("[red]✗[/red] Failed to generate course.")
                return 1
        return 0
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
