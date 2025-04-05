import csv
import time
import random
import os
import platform
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SupportEmailGenerator:
    def __init__(self, api_key=None, output_file="mock_support_emailstest.json"):
        """
        Initialize the support email generator using an API key for LLM access.
        
        Args:
            api_key: Your API key for the LLM service
            output_file: Output JSON file name
        """
        self.output_file = output_file
        
        # Set API key - either from parameter or environment variable
        self.api_key = api_key or os.environ.get("LLM_API_KEY")
        if not self.api_key:
            print("Warning: No API key provided. Please provide an API key with the api_key parameter")
            print("or set the LLM_API_KEY environment variable.")
            print("You can get an API key from OpenAI, Anthropic, or other LLM providers.")
        
        print("Initializing API-based support email generator...")
        
        # Initialize components
        self.setup_components()
        
        # Track API usage
        self.total_tokens_used = 0
        self.api_calls = 0
    
    def setup_components(self):
        """Setup components used to generate varied support emails"""
        # Email domains for sender addresses
        self.domains = [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
            "aol.com", "protonmail.com", "mail.com", "zoho.com", "gmx.com"
        ]
        
        # Common first names
        self.first_names = [
            "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Charles", "Karen", "Emma", "Olivia", "Noah", "Liam", "Sophia"
        ]
        
        # Common last names
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"
        ]
        
        # Intent categories (keeping these for categorization even though subjects will be generated)
        self.intents = [
            "Order Issue",
            "Return Request",
            "Exchange Request",
            "Shipping Delay",
            "Product Inquiry",
            "General Question",
            "Cancellation",
            "Billing Issue",
            "Account Access",
            "Product Feedback",
            "Warranty Claim",
            "Refund Request",
            "Complaint"
        ]

    def generate_random_email_address(self):
        """Generate a realistic customer email address"""
        first_name = random.choice(self.first_names).lower()
        last_name = random.choice(self.last_names).lower()
        domain = random.choice(self.domains)
        
        formats = [
            f"{first_name}.{last_name}@{domain}",
            f"{first_name}{last_name}@{domain}",
            f"{first_name}{random.randint(1, 99)}@{domain}",
            f"{first_name[0]}{last_name}@{domain}",
            f"{last_name}.{first_name}@{domain}"
        ]
        
        return random.choice(formats)
    
    def generate_random_timestamp(self, start_date=None, end_date=None):
        """Generate a random timestamp between two dates in MM/DD/YYYY format"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)  # Default to last year
        if not end_date:
            end_date = datetime.now() + timedelta(days=60)  # Include some future dates
            
        time_difference = end_date - start_date
        random_days = random.randint(0, time_difference.days)
        
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%m/%d/%Y")
    
    def generate_email_prompt(self):
        """Generate a detailed prompt for the LLM to create a support email and response"""
        # We'll still use the intent categories but let the LLM create a relevant subject
        intent = random.choice(self.intents)
        urgency = random.randint(0, 3)  # 0=low, 1=medium, 2=high, 3=critical
        
        # Example business types to provide context

        
        # Create the prompt for the API
        prompt = f"""Generate a realistic customer support email and a matching support agent response for an e-commerce store selling clothing.

The email should:
1. Have a specific, realistic subject line that a customer might use. Make sure these subjects have a relatively high level of uniqueness.
2. Involve a {intent.lower()} scenario with urgency level {urgency} (0=low, 1=medium, 2=high, 3=critical)
3. Sound like it was written by a real customer with a specific issue or question
4. Be written in English

The response should:
1. Sound like it was written by a customer service representative addressing the customer's concern
2. Be professional but personable
3. Directly address the specific issue raised by the customer

