import logging

def run(email, intent):
    """
    Generate a draft response based on the email and its intent.
    Args:
        email (dict): Email data.
        intent (str): Predicted email intent.
    Returns:
        str: Drafted response text.
    """
    logging.info("Response Drafter Agent: Generating response for intent: %s", intent)
    # Define simple templates for different intents.
    templates = {
        "Refund Request": (
            "Dear {sender},\n\nWe have received your refund request. "
            "Please follow the instructions to return the item.\n\nBest regards,\nCustomer Support Team"
        ),
        "Billing Issue": (
            "Dear {sender},\n\nWe've noted your billing issue. "
            "Please check your invoice details and let us know if there are any discrepancies.\n\nSincerely,\nCustomer Support Team"
        ),
        "Cancellation": (
            "Dear {sender},\n\nYour cancellation request is being processed. "
            "We will update you shortly.\n\nRegards,\nCustomer Support Team"
        ),
        # Add more templates as needed.
    }
    # Use a fallback template if the intent is unknown.
    template = templates.get(intent, (
        "Dear {sender},\n\nThank you for reaching out. "
        "We are reviewing your request and will respond soon.\n\nBest,\nCustomer Support Team"
    ))
    response = template.format(sender=email.get("sender", "Customer"))
    logging.info("Response Drafter Agent: Draft response generated.")
    return response

