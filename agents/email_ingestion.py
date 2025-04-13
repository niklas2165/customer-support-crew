import requests
import logging
import sqlite3
import os

DB_PATH = os.path.join("database", "support_emails.db")
API_URL = "https://customer-support-crew.onrender.com/new_email"

def run():
    logging.info("Email Ingestion Agent: Fetching new email...")

    try:
        response = requests.get(API_URL, timeout=60)
        response.raise_for_status()
        email = response.json()
        logging.info("Email Ingestion Agent: Fetched email from API.")
    except Exception as e:
        logging.error(f"Email Ingestion Agent: Error fetching email: {e}")
        return None

    # Always insert a new row with a new email_id, even if content is reused
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Determine next available email_id
    cur.execute("SELECT MAX(email_id) FROM support_emails")
    max_id = cur.fetchone()[0] or 0
    new_id = max_id + 1

    cur.execute(
        """
        INSERT INTO support_emails (email_id, timestamp, sender, subject, body)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            new_id,
            email["timestamp"],
            email["sender"],
            email["subject"],
            email["body"],
        ),
    )
    conn.commit()
    conn.close()

    logging.info(f"Email Ingestion Agent: Inserted email with new ID {new_id}.")

    # Ensure downstream agents receive the new ID
    email["email_id"] = new_id
    return email
