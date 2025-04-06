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

    update_sql = """
    UPDATE support_emails
    SET intent_label = ?, urgency_score = ?, response = ?
    WHERE email_id = ?
    """
    cur.execute(update_sql, (intent, urgency, response, email.get("email_id")))
    conn.commit()
    conn.close()
    logging.info("Logger Agent: Email logged successfully.")

    # Update the frontend (insert inside HTML structure)
    update_frontend(email, intent, urgency, response)


def update_frontend(email, intent, urgency, response):
    """
    Insert the latest email processing result into the HTML file within the logs container.
    """
    logging.info("Logger Agent: Updating frontend...")
    html_entry = f"""
    <div class="log-entry">
      <h3>Email ID: {email.get("email_id")}</h3>
      <p><strong>Intent:</strong> {intent}</p>
      <p><strong>Urgency:</strong> {urgency}</p>
      <p><strong>Response:</strong> {response}</p>
      <p><em>Logged on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</em></p>
    </div>
    """

    with open("docs/index.html", "r") as f:
        content = f.read()

    # Insert before the special comment marker
    updated_content = content.replace(
        "<!-- End of logs -->",
        html_entry + "\n<!-- End of logs -->"
    )

    with open("docs/index.html", "w") as f:
        f.write(updated_content)

    logging.info("Logger Agent: Frontend updated.")
