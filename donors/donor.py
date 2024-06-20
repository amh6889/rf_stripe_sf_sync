from salesforce.salesforce_connection import sf
import stripe
from dotenv import load_dotenv
import os

load_dotenv()


class Donor:
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    @staticmethod
    def exists_by_email(email: str) -> str:
        search_query = 'FIND {' + email + '} IN EMAIL FIELDS RETURNING Contact(Id)'
        print(search_query)
        response = sf.search(search_query)
        print(response)
        records = response.get('searchRecords')
        sf_contact_id = None
        if len(records) > 0:
            record = records[0]
            sf_contact_id = record.get('Id')
            print(sf_contact_id)
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
        response = sf.Contact.create(donor)
        print(response)
        return response

    @staticmethod
    def update(sf_contact_id, **donor):
        try:
            print(donor)
            response = sf.Contact.update(sf_contact_id, donor)
            print(response)
            return response
        except Exception as e:
            print(e.message)

    @staticmethod
    def get_email(stripe_customer_id):
        customer = stripe.Customer.retrieve(stripe_customer_id)
        print(customer)
        return customer.email

    @staticmethod
    def update_stripe_customer(customer_id, key, value):
        try:
            updates = {key: value}
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
