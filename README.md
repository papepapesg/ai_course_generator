# AI Course Generator

![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An AI-powered educational content generator that creates comprehensive, beautifully formatted courses on any subject.

> ⚠️ **Note**: This project is no longer actively maintained. Feel free to fork and adapt it for your needs.

## Service Dependencies

This project requires API keys from the following services:

- [Groq](https://groq.com/) - LLM API provider for course content generation
  - Requires a paid API key
  - Uses the Mixtral-8x7B model
  - Pricing: See [Groq's pricing page](https://groq.com/pricing)

- [Resend](https://resend.com/) - Email delivery service
  - Requires a paid API key
  - Needs a verified sender domain/email
  - Free tier available: 100 emails/day
  - Pricing: See [Resend's pricing page](https://resend.com/pricing)

## Features

- Generate courses on any subject using Groq's Mixtral-8x7B model
- Professional HTML email output with consistent styling
- Automatic email delivery via Resend
- Flexible configuration system
- Comprehensive error handling

## Prerequisites

- Python 3.8+
- Groq API key
- Resend API key and verified sender email

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai_course_generator.git
cd ai_course_generator
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Copy the example environment file and configure your settings:
```bash
cp example.env .env
```

Edit `.env` with your API keys and settings.

## Configuration

The project uses both a `config.yaml` file and environment variables (through `.env`):

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key
- `RESEND_API_KEY`: Your Resend API key
- `SENDER_EMAIL`: Verified sender email for Resend
- `RECIPIENT_EMAIL`: Default recipient email

### config.yaml
The `config.yaml` file contains:
- Model settings
- System prompts
- Email templates
- Course generation parameters

## Usage

1. Generate a master prompt for your subject:
```bash
python course_generator.py --generate-prompt "Your Subject"
```

2. Generate a course:
```bash
python course_generator.py
```

3. Test email configuration:
```bash
python course_generator.py --test-email
```

## Output

- Generated courses are saved in the `generated_courses` directory
- Each course is saved as an HTML file with timestamp
- Courses are automatically sent via email

## Development

### Project Structure
```
ai_course_generator/
├── ai_course_generator/       # Main package directory
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Command-line interface
│   ├── generator.py          # Course generation logic
│   ├── utils/                # Utility functions
│   └── templates/            # Email templates
├── tests/                    # Test directory
├── .env                      # Environment variables (not in git)
├── config.yaml              # Configuration file
├── example.env              # Example environment file
├── requirements.txt         # Project dependencies
├── setup.py                # Package setup file
└── README.md               # This file
```

### Running Tests
```bash
python -m pytest
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Groq](https://groq.com/) for their powerful LLM API
- [Resend](https://resend.com/) for email delivery

## Dependencies

- groq==0.12.0
- PyYAML==6.0.1
- resend==0.6.0
- rich==13.4.2
