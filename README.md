customer-support-crew/
├── agents/
│   ├── email_ingestion.py          # Fetch email from API or local JSON
│   ├── intent_classifier.py        # Classify email intent
│   ├── priority_scorer.py          # Heuristic & sentiment-based scoring
│   ├── response_drafter.py         # Generate email replies
│   └── logger.py                   # Log to DB and update frontend
│
├── data/
│   ├── EmailGenerator.py           # Create synthetic email dataset
│   └── mock_support_emails.json   # Pre-generated support emails
│
├── database/
│   ├── support_emails.db           # SQLite DB
│   └── schema.sql                  # DB table schema
│
├── db_utils.py                     # Database I/O utilities
├── crew.py                         # Multi-agent orchestration logic
├── daily_pipeline.py              # Daily pipeline runner
├── train_model.py                 # Intent model trainer
│
├── api/
│   └── main.py                     # FastAPI app for new email ingestion
│
├── models/
│   └── intent_classifier.pkl       # Trained ML model
│
├── docs/
│   └── index.html                  # GitHub Pages frontend
│
├── .github/
│   └── workflows/
│       └── respond.yml             # CI/CD with GitHub Actions
│
├── requirements.txt                # Python dependencies
├── .gitignore
├── Dockerfile                      # (Optional) Docker configuration
├── supervisord.conf                # (Optional) For multi-service containers
└── README.md
