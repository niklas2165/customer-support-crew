import requests
import logging
import sqlite3
import os
import time

DB_PATH = os.path.join("database", "support_emails.db")
API_URL = "https://customer-support-crew.onrender.com/new_email"

def run():
    logging.info("Email Ingestion Agent: Fetching new email...")

    max_retries = 3
    delay = 5  # initial delay in seconds

    email = None
    for attempt in range(max_retries):
        try:
            response = requests.get(API_URL, timeout=60)
            response.raise_for_status()
            email = response.json()
            logging.info(f"Email Ingestion Agent: Successfully fetched email on attempt {attempt + 1}.")
            break  # Exit loop on success
        except Exception as e:
            logging.warning(f"Email Ingestion Agent: Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # exponential backoff
            else:
                logging.error("Email Ingestion Agent: All retry attempts failed.")
                return None

    # Save to database if not already present
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
