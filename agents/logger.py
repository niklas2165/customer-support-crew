import os
import sqlite3
import logging
import datetime

DB_PATH = os.path.join('database', 'support_emails.db')

def run(email, intent, urgency, response):
    logging.info("Logger Agent: Logging processed email...")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # INSERT or REPLACE ensures the row is there
    cur.execute("""
        INSERT OR REPLACE INTO support_emails (
            email_id, timestamp, sender, subject, body, intent_label, urgency_score, response
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        email.get("email_id"),
        email.get("timestamp"),
        email.get("sender"),
        email.get("subject"),
        email.get("body"),
        intent,
        urgency,
        response
    ))

    conn.commit()
    conn.close()
    logging.info("Logger Agent: Email logged successfully.")
    update_frontend(email, intent, urgency, response)

def update_frontend(email, intent, urgency, response):
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

    updated = content.replace(
        "<!-- End of logs -->",
        html_entry + "\n<!-- End of logs -->"
    )

    with open("docs/index.html", "w") as f:
        f.write(updated)

    logging.info("Logger Agent: Frontend updated.")
