from salesforce.salesforce_connection import sf
from utils.filter_string import filter_string


class SalesforceDonorService:
    def get_contact_id(self, email: str) -> str:
        escaped_email = filter_string(email)
        search_query = f"""FIND {{{escaped_email}}} IN EMAIL FIELDS RETURNING Contact(Id)"""
        print(search_query)
        response = sf.search(search_query)
        records = response.get('searchRecords')
        if records:
            record = records[0]
            sf_contact_id = record.get('Id')
            return sf_contact_id

    def get_contact_id_by_stripe_customer_id(self, stripe_customer_id: str) -> str:
        search_query = f'SELECT Id FROM Contact Where {stripe_customer_id} IN EMAIL FIELDS RETURNING Contact(Id)'
        print(search_query)
        response = sf.search(search_query)
        records = response.get('searchRecords')
        if len(records) > 0:
            record = records[0]
            sf_contact_id = record.get('Id')
            return sf_contact_id

    def create(self, **donor: dict) -> dict:
        print(f'Creating Stripe donor in Salesforce with data:\n{donor}')
        response = sf.Contact.create(donor)
        print(f'Successfully created Stripe donor in Salesforce with ID: {response.get("id")}')
        return response

    def update(self, sf_contact_id: str, **donor: dict):
        print(f'Updating Stripe donor {sf_contact_id} in Salesforce with data:\n{donor}')
        response = sf.Contact.update(sf_contact_id, donor)
        print(f'Successfully updated Stripe donor {sf_contact_id} in Salesforce.')
        return response
