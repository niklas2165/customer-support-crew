import requests
import logging
import sqlite3
import os

DB_PATH = os.path.join("database", "support_emails.db")
API_URL = "https://customer-support-crew.onrender.com/new_email"

def run():
    logging.info("Email Ingestion Agent: Fetching new email...")

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        email = response.json()
        logging.info("Email Ingestion Agent: Fetched email from API.")
    except Exception as e:
        logging.error(f"Email Ingestion Agent: Error fetching email: {e}")
        return None

    # Save to DB if it doesn't exist
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM support_emails WHERE email_id = ?", (email["email_id"],))
    if not cur.fetchone():
        cur.execute(
            """
            INSERT INTO support_emails (email_id, timestamp, sender, subject, body)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                email["email_id"],
                email["timestamp"],
                email["sender"],
                email["subject"],
                email["body"],
            ),
        )
        conn.commit()
        logging.info("Email Ingestion Agent: Inserted new email into DB.")
    else:
        logging.info("Email Ingestion Agent: Email already exists in DB.")

    conn.close()
    return email