Return your answer in this exact JSON format:
{{
  "subject": "The email subject line",
  "customer_email": "The full text of the customer's email (1-3 paragraphs)",
  "support_response": "The full text of the customer service response (1-2 paragraphs)"
}}"""
        
        return prompt, intent, urgency
    
    def call_openai_api(self, prompt):
        """Generate emails using OpenAI API"""
        if not self.api_key:
            # Return dummy data if no API key provided
            return {
                "customer_email": "This is a placeholder customer email. Please provide an API key to generate real emails.",
                "support_response": "This is a placeholder support response. Please provide an API key to generate real responses."
            }
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": "gpt-4o-mini",  # You can use "gpt-4" for higher quality
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that generates realistic customer support emails and responses."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise exception for HTTP errors
            
            result = response.json()
            self.api_calls += 1
            self.total_tokens_used += result.get("usage", {}).get("total_tokens", 0)
            
            content = result["choices"][0]["message"]["content"].strip()
            
            # Parse the JSON response
            try:
                json_response = json.loads(content)
                return json_response
            except json.JSONDecodeError:
                print(f"Failed to parse JSON response: {content}")
                return {
                    "customer_email": "Error parsing response",
                    "support_response": "Error parsing response"
                }
                
        except Exception as e:
            print(f"API call error: {e}")
            return {
                "customer_email": f"Error generating email: {str(e)}",
                "support_response": f"Error generating response: {str(e)}"
            }
    
    def call_anthropic_api(self, prompt):
        """Generate emails using Anthropic Claude API"""
        if not self.api_key:
            # Return dummy data if no API key provided
            return {
                "customer_email": "This is a placeholder customer email. Please provide an API key to generate real emails.",
                "support_response": "This is a placeholder support response. Please provide an API key to generate real responses."
            }
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": "claude-3-haiku-20240307",  # Use "claude-3-opus-20240229" for higher quality
            "max_tokens": 800,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise exception for HTTP errors
            
            result = response.json()
            self.api_calls += 1
            
            content = result["content"][0]["text"]
            
            # Parse the JSON response
            try:
                json_response = json.loads(content)
                return json_response
            except json.JSONDecodeError:
                print(f"Failed to parse JSON response: {content}")
                return {
                    "customer_email": "Error parsing response",
                    "support_response": "Error parsing response"
                }
                
        except Exception as e:
            print(f"API call error: {e}")
            return {
                "customer_email": f"Error generating email: {str(e)}",
                "support_response": f"Error generating response: {str(e)}"
            }
    
    def generate_email(self, prompt, api_provider="openai"):
        """Generate an email using the specified API provider"""
        print(f"Calling {api_provider} API...")
        start_time = time.time()
        
        if api_provider.lower() == "openai":
            result = self.call_openai_api(prompt)
        elif api_provider.lower() == "anthropic":
            result = self.call_anthropic_api(prompt)
        else:
            raise ValueError(f"Unsupported API provider: {api_provider}")
        
        generation_time = time.time() - start_time
        print(f"Generation completed in {generation_time:.2f} seconds")
        
        return result
    
    def generate_emails(self, count=10, api_provider="openai"):
        """Generate specified number of emails and save to JSON file"""
        print(f"Generating {count} mock support emails using {api_provider} API...")
        start_time = time.time()
        
        emails = []
        
        for i in range(count):
            if i % 5 == 0 or i == count - 1:
                elapsed_time = time.time() - start_time
                emails_per_second = (i + 1) / elapsed_time if elapsed_time > 0 else 0
                estimated_time_left = (count - i - 1) / emails_per_second if emails_per_second > 0 else "unknown"
                if isinstance(estimated_time_left, float):
                    hours, remainder = divmod(estimated_time_left, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_left_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
                else:
                    time_left_str = estimated_time_left
                    
                print(f"Generated {i+1}/{count} emails... ({emails_per_second:.2f} emails/sec, est. time left: {time_left_str})")
            
            prompt, intent, urgency = self.generate_email_prompt()
            result = self.generate_email(prompt, api_provider)
            
            # Extract subject from the LLM response, fallback to a generic subject if missing
            subject = result.get("subject", "Customer Support Request")
            
            email = {
                "email_id": i + 1,
                "timestamp": self.generate_random_timestamp(),
                "sender": self.generate_random_email_address(),
                "subject": subject,
                "body": result["customer_email"],
                "intent_label": intent,
                "urgency_score": urgency,
                "response": result["support_response"]
            }
            
            emails.append(email)
            
        # Write each email as a separate JSON object on its own line (JSON Lines format)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for email in emails:
                f.write(json.dumps(email) + '\n')
                
        total_time = time.time() - start_time
        print(f"Successfully generated {count} emails in {total_time:.2f} seconds")
        print(f"Average generation speed: {count/total_time:.2f} emails per second")
        if self.api_calls > 0:
            print(f"API calls made: {self.api_calls}")
            print(f"Total tokens used: {self.total_tokens_used}")

        print(f"Output saved to: {self.output_file}")
                
        total_time = time.time() - start_time
        print(f"Successfully generated {count} emails in {total_time:.2f} seconds")
        print(f"Average generation speed: {count/total_time:.2f} emails per second")
        

# Example usage
if __name__ == "__main__":
    print(f"Python version: {platform.python_version()}")
    print(f"Operating system: {platform.system()} {platform.release()}")
    
    # Get API key from environment variables (including those loaded from .env file)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("No API key found in environment variables or .env file.")
        api_key = input("Please enter your OpenAI or Anthropic API key: ").strip()
    
    # Choose API provider
    api_provider = "openai"  # Default to OpenAI
    # Create generator with API key
    generator = SupportEmailGenerator(api_key=api_key, output_file="mock_support_emailstest.json")
    
    # Ask how many emails to generate
    try:
        count = int(input("How many emails do you want to generate? [default: 10]: ") or "10")
    except ValueError:
        count = 10
        print("Invalid input, using default count of 10 emails.")
    
    # Generate emails
    print(f"\nGenerating {count} emails using {api_provider} API...")
    generator.generate_emails(count=count, api_provider=api_provider)