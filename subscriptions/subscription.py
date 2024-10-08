import os
from pprint import pprint

import stripe
import re

from dotenv import load_dotenv
from simple_salesforce import format_soql

from salesforce.salesforce_connection import sf

load_dotenv()


class Subscription:
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    @staticmethod
    def exists(subscription_id):
        query = f"SELECT Id,npe03__Contact__c from npe03__Recurring_Donation__c where Stripe_Subscription_ID__c = '{subscription_id}'"
        print(query)
        # results = sf.npe03__Recurring_Donation__c.get_by_custom_id('Stripe_Subscription_ID__c', subscription_id)
        response = sf.query(query)
        records = response.get('records')
        subscription = {}
        if len(records) > 0:
            record = records[0]
            subscription['id'] = record.get('Id')
            subscription['sf_contact_id'] = record.get('npe03__Contact__c')
        return subscription

    @staticmethod
    def get_metadata():
        metadata = sf.npe03__Recurring_Donation__c.metadata()
        mdapi = sf.mdapi
        custom_object = mdapi.CustomObject.read("npe03__Recurring_Donation__c")
        pprint(custom_object)
        return metadata

    @staticmethod
    def create_metadata():
        fields = []
        mdapi = sf.mdapi
        custom_field = mdapi.CustomField(
            type=mdapi.FieldType("Text"),
            fullName="Stripe_Sub_ID__c",
            label="Stripe Subscription ID",
            length="100",
            externalId=True,
            description="Stripe Subscription ID.",
            required=False,
            unique=False
        )
        fields.append(
            custom_field
        )

    @staticmethod
    def create(**recurring_donation):
        print(f'Creating recurring donation in Salesforce with data:\n{recurring_donation}\n')
        response = sf.npe03__Recurring_Donation__c.create(recurring_donation)
        return response

    @staticmethod
    def update(recurring_donation_id, **recurring_donation):
        print(f'Updating Salesforce recurring donation {recurring_donation_id} in Salesforce with data:\n{recurring_donation}\n')
        response = sf.npe03__Recurring_Donation__c.update(recurring_donation_id, recurring_donation)
        return response

    @staticmethod
    def get_payment_method(stripe_subscription_id):
        print(f'Getting payment method from Stripe for subscription {stripe_subscription_id}')
        subscription = stripe.Subscription.retrieve(stripe_subscription_id,
                                                    expand=['default_payment_method', 'default_source',
                                                            'latest_invoice.payment_intent.payment_method'])
        payment_method = Subscription.parse_payment_method(subscription)
        return payment_method

    @staticmethod
    def parse_payment_method(subscription):
        payment_method = None
        payment_methods = []
        if subscription['default_payment_method']:
            payment_methods.append(subscription['default_payment_method'])
        if subscription['default_source']:
            payment_methods.append(subscription['default_source'])
        if subscription['latest_invoice']:
            if subscription['latest_invoice']['payment_intent']:
                temp_payment_intent = subscription['latest_invoice']['payment_intent']
                if temp_payment_intent['payment_method']:
                    payment_methods.append(temp_payment_intent.get('payment_method'))
        if payment_methods:
            any(payment_method := pm for pm in tuple(payment_methods))
        return payment_method

    @staticmethod
    def get_campaign_id(campaign_code):
        # escaped_string = re.escape(campaign_code)
        # regex = r"""[-?&!{}\[\]\\^~*:"'+]"""
        # regex_campaign_code = re.sub(regex, "\\\\", campaign_code)
        # #print(regex_campaign_code)
        # query = f"FIND {{{regex_campaign_code}}} IN ALL FIELDS RETURNING Campaign(Id, Name)"
        # #query = f
        # print(query)
        # response = sf.search(query)
        print(f'Retrieving campaign code {campaign_code} from Salesforce...')
        response = sf.query(format_soql("SELECT Id FROM CAMPAIGN WHERE NAME LIKE '%{:like}%'", campaign_code))
        records = response['records']
        campaign_id = None
        if len(records) > 0:
            record = records[0]
            campaign_id = record.get('Id')
        return campaign_id
