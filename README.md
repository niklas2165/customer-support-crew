# Technical Report: Solopreneur Customer Support Automation

## 1. Introduction and Aim

The aim of this project is to automate the customer support process for a solopreneur by building a modular MLOps pipeline that classifies and responds to incoming customer emails in a consistent, efficient manner. The system is designed to:

- **Ingest and store historical email data** using a lightweight SQLite database.
- **Train an intent classifier** using traditional NLP methods (TF-IDF and Logistic Regression).
- **Implement a modular agent-based architecture** (simulated with our custom orchestrator) to process new emails, including intent classification, urgency scoring, and response drafting.
- **Deploy a FastAPI endpoint** to serve live email data.
- **Automate the entire pipeline** using GitHub Actions with a continuously updated frontend via GitHub Pages.

This project not only demonstrates the practical application of NLP in an automated support system but also serves as a solid foundation for further extensions such as integrating advanced LLMs or multi-agent orchestration frameworks like CrewAI.

---

## 2. Technical Details of Each Pipeline Component

### 2.1 Data Ingestion and Storage

- **Historical Data Generation:**  
  A dataset of 100 realistic support emails is generated in JSON format. Each email entry includes fields such as `email_id`, `timestamp`, `sender`, `subject`, `body`, `intent_label`, `urgency_score`, and `response`.

- **Database Schema (`database/schema.sql`):**  
  The SQLite schema is defined to create a `support_emails` table that mirrors the JSON structure. A lightweight database was chosen for its simplicity, ease of use, and local testing capabilities.

- **Ingestion Script (`initial_ingestion.py`):**  
  This script reads the JSON data, creates a database connection, applies the schema, and populates the database. It is a one-time setup utility ensuring that the historical data is available for model training and evaluation.

### 2.2 Model Training

- **Preprocessing and Training (`train_model.py`):**  
  The training script performs the following tasks:
  - **Data Loading:** Reads the `subject` and `body` fields from the SQLite database.
  - **Text Normalization:** Combines and lowercases the email subject and body to standardize the text for feature extraction.
  - **Pipeline Construction:** Utilizes TF-IDF vectorization followed by a Logistic Regression classifier. This pipeline was chosen for its simplicity and efficiency, making it suitable for a modest-sized dataset.
  - **Model Evaluation:** A classification report is generated to assess performance metrics (precision, recall, and F1-score) for each intent category.
  - **Model Persistence:** The trained model is serialized and saved to `models/intent_classifier.pkl` for future inference.

### 2.3 Modular Agent Architecture

- **Agent-Based Design:**  
  The project uses a modular approach where each component of the pipeline is encapsulated in its own Python module under the `agents/` directory. This design enhances maintainability and scalability.

- **Agents:**
  - **Email Ingestion Agent (`agents/email_ingestion.py`):**  
    Fetches a new email from the live FastAPI endpoint. If the email is not yet in the database, it inserts it. This guarantees that each processed email is stored for reproducibility and monitoring. This replaced the initial fallback approach with one that consistently pulls live data from the hosted API.
  - **Intent Classifier Agent (`agents/intent_classifier.py`):**  
    Loads the pre-trained model and classifies the intent of the email based on its subject and body.
  - **Priority Scorer Agent (`agents/priority_scorer.py`):**  
    Uses a sentiment-based heuristic (via TextBlob) to assign a 0–2 urgency score.
  - **Response Drafter Agent (`agents/response_drafter.py`):**  
    Generates a response using simple rule-based templates aligned with the predicted intent.
  - **Logger Agent (`agents/logger.py`):**  
    Uses an `INSERT OR REPLACE` operation to write the processed email (including intent, urgency, and response) to the database. It also injects a new log entry into `docs/index.html` before a predefined marker, ensuring daily updates to the GitHub Pages frontend.

- **Orchestration (`crew.py`):**  
  A custom orchestrator simulates a CrewAI multi-agent system by sequentially invoking each agent. Though not using official CrewAI syntax yet, the modular design allows for easy upgrades to more sophisticated frameworks later.

