import logging
from textblob import TextBlob

def run(email):
    """
    Score the urgency of the email using sentiment analysis as a heuristic.
    Args:
        email (dict): Email data.
    Returns:
        int: Urgency score (0, 1, or 2).
    """
    logging.info("Priority Scorer Agent: Scoring email urgency...")
    body = email.get("body", "")
    blob = TextBlob(body)
    polarity = blob.sentiment.polarity
    # Heuristic: lower polarity (more negative) means higher urgency.
    if polarity < -0.5:
        urgency = 2
    elif polarity < 0:
        urgency = 1
    else:
        urgency = 0
    logging.info("Priority Scorer Agent: Urgency score: %d", urgency)
    return urgency

