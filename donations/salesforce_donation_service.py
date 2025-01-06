from salesforce.salesforce_connection import sf


class SalesforceDonationService:

    def exists(self, stripe_donation_id) -> str:
        query = f"SELECT Id from Opportunity where Stripe_Invoice_ID__c = '{stripe_donation_id}'"
        print(query)
        # results = sf.Opportunity.get_by_custom_id('Stripe_Invoice_ID__c', donation_id)
        response = sf.query(query)
        records = response['records']
        donation_id = None
        if len(records) > 0:
            record = records[0]
            donation_id = record.get('Id')
        return donation_id


    def create(self, **donation):
        print(f'Creating donation in Salesforce with data:\n{donation}')
        response = sf.Opportunity.create(donation)
        return response


    def update(self, donation_id, **donation):
        print(f'Updating Donation {donation_id} in Salesforce with data:\n{donation}')
        response = sf.Opportunity.update(donation_id, donation)
        return response