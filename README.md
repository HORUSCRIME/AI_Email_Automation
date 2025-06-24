# 📧 Intelligent Email Automation Application

## 🚀 Project Objective

Build an intelligent, automated application that:
- Accepts a list of email addresses via file upload,
- Extracts personalized business data by scraping company websites,
- Uses an LLM to generate customized, engaging HTML emails,
- Sends those emails via SMTP,
- Logs all attempts to an SQLite database for auditing and tracking.

---

## 🧩 Core Features & Functional Workflow

### ✅ Web-based File Upload UI
- Upload `.csv`, `.xlsx`, `.xls`, or `.txt` files through a friendly web interface.

### ✅ Email List Handling
- Parses email addresses and infers:
  - `first_name`, `last_name`, `full_name`, `domain`
  - Uses NLP-style logic to ensure human-friendly formatting.

### ✅ Website Scraping Module
- Extracts company info from the homepage using the email domain.
- Identifies:
  - Company summary (via metadata, headers, content)
  - Simulated issues (SEO, SSL, speed, mobile-friendliness, etc.)

### ✅ LLM-driven Personalized Content Generation
- Uses `llama free turbo from together.ai` locally to:
  - Summarize business activity
  - Generate 3–5 tailored improvement suggestions
  - Craft a unique email with insights, congratulations, and CTA

### ✅ HTML Email Generation
- Uses `Jinja2` templating for modern, responsive emails.
- Injects personalized tips and recipient details into a clean HTML layout.

### ✅ Email Delivery Integration
- Sends emails via `sendgrid api` and sendgrid api credentials.
- Configurable sender, reply-to, and test recipient in `.env`.

### ✅ Processing Log (SQLite Database)
- Logs:
  - Original email, recipient, company domain, subject
  - Status, error message (if any), and timestamp
- View logs via `/logs` API.

---

## 🛠️ Tech Stack

| Component              | Technology/Tool             |
|------------------------|-----------------------------|
| Backend Framework      | Python (FastAPI)            |
| Web Scraping           | BeautifulSoup + requests    |
| LLM Integration        | Llama turbo free together.ai|
| Email Generation       | Jinja2 + HTML Template      |
| Email Sending          | Python `smtplib` `sendgrid api`|
| File Uploads           | `python-multipart`, `openpyxl` |
| Environment Mgmt       | `python-dotenv`             |
| Storage                | SQLite3                     |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
bash
git clone <repository-url-here>
cd email_automation_app

2. Create and Activate Virtual Environment
bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

3. Install Dependencies
bash
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root directory:
env

# Optional (for Hugging Face API)
# HUGGING_FACE_API_KEY="YOUR_API_KEY"
# HUGGING_FACE_MODEL_NAME="distilgpt2"

# SMTP Settings
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="your_email@example.com"
SMTP_PASSWORD="your_email_app_password"

SENDER_EMAIL="noreply@yourdomain.com"
REPLY_TO_EMAIL="your_reply_to_email@example.com"

TOGETHER_API_KEY="place your together.ai key"
SENDGRID_API_KEY="place your sendgrid api key"



# Testing Recipient
TEST_RECEIVER_EMAIL="your_actual_test_recipient@example.com"
💡 Note: For Gmail + 2FA, generate an "App Password" in your Google Account.

▶️ How to Run
uvicorn main:app --reload
