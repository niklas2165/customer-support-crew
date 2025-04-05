import logging
import agents.email_ingestion as ingestion
import agents.intent_classifier as classifier
import agents.priority_scorer as scorer
import agents.response_drafter as drafter
import agents.logger as logger

def run_pipeline():
    logging.info("CrewAI Orchestrator: Starting the customer support pipeline.")
    
    # Step 1: Ingest Email
    email = ingestion.run()
    
    # Step 2: Classify Intent
    intent = classifier.run(email)
    
    # Step 3: Score Urgency
    urgency = scorer.run(email)
    
    # Step 4: Draft Response
    response = drafter.run(email, intent)
    
    # Step 5: Log the processed result
    logger.run(email, intent, urgency, response)
    
    logging.info("CrewAI Orchestrator: Pipeline execution completed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run_pipeline()

