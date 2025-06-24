# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import ssl

# class EmailSender:
#     """
#     Handles sending HTML emails via SMTP.
#     """
#     def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str):
#         """
#         Initializes the EmailSender with SMTP server details.
#         Args:
#             smtp_server (str): The SMTP server address (e.g., 'smtp.gmail.com').
#             smtp_port (int): The SMTP server port (e.g., 587 for TLS, 465 for SSL).
#             smtp_username (str): The username for SMTP authentication (your email address).
#             smtp_password (str): The password or app-specific password for SMTP authentication.
#         """
#         self.smtp_server = smtp_server
#         self.smtp_port = smtp_port
#         self.smtp_username = smtp_username
#         self.smtp_password = smtp_password

#     def send_email(self, sender_email: str, recipient_email: str, reply_to_email: str, subject: str, html_content: str):
#         """
#         Sends an HTML email.
#         Args:
#             sender_email (str): The email address from which the email will be sent.
#             recipient_email (str): The email address to which the email will be sent.
#             reply_to_email (str): The email address for replies.
#             subject (str): The subject line of the email.
#             html_content (str): The HTML content of the email body.
#         Returns:
#             bool: True if the email was sent successfully, False otherwise.
#         """
#         msg = MIMEMultipart("alternative")
#         msg["From"] = sender_email
#         msg["To"] = recipient_email
#         msg["Subject"] = subject
#         msg["Reply-To"] = reply_to_email

#         # Attach HTML content
#         part1 = MIMEText(html_content, "html")
#         msg.attach(part1)

#         try:
#             print(f"Attempting to send email to {recipient_email} from {sender_email}...")
#             # Create a secure SSL context
#             context = ssl.create_default_context()

#             # Connect to the SMTP server
#             with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
#                 server.ehlo()  # Can be omitted
#                 server.starttls(context=context) # Secure the connection
#                 server.ehlo()  # Can be omitted

#                 server.login(self.smtp_username, self.smtp_password)
#                 server.sendmail(sender_email, recipient_email, msg.as_string())

#             print(f"Email successfully sent to {recipient_email}.")
#             return True
#         except smtplib.SMTPAuthenticationError:
#             print(f"SMTP Authentication Error: Failed to log in to the SMTP server. "
#                   f"Check username, password, or app-specific password (for Gmail).")
#             return False
#         except smtplib.SMTPConnectError as e:
#             print(f"SMTP Connection Error: Could not connect to the SMTP server '{self.smtp_server}' on port {self.smtp_port}. "
#                   f"Check server address, port, and network connectivity. Error: {e}")
#             return False
#         except smtplib.SMTPException as e:
#             print(f"An SMTP error occurred: {e}")
#             return False
#         except Exception as e:
#             print(f"An unexpected error occurred while sending email: {e}")
#             return False

# if __name__ == "__main__":
#     # This block would typically load from .env, but for standalone test, define here.
#     # In a real application, ensure these are loaded securely.
#     _SMTP_SERVER = "smtp.gmail.com" # Replace with your SMTP server
#     _SMTP_PORT = 587
#     _SMTP_USERNAME = "your_email@example.com" # Replace with your email
#     _SMTP_PASSWORD = "your_app_password" # Replace with your app password/email password

#     _SENDER_EMAIL = "noreply@example.com" # Replace with your sender email
#     _REPLY_TO_EMAIL = "your_reply_to_email@example.com" # Replace with your reply-to email
#     _TEST_RECEIVER_EMAIL = "test_recipient@example.com" # Replace with a real recipient for testing

#     if _SMTP_USERNAME == "your_email@example.com" or _SMTP_PASSWORD == "your_app_password":
#         print("Please configure your SMTP details in email_sender.py (or .env) for testing.")
#     else:
#         email_sender = EmailSender(
#             smtp_server=_SMTP_SERVER,
#             smtp_port=_SMTP_PORT,
#             smtp_username=_SMTP_USERNAME,
#             smtp_password=_SMTP_PASSWORD
#         )

