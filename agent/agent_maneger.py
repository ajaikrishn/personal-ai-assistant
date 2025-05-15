import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tools_file 
from tools_file.gmail_tool import get_emails, analyze_emails_with_llm
from configure import EMAIL_USERNAME, EMAIL_PASSWORD, OLLAMA_MODEL

def run_assistant():
    print("Fetching emails...")
    emails = get_emails(EMAIL_USERNAME, EMAIL_PASSWORD, max_mails=10)

    if not emails:
        print("No emails found or error occurred.")
        return

    print(f"Found {len(emails)} recent emails.\nAnalyzing with Ollama...")
    analysis = analyze_emails_with_llm(emails, model_name=OLLAMA_MODEL)

    print("\nEmail Analysis:")
    print("=" * 50)
    print(analysis)   
def process_user_input(user_input):
    response = f"Echo: {user_input}"
    return response
