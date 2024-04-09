from salesforce.salesforce_connection import sf
from utils.database_connection import db_connection
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
        records = response.get('searchRecords')
        sf_contact_id = None
        if len(records) > 0:
            record = records[0]
            sf_contact_id = record.get('Id')
            print(sf_contact_id)
        return sf_contact_id

    @staticmethod
    def exists_by_stripe_customer_id(stripe_customer_id: str) -> str:
        search_query = 'SELECT Id FROM Contact Where {' + stripe_customer_id + '} IN EMAIL FIELDS RETURNING Contact(Id)'
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
        try:
            response = sf.Contact.create(donor)
            print(response)
            return response
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update(sf_contact_id, **donor):
        print(donor)
        try:
            response = sf.Contact.update(sf_contact_id, donor)
            print(response)
            return response
        except Exception as e:
            print(e)

    @staticmethod
    def get_donor_events():
        query = (
            "SELECT * FROM stripe.stripe_event where is_synced = 'N' and event_type like '%customer%' order by created_at")
        events = []
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            for row in cursor:
                print(row)
                events.append(row)
        print((events[0]))
        return events

    @staticmethod
    def get_email(stripe_customer_id):
        customer = stripe.Customer.retrieve(stripe_customer_id)
        print(customer)
        return customer.email
