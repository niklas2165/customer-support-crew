#!/usr/bin/env python
import logging
import sys
import crew

if __name__ == "__main__":
    # Configure logging so it shows up in GitHub Actions logs
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Run the complete email processing pipeline
    crew.run_pipeline()
