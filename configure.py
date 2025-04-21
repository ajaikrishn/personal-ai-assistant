from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
import imaplib as imap
import email
from email.header import decode_header
from datetime import datetime
import anthropic


model = OllamaLLM(model="llama2")
# scope=['https://www.googleapis.com/auth/gmail.readonly']


def clean_text(text):
    # Check if the input is bytes, decode it; otherwise, assume it's already a string
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    # Remove any unwanted characters or formatting
    cleaned_text = text.replace('\n', ' ').replace('\r', '')
    return cleaned_text

def parse_email_date(date_string):
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(date_string)
    except:
        try:
            return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
        except:
            return None

def get_emails(username,password,folder="inbox",server="imap.gmail.com",max_mails=10):
    mail= imap.IMAP4_SSL(server)
    try:
        mail.login(username,password)
        mail.select(folder)
        status, messages= mail.search(None, 'ALL')
        email_ids= messages[0].split()
        start_index= max(0, len(email_ids) - max_mails)
        recent_email_ids= email_ids[start_index:]
        emails= []
   # Fetch each email and extract details
        for email_id in reversed(recent_email_ids):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    
                    # Extract subject
                    subject = decode_header(msg["Subject"])[0][0]
                    subject = clean_text(subject)
                    
                    # Extract sender
                    from_ = decode_header(msg.get("From", ""))[0][0]
                    from_ = clean_text(from_)
                    
                    # Extract date
                    date_str = msg.get("Date")
                    date = parse_email_date(date_str)
                    
                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            # Skip attachments
                            if "attachment" in content_disposition:
                                continue
                            
                            # Get text content
                            if content_type == "text/plain" or content_type == "text/html":
                                try:
                                    body_part = part.get_payload(decode=True)
                                    body += clean_text(body_part)
                                except:
                                    pass
                    else:
                        # Handle non-multipart messages
                        payload = msg.get_payload(decode=True)
                        body = clean_text(msg.get_payload(decode=True))
                    
                    # Limit body length to prevent very large inputs to LLM
                    if len(body) > 2000:
                        body = body[:2000] + "... [truncated]"
                    
                    emails.append({
                        "id": email_id.decode(),
                        "from": from_,
                        "subject": subject,
                        "date": date.strftime("%Y-%m-%d %H:%M:%S") if date else "Unknown",
                        "body": body
                    })
        
        # Close the connection
        mail.close()
        mail.logout()
        
        return emails
    except Exception as e:
        print(f"Error accessing emails: {str(e)}")
        # Make sure to close the connection on error
        try:
            mail.close()
            mail.logout()
        except:
            pass
        return []

def analyze_emails_with_llm(emails, model_name=model, prompt_template=None):
    """Analyze emails using Ollama LLM."""
    import requests
    import json
    
    if not prompt_template:
        prompt_template = """
        Please analyze the following emails and provide:
        1. A brief summary of each important email
        2. Any urgent items that need attention
        3. Categorize emails (work, personal, promotional, etc.)
        
        Here are the emails:
        {email_content}
        """
    
    # Prepare email content for the LLM
    email_content = "\n\n".join([
        f"Email {i+1}:\nFrom: {email['from']}\nSubject: {email['subject']}\nDate: {email['date']}\nBody: {email['body'][:300]}..."
        for i, email in enumerate(emails)
    ])
    
    # Complete the prompt
    prompt = prompt_template.format(email_content=email_content)
    
    # Send to Ollama for analysis
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error analyzing emails with Ollama: {str(e)}"




def main():
    # Configuration - replace with your actual credentials
    EMAIL_USERNAME = "ajaikrishna114@gmail.com"  
    EMAIL_PASSWORD = "uyuz kxau hrko oabg "  # For Gmail, use an App Password
    OLLAMA_MODEL = "llama2"  # or whatever model you're using with Ollama
    
    # Get emails
    print("Fetching emails...")
    emails = get_emails(EMAIL_USERNAME, EMAIL_PASSWORD, max_mails=10)
    
    if not emails:
        print("No emails found or error occurred.")
        return
    
    print(f"Found {len(emails)} recent emails.")
    
    # Analyze emails with Ollama
    print("Analyzing emails with Ollama...")
    analysis = analyze_emails_with_llm(emails, model_name=OLLAMA_MODEL)
    
    # Print results
    print("\nEmail Analysis:")
    print("=" * 50)
    print(analysis)

if __name__ == "__main__":
    main()



# def authenticate_gmail():
#     creds= None
#     if os.path.exists('token.json'):
#         creds= Credentials.from_authorized_user_file('token.json', scope)





