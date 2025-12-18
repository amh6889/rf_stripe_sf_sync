from simple_salesforce import format_soql

from salesforce.salesforce_connection import sf


class SalesforceSubscriptionService:

    def create(self, **recurring_donation):
        print(f'Creating recurring donation in Salesforce with data:\n{recurring_donation}\n')
        response = sf.npe03__Recurring_Donation__c.create(recurring_donation)
        return response

    def update(self, recurring_donation_id: str, recurring_donation: dict):
        print(
            f'Updating Salesforce recurring donation {recurring_donation_id} in Salesforce with data:\n{recurring_donation}\n')
        response = sf.npe03__Recurring_Donation__c.update(recurring_donation_id, recurring_donation)
        return response

    def get_by_stripe_id(self, subscription_id: str) -> dict:
        query = f"SELECT Id,npe03__Contact__c, npsp__RecurringType__c from npe03__Recurring_Donation__c where Stripe_Subscription_ID__c = '{subscription_id}'"
        print(query)
        response = sf.query(query)
        records = response.get('records')
        if len(records) > 0:
            record = records[0]
            subscription = {'id': record.get('Id'), 'sf_contact_id': record.get('npe03__Contact__c'), 'type': record.get('npsp__RecurringType__c')}
            return subscription

    def get_by_anet_id(self, subscription_id: str) -> dict:
        query = f"SELECT Id,npe03__Contact__c from npe03__Recurring_Donation__c where ANET_ARB_ID__c = '{subscription_id}'"
        print(query)
        response = sf.query(query)
        records = response.get('records')
        if len(records) > 0:
            record = records[0]
            subscription = {'id': record.get('Id'), 'sf_contact_id': record.get('npe03__Contact__c')}
            return subscription

    def get_campaign_id(self, campaign_code):
        print(f'Retrieving campaign code {campaign_code} from Salesforce...')
        response = sf.query(format_soql("SELECT Id FROM CAMPAIGN WHERE NAME LIKE '%{:like}%'", campaign_code))
        records = response['records']
        campaign_id = None
        if len(records) > 0:
            record = records[0]
            campaign_id = record.get('Id')
        return campaign_id
