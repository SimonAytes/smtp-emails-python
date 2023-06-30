import send_emails as email
from dotenv import load_dotenv
import os

is_env_loaded = load_dotenv()

if not is_env_loaded:
    print("ERROR loading dotenv. Quitting now...")
    quit()

if __name__ == "__main__":
    email.send_email(sender_email=os.getenv("SENDER_EMAIL"),
                     sender_password=os.getenv("SENDER_PASSWORD"),
                     recipient_email="simon@aytes.net",
                     subject="Test email with multiple attachments",
                     email_body="Hello world!",
                     sender_friendly_name="Python Program",
                     attachment_paths=["./test_attachments/TXT.txt"],
                     server="Gmail")

