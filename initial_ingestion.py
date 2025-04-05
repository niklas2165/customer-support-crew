# initial_ingestion.py
import json
import sqlite3
import os

# Define file paths
DATA_JSON = os.path.join('data', 'mock_support_emails.json')
DB_PATH = os.path.join('database', 'support_emails.db')
SCHEMA_PATH = os.path.join('database', 'schema.sql')

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite DB: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return None

def create_table(conn, schema_file):
    """Create table(s) using the provided schema file."""
    with open(schema_file, 'r') as f:
        sql_script = f.read()
    try:
        cur = conn.cursor()
        cur.executescript(sql_script)
        conn.commit()
        print("Database table(s) created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table(s): {e}")

def ingest_data(conn, data_file):
    """Insert JSON data into the database."""
    with open(data_file, 'r') as f:
        data = json.load(f)
    sql = '''INSERT INTO support_emails(email_id, timestamp, sender, subject, body, intent_label, urgency_score, response)
             VALUES(?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    for email in data:
        cur.execute(sql, (
            email["email_id"],
            email["timestamp"],
            email["sender"],
            email["subject"],
            email["body"],
            email["intent_label"],
            email["urgency_score"],
            email["response"]
        ))
    conn.commit()
    print(f"Ingested {len(data)} emails into the database.")

def main():
    # Connect to the SQLite database
    conn = create_connection(DB_PATH)
    if conn is not None:
        # Create table(s) from the schema file
        create_table(conn, SCHEMA_PATH)
        # Ingest JSON data into the database
        ingest_data(conn, DATA_JSON)
        conn.close()
    else:
        print("Failed to create database connection.")

if __name__ == '__main__':
    main()
