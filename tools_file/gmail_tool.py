import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime
import requests

def clean_text(text):
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    return text.replace('\n', ' ').replace('\r', '')

def parse_email_date(date_string):
    try:
        return parsedate_to_datetime(date_string)
    except:
        try:
            return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")
        except:
            return None

def get_emails(username, password, folder="inbox", server="imap.gmail.com", max_mails=10):
    mail = imaplib.IMAP4_SSL(server)
    emails = []
    try:
        mail.login(username, password)
        mail.select(folder)
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()[-max_mails:]

        for email_id in reversed(email_ids):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject = clean_text(decode_header(msg["Subject"])[0][0])
                    from_ = clean_text(decode_header(msg.get("From", ""))[0][0])
                    date = parse_email_date(msg.get("Date"))
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() in ["text/plain", "text/html"] and "attachment" not in str(part.get("Content-Disposition", "")):
                                try:
                                    body += clean_text(part.get_payload(decode=True))
                                except: pass
                    else:
                        body = clean_text(msg.get_payload(decode=True))

                    emails.append({
                        "id": email_id.decode(),
                        "from": from_,
                        "subject": subject,
                        "date": date.strftime("%Y-%m-%d %H:%M:%S") if date else "Unknown",
                        "body": (body[:2000] + "... [truncated]") if len(body) > 2000 else body
                    })

        mail.close()
        mail.logout()
        return emails

    except Exception as e:
        print(f"Error accessing emails: {str(e)}")
        try:
            mail.close()
            mail.logout()
        except: pass
        return []

def analyze_emails_with_llm(emails, model_name="llama2", prompt_template=None):
    if not prompt_template:
        prompt_template = """
        Please analyze the following emails and provide:
        1. A brief summary of each important email
        2. Any urgent items that need attention
        3. Categorize emails (work, personal, promotional, etc.)

        Here are the emails:
        {email_content}
        """

    email_content = "\n\n".join([
        f"Email {i+1}:\nFrom: {email['from']}\nSubject: {email['subject']}\nDate: {email['date']}\nBody: {email['body'][:300]}..."
        for i, email in enumerate(emails)
    ])

    prompt = prompt_template.format(email_content=email_content)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False}
        )
        if response.status_code == 200:
            return response.json().get("response", "No response from model.")
        else:
            return f"Error: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error calling Ollama: {str(e)}"
