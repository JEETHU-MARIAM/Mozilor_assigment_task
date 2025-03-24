import csv
import smtplib
from email.mime.text import MIMEText
import os
# Email Configuration (replace with your actual details)
#SENDER_EMAIL = "your_email@gmail.com"
#SENDER_PASSWORD = "your_email_password"
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")  
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(recipient_email, subject, body):
    """Sends an email using the configured email settings."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")


def send_emails_from_csv(csv_filename="website_approval.csv"):
    """Sends emails based on the approval status in the CSV file."""
    try:
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row['URL']
                email = row['Email']
                approval = row['Approval']

                if approval == "Approved":
                    subject = "Welcome!"
                    body = f"Congratulations! Your website {url} has been approved."
                elif approval == "Rejected":
                    subject = "Website Review Result"
                    body = f"Thank you for submitting your website {url} for review. Unfortunately, it did not meet our criteria."
                else:
                    print(f"Invalid approval status '{approval}' for {url}. Skipping.")
                    continue

                send_email(email, subject, body)

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filename}' not found.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")


if __name__ == "__main__":
    send_emails_from_csv()  # Or specify the CSV filename