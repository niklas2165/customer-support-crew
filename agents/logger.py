import os
import sqlite3
import logging
import datetime

DB_PATH = os.path.join('database', 'support_emails.db')

def run(email, intent, urgency, response):
    """
    Log the processed email details into the database and update the frontend.
    Args:
        email (dict): Original email data.
        intent (str): Predicted intent.
        urgency (int): Urgency score.
        response (str): Drafted response.
    """
    logging.info("Logger Agent: Logging processed email...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Update the existing email record with new information.
    update_sql = """
    UPDATE support_emails
    SET intent_label = ?, urgency_score = ?, response = ?
    WHERE email_id = ?
    """
    cur.execute(update_sql, (intent, urgency, response, email.get("email_id")))
    conn.commit()
    conn.close()
    logging.info("Logger Agent: Email logged successfully.")
    
    # Update the frontend (e.g., append to docs/index.html).
    update_frontend(email, intent, urgency, response)

def update_frontend(email, intent, urgency, response):
    """
    Append the latest email processing result to an HTML file.
    """
    logging.info("Logger Agent: Updating frontend...")
    html_entry = f"""
    <div class="email-log">
      <h3>Email ID: {email.get("email_id")}</h3>
      <p><strong>Intent:</strong> {intent}</p>
      <p><strong>Urgency:</strong> {urgency}</p>
      <p><strong>Response:</strong> {response}</p>
      <p><em>Logged on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</em></p>
    </div>
    """
    with open("docs/index.html", "a") as f:
        f.write(html_entry)
    logging.info("Logger Agent: Frontend updated.")

