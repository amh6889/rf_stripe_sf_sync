import re

from salesforce.salesforce_connection import sf
import stripe
from dotenv import load_dotenv
import os

from utils.filter_string import filter_string

load_dotenv()


class Donor:
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    @staticmethod
    def exists_by_email(email: str) -> str:
        escaped_email = filter_string(email)
        search_query = f"""FIND {{{escaped_email}}} IN EMAIL FIELDS RETURNING Contact(Id)"""
        print(search_query)
        response = sf.search(search_query)
        print(response)
        records = response.get('searchRecords')
        sf_contact_id = None
        if records:
            record = records[0]
            sf_contact_id = record.get('Id')
        return sf_contact_id

    @staticmethod
    def exists_by_stripe_customer_id(stripe_customer_id: str) -> str:
        search_query = f'SELECT Id FROM Contact Where {stripe_customer_id} IN EMAIL FIELDS RETURNING Contact(Id)'
        print(search_query)
        response = sf.search(search_query)
        records = response.get('searchRecords')
        sf_contact_id = None
        if len(records) > 0:
            record = records[0]
            sf_contact_id = record.get('Id')
            print(sf_contact_id)
        return sf_contact_id

    @staticmethod
    def create(**donor):
        print(donor)
        response = sf.Contact.create(donor)
        return response

    @staticmethod
    def update(sf_contact_id, **donor):
        print(donor)
        response = sf.Contact.update(sf_contact_id, donor)
        return response

    @staticmethod
    def get_email(stripe_customer_id):
        customer = stripe.Customer.retrieve(stripe_customer_id)
        print(customer)
        return customer.email

    @staticmethod
    def update_stripe_customer(customer_id, updates):
        try:
            print(updates)
            response = stripe.Customer.modify(customer_id, **updates)
            print(response)
        except Exception as error:
            print(error)

    @staticmethod
    def get_stripe_customer_address(stripe_payment_method_id):
        payment_method = stripe.PaymentMethod.retrieve(stripe_payment_method_id)
        address = payment_method.billing_details.address
        return address
