import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def get_server_address(server):
    server_dict = {
        "AOL": "smtp.aol.com",
        "AT&T": "smtp.mail.att.net",
        "Comcast": "smtp.comcast.net",
        "iCloud": "smtp.comcast.net",
        "Gmail": "smtp.gmail.com",
        "Outlook": "smtp-mail.outlook.com",
        "Yahoo": "smtp.mail.yahoo.com"
    }

    return server_dict[server]


def send_email(sender_email, sender_password, recipient_email, subject, email_body,
               sender_friendly_name="Python Program", attachment_paths=[], server="Gmail"):
    """
    Send an email using the SMTP package.

    :param sender_email: Email address that the message is being sent from.
    :param sender_password: Email password for the sender's email address.
    :param recipient_email: Destination email address.
    :param subject: Subject line of the email.
    :param email_body: Body text of the email (plaintext or HTML).
    :param sender_friendly_name: Display name for the email sender.
    :param attachment_paths: (Optional) Paths to the desired attachment files.
    :param server: (Default="Gmail") Server to use for the mail delivery.
    :return: True (email sent) or False (email not sent).
    """

    # Get SMTP server from dictionary
    smtp_server = get_server_address(server)
    # SMTP port
    smtp_port = 587

    # Create a connectio to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Try sending the email
    try:
        # Login to the Gmail account
        server.login(sender_email, sender_password)

        # The email message
        email_message = MIMEMultipart()

        email_message['From'] = f'{sender_friendly_name} <{sender_email}>'
        email_message['To'] = recipient_email
        email_message['Subject'] = subject

        # Attach the message to the email.
        email_message.attach(MIMEText(email_body, 'html'))

        # If specified, attach the attachment to the email
        for attachment_file in attachment_paths:
            print(attachment_file)
            if attachment_file.endswith('.csv') or attachment_file.endswith('.txt'):
                attachment = MIMEApplication(open(attachment_file, 'r').read())
            else:
                attachment = MIMEApplication(open(attachment_file, 'rb').read())

            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_file))
            email_message.attach(attachment)

        # Send the email
        server.sendmail(sender_email, recipient_email, email_message.as_string())

        # Print success message
        print("Email sent successfully!")

        # Close the connection to the SMTP server
        server.quit()

        # Return a true value
        return True

    # Except an authentication error
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with Gmail account.")

        server.quit()
        return False

    # Except other errors (e.g. loss of WiFi, invalid options)
    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")

        server.quit()
        return False
