import requests
import logging
import json

def run():
    """
    Fetch a new email from the FastAPI endpoint.
    Returns:
        dict: Email data as a dictionary.
    """
    logging.info("Email Ingestion Agent: Fetching new email...")
    try:
        # Example: FastAPI endpoint for new emails.
        response = requests.get("http://localhost:8000/new_email")
        response.raise_for_status()
        email_data = response.json()
        logging.info("Email Ingestion Agent: Email fetched successfully.")
        return email_data
    except Exception as e:
        logging.error("Email Ingestion Agent: Error fetching email: %s", e)
        # Fallback: load from local JSON file.
        with open("data/mock_support_emails.json", "r") as f:
            emails = json.load(f)
        logging.info("Email Ingestion Agent: Using fallback email data.")
        return emails[0]

