import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """
    Manages SQLite database operations for logging email processing.
    """
    def __init__(self, db_name: str = 'email_automation.db'):
        """
        Initializes the DatabaseManager.
        Args:
            db_name (str): The name of the SQLite database file.
        """
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self._create_table()
        print(f"Database initialized at: {self.db_path}")

    def _get_connection(self):
        """
        Establishes and returns a database connection.
        """
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        """
        Creates the 'processed_emails' table if it doesn't already exist.
        This table will store logs of each email processing attempt.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_email TEXT NOT NULL,
                    recipient_email_sent_to TEXT,
                    company_domain TEXT,
                    email_subject TEXT,
                    status TEXT NOT NULL, -- 'success' or 'failed'
                    error_message TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("Table 'processed_emails' ensured to exist.")

    def log_email_processing(self,
                             original_email: str,
                             recipient_email_sent_to: str,
                             company_domain: str,
                             email_subject: str,
                             status: str,
                             error_message: str = None):
        """
        Logs the outcome of an email processing attempt to the database.

        Args:
            original_email (str): The email address from the input file/request.
            recipient_email_sent_to (str): The actual email address the email was sent to (e.g., TEST_RECEIVER_EMAIL).
            company_domain (str): The domain extracted from the email.
            email_subject (str): The subject line of the generated email.
            status (str): The status of the processing ('success' or 'failed').
            error_message (str, optional): Any error message if the status is 'failed'. Defaults to None.
        """
        timestamp = datetime.now().isoformat()
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO processed_emails (
                        original_email, recipient_email_sent_to, company_domain,
                        email_subject, status, error_message, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (original_email, recipient_email_sent_to, company_domain,
                      email_subject, status, error_message, timestamp))
                conn.commit()
                print(f"Logged email processing: {original_email} - Status: {status}")
        except Exception as e:
            print(f"Error logging email processing for {original_email}: {e}")

    def get_all_logs(self):
        """
        Retrieves all processed email logs from the database.

        Returns:
            list: A list of dictionaries, where each dictionary represents a log entry.
        """
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row # Allows accessing columns by name
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM processed_emails ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

if __name__ == "__main__":
    # Example Usage:
    # This will create email_automation.db in the app directory if it doesn't exist
    db_manager = DatabaseManager()

    print("\n--- Logging successful email ---")
    db_manager.log_email_processing(
        original_email="test.success@example.com",
        recipient_email_sent_to="your.test@receiver.com",
        company_domain="example.com",
        email_subject="Your Website Review",
        status="success"
    )

    print("\n--- Logging failed email ---")
    db_manager.log_email_processing(
        original_email="another.fail@bad-domain.com",
        recipient_email_sent_to="your.test@receiver.com",
        company_domain="bad-domain.com",
        email_subject="Your Website Review (Failed)",
        status="failed",
        error_message="Web scraping failed for bad-domain.com"
    )

    print("\n--- Retrieving all logs ---")
    logs = db_manager.get_all_logs()
    for log in logs:
        print(log)

    print("\n--- Demonstrating log after multiple runs (if db file persists) ---")
    # If you run this multiple times, it will keep adding logs.
    # To reset for testing, delete 'email_automation.db' file.
