# Technical Report: Solopreneur Customer Support Automation

flowchart TD
    %% Data Ingestion & Training
    subgraph Data_Ingestion_&_Training
      A[Historical Data (JSON)]
      B[initial_ingestion.py]
      C[SQLite Database (support_emails.db)]
      D[train_model.py]
      E[Trained Model (intent_classifier.pkl)]
    end

    %% Modular Agent Architecture
    subgraph Modular_Agents
      F1[Email Ingestion Agent]
      F2[Intent Classifier Agent]
      F3[Priority Scorer Agent]
      F4[Response Drafter Agent]
      F5[Logger Agent]
    end

    %% Orchestration & Daily Pipeline
    subgraph Orchestration_&_Pipeline
      G[Crew Orchestrator (crew.py)]
      H[Daily Pipeline (daily_pipeline.py)]
    end

    %% API & Deployment
    subgraph API_&_Deployment
      I[FastAPI Endpoint (/new_email)]
      J[Hosted API on Render]
    end

    %% Automation & Frontend
    subgraph Automation_&_Frontend
      K[GitHub Actions (CI/CD)]
      L[Frontend Dashboard (docs/index.html)]
      M[GitHub Pages]
    end

    %% Connections
    A --> B
    B --> C
    C --> D
    D --> E

    C --> F1
    F1 --> I
    I --> J

    E --> F2

    G --> F1
    G --> F2
    G --> F3
    G --> F4
    G --> F5
    H --> G

    F5 --> C
    F5 --> L
    L --> M

    H --> K


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
    Fetches new email data by attempting to call a live FastAPI endpoint and falls back to the local JSON file if the API is unreachable.
  - **Intent Classifier Agent (`agents/intent_classifier.py`):**  
    Loads the pre-trained model and classifies the intent of an incoming email based on its subject and body.
  - **Priority Scorer Agent (`agents/priority_scorer.py`):**  
    Uses sentiment analysis (via TextBlob) as a heuristic to assign an urgency score.
  - **Response Drafter Agent (`agents/response_drafter.py`):**  
    Generates a rule-based draft response using pre-defined templates based on the identified intent.
  - **Logger Agent (`agents/logger.py`):**  
    Updates the SQLite database with the processed email and appends a new log entry to the frontend (`docs/index.html`). This agent also ensures that a consistent monitoring log is maintained.

- **Orchestration (`crew.py`):**  
  A custom orchestrator simulates a CrewAI multi-agent system by sequentially invoking each agent. Although this does not yet use the official CrewAI syntax, it provides a clear, modular structure that can later be extended with asynchronous or parallel processing capabilities.

### 2.4 API Implementation

- **FastAPI Endpoint (`api/main.py`):**  
  A lightweight API is developed to serve new emails. The endpoint `/new_email` randomly selects an email from the dataset, simulating an incoming email stream.

- **Deployment on Render:**  
  The API is deployed on Render, making it live and accessible at:  
  **[https://customer-support-crew.onrender.com/new_email](https://customer-support-crew.onrender.com/new_email)**  
  This endpoint is used by the Email Ingestion Agent to fetch new email data dynamically.

### 2.5 Daily Pipeline and Automation

- **Daily Pipeline (`daily_pipeline.py`):**  
  A script that calls the orchestrator function (`crew.run_pipeline()`) to process emails end-to-end. This script is designed to be executed manually or automatically.

- **CI/CD Integration with GitHub Actions (`.github/workflows/respond.yml`):**
  - **Scheduled Runs:** The pipeline is scheduled to run daily using a cron expression.
  - **Automation:** The workflow checks out the repository, installs dependencies, runs the daily pipeline, and commits updates to the frontend.
  - **Frontend Update:** The updated `docs/index.html` file (serving as a monitoring dashboard) is pushed, allowing GitHub Pages to display the latest logs.

### 2.6 Frontend for Monitoring

- **Static Frontend (`docs/index.html`):**  
  The frontend is a static HTML page that displays log entries of processed emails. The Logger Agent appends new log entries to this file, which is served via GitHub Pages.

- **User Interface:**  
  Basic styling and organization are applied to improve readability and provide quick insights into system performance.

- **Live Frontend URL:**  
  The GitHub Pages site is available at:  
  **[https://niklas2165.github.io/customer-support-crew/](https://niklas2165.github.io/customer-support-crew/)**

### 2.7 Database Utilities

- **db_utils.py:**  
  Currently, this module is a placeholder for future database utility functions that will centralize common database operations. While not critical to the current workflow, it will facilitate refactoring as the project scales.

---

## 3. Evaluation and Monitoring Strategy

### 3.1 Model Evaluation

- **During Training:**  
  The training script generates a detailed classification report that includes precision, recall, and F1-scores for each intent class. This helps in identifying potential class imbalances and areas where the model may need improvement.
  
- **Test-Train Split:**  
  The dataset is split into training and testing sets to reliably measure model performance and ensure that the classifier generalizes well to unseen data.

### 3.2 Runtime Monitoring

- **Logging:**  
  Each agent logs key events (e.g., data ingestion, intent classification, urgency scoring) using Python’s logging module, providing immediate feedback and aiding in debugging.
  
- **Frontend Dashboard:**  
  The static HTML page (`docs/index.html`) acts as a simple dashboard, displaying the latest log entries to monitor daily operations.
  
- **Database Records:**  
  All processed emails are stored in the SQLite database, offering a historical record that can be analyzed for trends and performance issues.

### 3.3 CI/CD Monitoring

- **GitHub Actions Logs:**  
  Each scheduled run is logged in GitHub Actions, allowing for monitoring of execution, detection of failures, and troubleshooting of errors.
  
- **Version Control:**  
  Changes to the frontend are committed and pushed automatically, ensuring that the system's state is reproducible and well-documented.

### 3.4 Future Enhancements

- **Advanced Dashboarding:**  
  Consider integrating tools like Grafana or Kibana for visualizing performance metrics over time.
  
- **Alerting Mechanisms:**  
  Implement alerts (via email or messaging platforms) to notify the team of pipeline failures or performance degradation.
  
- **Feedback Loop for Model Retraining:**  
  Utilize historical performance data to trigger periodic retraining or fine-tuning of the classifier, ensuring that the model adapts to evolving data trends.

---

## 4. Conclusion

This project demonstrates a complete, modular pipeline for automating customer support email processing. By integrating data ingestion, model training, agent-based orchestration, API deployment, and CI/CD automation, the system provides an end-to-end solution that is robust and scalable.

The evaluation and monitoring strategy ensures that both immediate feedback (via logs and a simple dashboard) and long-term system health (through CI/CD and database records) are maintained. This modular design not only meets the current requirements but also offers a clear path for future enhancements, including integration with advanced NLP models and true multi-agent orchestration frameworks.

---

## 5. Live Demo and Access

- **API Endpoint:**  
  [https://customer-support-crew.onrender.com/new_email](https://customer-support-crew.onrender.com/new_email)

- **Frontend Dashboard (GitHub Pages):**  
  [https://niklas2165.github.io/customer-support-crew/](https://niklas2165.github.io/customer-support-crew/)
