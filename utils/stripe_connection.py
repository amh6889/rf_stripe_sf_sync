import os

import stripe
from dotenv import load_dotenv

load_dotenv()


class StripeConnection:
    def __init__(self):
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.stripe = stripe