### 2.4 API Implementation

- **FastAPI Endpoint (`api/main.py`):**  
  A lightweight FastAPI server exposes the `/new_email` endpoint, which randomly returns a realistic email from a predefined JSON dataset.

- **Deployment on Render:**  
  The API is live at:  
  **[https://customer-support-crew.onrender.com/new_email](https://customer-support-crew.onrender.com/new_email)**  
  This endpoint is accessed daily by the pipeline.

### 2.5 Daily Pipeline and Automation

- **Daily Pipeline (`daily_pipeline.py`):**  
  The pipeline fetches one new email from the API, inserts it into the database (if not present), classifies it, scores its urgency, generates a response, updates the database, and finally logs it to the frontend HTML.

- **CI/CD Integration with GitHub Actions (`.github/workflows/respond.yml`):**
  - **Scheduled Runs:** Configured to run once daily via cron (`7:30 UTC`).
  - **Automation:** Each run installs dependencies, executes the full pipeline, and pushes the updated HTML to the `docs/` directory.
  - **Push Permissions:** Workflow permissions are explicitly enabled to allow GitHub Actions to commit and push frontend changes using the built-in `GITHUB_TOKEN`.

### 2.6 Frontend for Monitoring

- **Static Frontend (`docs/index.html`):**  
  Serves as a simple but effective monitoring dashboard. New log entries are inserted by the Logger Agent and pushed via CI/CD to GitHub Pages.

- **Marker-Based Update Logic:**  
  The Logger Agent inserts new entries before the marker `<!-- End of logs -->` inside a designated container `<div id="logs">`, ensuring that new emails appear chronologically in the frontend.

- **Live Frontend URL:**  
  View the updated logs at:  
  **[https://niklas2165.github.io/customer-support-crew/](https://niklas2165.github.io/customer-support-crew/)**

### 2.7 Database Utilities

- **db_utils.py:**  
  A placeholder for shared database logic. Can be expanded as the system grows to support reusable queries or database backups.

---

## 3. Evaluation and Monitoring Strategy

### 3.1 Model Evaluation

- **Training Time Metrics:**  
  The classifier’s accuracy is evaluated using a test/train split and `sklearn`'s classification report.

- **Class Distribution Awareness:**  
  Performance metrics per intent help identify class imbalance and optimize templates or thresholds accordingly.

### 3.2 Runtime Monitoring

- **Agent-Level Logging:**  
  All key steps are logged using `logging`, with output visible locally and in GitHub Actions logs.

- **Frontend Audit Trail:**  
  `index.html` acts as an audit dashboard that’s updated every day with one new processed email.

- **Data Provenance:**  
  Every processed email is logged in `support_emails.db`, allowing downstream analysis of trends, misclassifications, and re-training opportunities.

### 3.3 CI/CD Monitoring

- **Live Logs:**  
  Every scheduled run is visible in GitHub Actions with full stdout logs (enabled via `StreamHandler(sys.stdout)` in `daily_pipeline.py`).

- **Change Tracking:**  
  Git commits to the updated frontend serve as version-controlled records of pipeline activity.

---

## 4. Conclusion

This pipeline automates daily customer support by combining ML, automation, and monitoring in one modular system. The orchestration simulates multi-agent workflows, while the integration of a live API, GitHub Actions, and GitHub Pages ensures full reproducibility and visibility.

The system is stable, extensible, and provides a strong foundation for future enhancements including:
- Retrieval-Augmented Generation (RAG)
- Full LLM-powered response generation
- Feedback-driven model retraining

---

## 5. Live Demo and Access

- **API Endpoint (Render):**  
  [https://customer-support-crew.onrender.com/new_email](https://customer-support-crew.onrender.com/new_email)

- **Frontend Dashboard (GitHub Pages):**  
  [https://niklas2165.github.io/customer-support-crew/](https://niklas2165.github.io/customer-support-crew/)