#         test_subject = "Test Personalized Website Review"
#         test_html_content = """
#         <html>
#         <body>
#             <h1>Hello from the Email Automation App!</h1>
#             <p>This is a test email sent from your application.</p>
#             <p>If you received this, your SMTP configuration is likely working.</p>
#             <p>Best regards,<br>Your App</p>
#         </body>
#         </html>
#         """
#         print("\n--- Sending test email ---")
#         success = email_sender.send_email(
#             sender_email=_SENDER_EMAIL,
#             recipient_email=_TEST_RECEIVER_EMAIL,
#             reply_to_email=_REPLY_TO_EMAIL,
#             subject=test_subject,
#             html_content=test_html_content
#         )
#         if success:
#             print("Test email sent successfully!")
#         else:
#             print("Failed to send test email. Check console for errors.")



import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import ssl # Although not directly used for SendGrid API, kept for context of previous SSL usage

class EmailSender:
    """
    Handles sending HTML emails via SendGrid API.
    """
    def __init__(self, sendgrid_api_key: str = None):
        """
        Initializes the EmailSender with SendGrid API key.
        Args:
            sendgrid_api_key (str): Your SendGrid API key. If not provided,
                                    it will try to fetch from the `SENDGRID_API_KEY` environment variable.
        """
        self.sendgrid_api_key = sendgrid_api_key if sendgrid_api_key else os.getenv("SENDGRID_API_KEY")

        if not self.sendgrid_api_key:
            print("Warning: SENDGRID_API_KEY not found. Please set the environment variable or pass it to the constructor.")
            self.email_sender_available = False
            return

        try:
            self.sg = sendgrid.SendGridAPIClient(self.sendgrid_api_key)
            self.email_sender_available = True
            print("SendGrid EmailSender initialized.")
        except Exception as e:
            print(f"Error initializing SendGrid API client: {e}")
            self.email_sender_available = False

    def send_email(self, sender_email: str, recipient_email: str, reply_to_email: str, subject: str, html_content: str):
        """
        Sends an HTML email using the SendGrid API.
        Args:
            sender_email (str): The verified sender email address in SendGrid.
            recipient_email (str): The email address to which the email will be sent.
            reply_to_email (str): The email address for replies.
            subject (str): The subject line of the email.
            html_content (str): The HTML content of the email body.
        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        if not self.email_sender_available:
            return "EmailSender not initialized due to missing API key."

        # Create a Mail object
        message = Mail(
            from_email=Email(sender_email),
            to_emails=To(recipient_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        # Add reply-to header
        message.reply_to = Email(reply_to_email)

        try:
            print(f"Attempting to send email to {recipient_email} from {sender_email} using SendGrid...")
            response = self.sg.send(message)

            if response.status_code >= 200 and response.status_code < 300:
                print(f"Email successfully sent to {recipient_email}. Status Code: {response.status_code}")
                # print(f"Response Body: {response.body}") # Uncomment for debugging
                # print(f"Response Headers: {response.headers}") # Uncomment for debugging
                return True
            else:
                print(f"Failed to send email. Status Code: {response.status_code}")
                print(f"Response Body: {response.body}")
                return False
        except Exception as e:
            print(f"An error occurred while sending email with SendGrid: {e}")
            return False

if __name__ == "__main__":
    # IMPORTANT: Set your SendGrid API key as an environment variable
    # Example (in your shell): export SENDGRID_API_KEY="SG.YOUR_SENDGRID_API_KEY_HERE"
    # Or pass it directly to the constructor: email_sender = EmailSender(sendgrid_api_key="SG.YOUR_SENDGRID_API_KEY_HERE")

    # For testing, ensure these values are configured or loaded from .env
    # The sender_email MUST be a verified sender in your SendGrid account.
    _SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    _SENDER_EMAIL = "your_verified_sender@example.com" # Replace with your SendGrid verified sender email
    _REPLY_TO_EMAIL = "your_reply_to_email@example.com" # Replace with your reply-to email
    _TEST_RECEIVER_EMAIL = "test_recipient@example.com" # Replace with a real recipient for testing

    if not _SENDGRID_API_KEY or _SENDER_EMAIL == "your_verified_sender@example.com":
        print("Please configure your SENDGRID_API_KEY and _SENDER_EMAIL for testing.")
    else:
        email_sender = EmailSender(sendgrid_api_key=_SENDGRID_API_KEY)

        if email_sender.email_sender_available:
            test_subject = "Test Personalized Website Review via SendGrid"
            test_html_content = """
            <html>
            <body>
                <h1>Hello from the Email Automation App!</h1>
                <p>This is a test email sent from your application using SendGrid.</p>
                <p>If you received this, your SendGrid configuration is likely working.</p>
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
        else:
            print("EmailSender could not be initialized. Check console for details.")

