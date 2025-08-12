import logging
import smtplib
import os
from dotenv import load_dotenv

def get_marketwatch(api_key: str): 
    print('test')


def main(): 
    # Load environment variables from .env file
    load_dotenv()

    # Setup logger 
    logger = logging.getLogger("Market Watch")

    # Setup environments 
    try: 
        MARKET_API_KEY = os.getenv("MARKETSTACK_API_KEY")
        EMAIL_USER = os.getenv("EMAIL_USER")
        EMAIL_PASS = os.getenv("OUTLOOK_APP_PASSWORD")
        EMAIL_TO = os.getenv("EMAIL_TO").split(',') # Create list from string of emails
        EMAIL_TO = [email.strip() for email in EMAIL_TO]  # Remove spaces
    except Exception as e: 
        logger.error(f"Failed to setup environment {e}")

    # Setup Outlook email 
    try: 
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
    except Exception as e: 
        logger.error(f"Failed to setup Outlook email {e}")

    

if __name__ == "__main__": 
    main()