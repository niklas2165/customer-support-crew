# train_model.py
import os
import sqlite3
import pandas as pd
import argparse
import logging
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define paths
DB_PATH = os.path.join('database', 'support_emails.db')
MODEL_PATH = os.path.join('models', 'intent_classifier.pkl')

def load_data(db_path):
    """Load email data from the SQLite database."""
    conn = sqlite3.connect(db_path)
    query = "SELECT subject, body, intent_label FROM support_emails"
    df = pd.read_sql_query(query, conn)
    conn.close()
    logging.info(f"Loaded {len(df)} emails from database.")
    return df

def train_model(df, test_size=0.2, random_state=42):
    """
    Train a classifier using the email 'subject' and 'body' as input.
    Returns a pipeline that includes TF-IDF vectorization and Logistic Regression.
    """
    # Combine subject and body, normalize text by lowercasing
    df['text'] = (df['subject'] + " " + df['body']).str.lower()
    X = df['text']
    y = df['intent_label']
    
    # Split the data for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    logging.info(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
    
    # Build a pipeline with TF-IDF and Logistic Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', LogisticRegression(solver='liblinear'))
    ])
    
    logging.info("Starting model training...")
    pipeline.fit(X_train, y_train)
    logging.info("Model training completed.")
    
    # Evaluate model performance
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred)
    logging.info("Classification Report:\n" + report)
    
    return pipeline

def save_model(model, model_path):
    """Save the trained model as a pickle file."""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    logging.info(f"Model saved to {model_path}")

def main(args):
    df = load_data(DB_PATH)
    
    if df.empty:
        logging.error("No data found in the database. Please run the ingestion script first.")
        return
    
    model = train_model(df, test_size=args.test_size, random_state=args.random_state)
    save_model(model, MODEL_PATH)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train an intent classifier using support emails data.")
    parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of the dataset to include in the test split')
    parser.add_argument('--random_state', type=int, default=42, help='Random state for train/test splitting')
    
    args = parser.parse_args()
    main(args)

