from salesforce.salesforce_connection import sf


class SalesforceDonationService:

    def exists(self, stripe_donation_id) -> str:
        query = f"SELECT Id from Opportunity where Stripe_Invoice_ID__c = '{stripe_donation_id}'"
        print(query)
        response = sf.query(query)
        records = response['records']
        donation_id = None
        if len(records) > 0:
            record = records[0]
            donation_id = record.get('Id')
        return donation_id


    def create(self, donation):
        print(f'Creating Stripe donation in Salesforce with data:\n{donation}')
        response = sf.Opportunity.create(donation)
        return response


    def update(self, donation_id, donation):
        print(f'Updating Stripe donation {donation_id} in Salesforce with data:\n{donation}')
        response = sf.Opportunity.update(donation_id, donation)
        return response