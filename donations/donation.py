from pprint import pprint

import stripe

from salesforce.salesforce_connection import sf


class Donation:

    @staticmethod
    def exists(donation_id) -> str:
        query = f"SELECT Id from Opportunity where Stripe_Invoice_ID__c = '{donation_id}'"
        print(query)
        # results = sf.Opportunity.get_by_custom_id('Stripe_Invoice_ID__c', donation_id)
        response = sf.query(query)
        pprint(response)
        records = response['records']
        donation_id = None
        if len(records) > 0:
            record = records[0]
            donation_id = record.get('Id')
        return donation_id

    @staticmethod
    def create(**donation):
        print(donation)
        try:
            response = sf.Opportunity.create(donation)
            print(response)
            return response
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_stripe_subscription_id(invoice_id: str):
        print(invoice_id)
        try:
            response = stripe.Invoice.retrieve(invoice_id)
            print(response)
            return response['subscription']
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update(donation_id, **donation):
        print(donation)
        try:
            response = sf.Opportunity.update(donation_id, donation)
            print(response)
            return response
        except Exception as e:
            print(e)
            return None
