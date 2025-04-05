-- database/schema.sql
DROP TABLE IF EXISTS support_emails;

CREATE TABLE IF NOT EXISTS support_emails (
    email_id INTEGER PRIMARY KEY,
    timestamp TEXT,
    sender TEXT,
    subject TEXT,
    body TEXT,
    intent_label TEXT,
    urgency_score INTEGER,
    response TEXT
);

