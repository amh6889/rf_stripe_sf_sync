from simple_salesforce import Salesforce
from dotenv import load_dotenv
import os

load_dotenv()

global sf

domain = os.getenv('SF_DOMAIN')
consumer_key = os.getenv('SF_CONSUMER_KEY')
consumer_secret = os.getenv('SF_CONSUMER_SECRET')

sf = Salesforce(domain=domain,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret)

