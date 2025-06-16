from jinja2 import Environment, FileSystemLoader

class EmailGenerator:
    """
    Generates HTML email content using Jinja2 templates.
    """
    def __init__(self, template_dir: str = "app/templates"):
        """
        Initializes the EmailGenerator with the path to the email templates.
        Args:
            template_dir (str): The directory where Jinja2 templates are located.
        """
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_email_html(self, data: dict) -> str:
        """
        Generates the HTML content for the email using 'email_template.html'.

        Args:
            data (dict): A dictionary containing data to populate the template.
                         Expected keys:
                         - 'recipient_name': First name of the recipient.
                         - 'company_name': Name of the recipient's company.
                         - 'business_summary': LLM-generated summary of the business.
                         - 'improvement_tips': List of LLM-generated improvement tips.
                         - 'email_body': LLM-generated main email body.
                         - 'sender_name': Name of the sender (e.g., Dave Chatpar).
                         - 'sender_company': Name of the sender's company (e.g., NetWit).
                         - 'reply_to_email': Email address for replies.

        Returns:
            str: The rendered HTML content of the email.
        """
        try:
            template = self.env.get_template("email_template.html")
            html_content = template.render(data)
            return html_content
        except Exception as e:
            print(f"Error rendering email template: {e}")
            return f"<p style='color: red;'>Error generating email: {e}</p>"

if __name__ == "__main__":
    # Example Usage
    email_gen = EmailGenerator()

    # Prepare mock data for the template
    mock_data = {
        "recipient_name": "John",
        "company_name": "Dada Auto Repair",
        "business_summary": "Dada Auto Repair is a family-owned shop specializing in engine diagnostics, brake repair, oil changes, and tire services, serving the community for over 30 years with a mission to provide honest and reliable auto repair.",
        "improvement_tips": [
            "Improve website mobile responsiveness for a better user experience.",
            "Optimize website loading speed to reduce bounce rates.",
            "Update the website design to a more modern aesthetic.",
            "Add a clear call-to-action on the homepage.",
            "Enhance SEO meta tags for better search engine visibility."
        ],
        "email_body": (
            "Hi John,\n\n"
            "I was browsing the Dada Auto Repair website and was impressed by your long-standing commitment to providing honest and reliable auto repair services in the community. It's clear you have a strong foundation.\n\n"
            "While exploring, I noticed a few areas where your online presence could be further enhanced to attract even more customers and streamline your operations. For example, enhancing mobile responsiveness and optimizing site loading speed could significantly improve user experience.\n\n"
            "We specialize in helping businesses like yours refine their digital footprint to drive growth. Would you be open to a brief chat next week to explore how we can help Dada Auto Repair shine even brighter online?\n\n"
            "Looking forward to hearing from you."
        ),
        "sender_name": "Dave Chatpar",
        "sender_company": "NetWit",
        "reply_to_email": "dave@netwit.ca"
    }

    generated_html = email_gen.generate_email_html(mock_data)
    print("\n--- Generated HTML Email (preview) ---")
    # In a real scenario, you'd save this to a .html file or send it.
    # For demonstration, printing a snippet or the whole thing.
    print(generated_html[:1000]) # Print first 1000 characters
    print("\n...\n")
    print(generated_html[-500:]) # Print last 500 characters
