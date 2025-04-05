# api/main.py
from fastapi import FastAPI, HTTPException
import random
import json
import os

app = FastAPI()

# Path to the JSON data file containing the historical emails
DATA_FILE = os.path.join("data", "mock_support_emails.json")

def load_emails():
    """Load emails from the JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            emails = json.load(f)
        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading emails: {e}")

@app.get("/new_email")
def get_new_email():
    """Return a random email from the dataset."""
    emails = load_emails()
    if not emails:
        raise HTTPException(status_code=404, detail="No emails found")
    # Pick a random email to simulate a new incoming email
    email = random.choice(emails)
    return email

