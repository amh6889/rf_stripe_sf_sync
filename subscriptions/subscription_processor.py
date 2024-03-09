from pprint import pprint

from salesforce.salesforce_connection import sf


class SubscriptionProcessor:

    @staticmethod
    def subscription_exists(subscription_id):
        query = f"SELECT Id,npe03__Contact__c from npe03__Recurring_Donation__c where Stripe_Subscription_ID__c = '{subscription_id}'"
        print(query)
        #results = sf.npe03__Recurring_Donation__c.get_by_custom_id('Stripe_Subscription_ID__c', subscription_id)
        response = sf.query(query)
        pprint(response)
        records = response['records']
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
    def create_subscription(**recurring_donation):
        print(recurring_donation)
        try:
            response = sf.npe03__Recurring_Donation__c.create(recurring_donation)
            print(response)
            return response
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_subscription(recurring_donation_id, **recurring_donation):
        print(recurring_donation)
        try:
            response = sf.npe03__Recurring_Donation__c.update(recurring_donation_id,recurring_donation)
            print(response)
            return response
        except Exception as e:
            print(e)
            return None
