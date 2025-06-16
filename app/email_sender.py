import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

class EmailSender:
    """
    Handles sending HTML emails via SMTP.
    """
    def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str):
        """
        Initializes the EmailSender with SMTP server details.
        Args:
            smtp_server (str): The SMTP server address (e.g., 'smtp.gmail.com').
            smtp_port (int): The SMTP server port (e.g., 587 for TLS, 465 for SSL).
            smtp_username (str): The username for SMTP authentication (your email address).
            smtp_password (str): The password or app-specific password for SMTP authentication.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_email(self, sender_email: str, recipient_email: str, reply_to_email: str, subject: str, html_content: str):
        """
        Sends an HTML email.
        Args:
            sender_email (str): The email address from which the email will be sent.
            recipient_email (str): The email address to which the email will be sent.
            reply_to_email (str): The email address for replies.
            subject (str): The subject line of the email.
            html_content (str): The HTML content of the email body.
        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg["Reply-To"] = reply_to_email

        # Attach HTML content
        part1 = MIMEText(html_content, "html")
        msg.attach(part1)

        try:
            print(f"Attempting to send email to {recipient_email} from {sender_email}...")
            # Create a secure SSL context
            context = ssl.create_default_context()

            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context) # Secure the connection
                server.ehlo()  # Can be omitted

                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())

            print(f"Email successfully sent to {recipient_email}.")
            return True
        except smtplib.SMTPAuthenticationError:
            print(f"SMTP Authentication Error: Failed to log in to the SMTP server. "
                  f"Check username, password, or app-specific password (for Gmail).")
            return False
        except smtplib.SMTPConnectError as e:
            print(f"SMTP Connection Error: Could not connect to the SMTP server '{self.smtp_server}' on port {self.smtp_port}. "
                  f"Check server address, port, and network connectivity. Error: {e}")
            return False
        except smtplib.SMTPException as e:
            print(f"An SMTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while sending email: {e}")
            return False

if __name__ == "__main__":
    # This block would typically load from .env, but for standalone test, define here.
    # In a real application, ensure these are loaded securely.
    _SMTP_SERVER = "smtp.gmail.com" # Replace with your SMTP server
    _SMTP_PORT = 587
    _SMTP_USERNAME = "your_email@example.com" # Replace with your email
    _SMTP_PASSWORD = "your_app_password" # Replace with your app password/email password

    _SENDER_EMAIL = "noreply@example.com" # Replace with your sender email
    _REPLY_TO_EMAIL = "your_reply_to_email@example.com" # Replace with your reply-to email
    _TEST_RECEIVER_EMAIL = "test_recipient@example.com" # Replace with a real recipient for testing

    if _SMTP_USERNAME == "your_email@example.com" or _SMTP_PASSWORD == "your_app_password":
        print("Please configure your SMTP details in email_sender.py (or .env) for testing.")
    else:
        email_sender = EmailSender(
            smtp_server=_SMTP_SERVER,
            smtp_port=_SMTP_PORT,
            smtp_username=_SMTP_USERNAME,
            smtp_password=_SMTP_PASSWORD
        )

        test_subject = "Test Personalized Website Review"
        test_html_content = """
        <html>
        <body>
            <h1>Hello from the Email Automation App!</h1>
            <p>This is a test email sent from your application.</p>
            <p>If you received this, your SMTP configuration is likely working.</p>
            <p>Best regards,<br>Your App</p>
        </body>
        </html>
        """
        print("\n--- Sending test email ---")
        success = email_sender.send_email(
            sender_email=_SENDER_EMAIL,
            recipient_email=_TEST_RECEIVER_EMAIL,
            reply_to_email=_REPLY_TO_EMAIL,
            subject=test_subject,
            html_content=test_html_content
        )
        if success:
            print("Test email sent successfully!")
        else:
            print("Failed to send test email. Check console for errors.")
