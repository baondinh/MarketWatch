import logging
import smtplib
import os
from dotenv import load_dotenv
import requests
import pandas as pd


'''
There are several API endpoints to choose from:

    End-of-Day Data: Get daily stock market data.
    Intraday Data: Get intraday and real-time market data.
    Tickers: Get information about stock ticker symbols.
    Exchanges: Get infotmation about all supported exchanges.
    Currencies: Get information about all supported currencies.
    Timezones: Get information about all supported timezones.

Base URL: API requests start out with the following base URL:

http://api.marketstack.com/v1/
'''

# dates YYYY-MM-DD
# EOD or intraday endpoints both return historic if providing date_from and date_to params
def get_marketwatch_historic(symbols, date_from, date_to, api_key: str): 
    url = 'http://api.marketstack.com/v1/eod'

    params = {
        "access_key": api_key,
        "symbols": ",".join(symbols),  # supports multiple tickers
        "date_from": date_from,
        "date_to": date_to
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

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

    logger.info("Fetching marketwatch data")
    date_from = '2025-08-04'
    date_to = '2025-08-08'
    symbols = ['AAPL']
    results = get_marketwatch_historic(symbols, date_from, date_to, MARKET_API_KEY)

    if results:
        df = pd.DataFrame(results)
        output_file = f'market_data_{date_from}_{date_to}.csv'
        df.to_csv(f"output/{output_file}", index=False)
        logger.info(f"Data successfully saved as {output_file}")
    else:
        logger.error("No data to save.")

if __name__ == "__main__": 
    main()