import pickle
import os
import logging

MODEL_PATH = os.path.join('models', 'intent_classifier.pkl')

# Load the model once for efficiency.
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

def run(email):
    """
    Classify the intent of the email using the pre-trained model.
    Args:
        email (dict): Email data.
    Returns:
        str: Predicted intent label.
    """
    logging.info("Intent Classifier Agent: Classifying email intent...")
    text = (email.get("subject", "") + " " + email.get("body", "")).lower()
    predicted_intent = model.predict([text])[0]
    logging.info("Intent Classifier Agent: Predicted intent: %s", predicted_intent)
    return predicted_intent

