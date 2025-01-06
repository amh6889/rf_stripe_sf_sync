import time

from donors.donor_mapper import DonorMapper
from donors.salesforce_donor_service import SalesforceDonorService
from donors.stripe_donor_service import StripeDonorService


class DonorEventProcessor:
    def __init__(self, donor_mapper: DonorMapper, stripe_donor: StripeDonorService, salesforce_donor: SalesforceDonorService) -> None:
        self.donor_mapper = donor_mapper
        self.stripe_donor_service = stripe_donor
        self.salesforce_donor_service = salesforce_donor

    def process_create_event(self, event_data):
        donor = self.donor_mapper.map_donor_create_event(**event_data)
        stripe_customer_id = donor.get('External_Contact_ID__c')
        stripe_updates = donor.pop('stripe_updates', None)
        email = donor.get('Email')
        if email is None:
            raise Exception('Donor email is null.  Cannot process donor create event further.')
        sf_contact_id = self.salesforce_donor_service.get_contact_id(email=email)
        if not sf_contact_id:
            self._create_donor_in_salesforce(donor)
            if stripe_updates:
                self._update_donor_in_stripe(stripe_customer_id, stripe_updates)
        else:
            error_message = f'Stripe customer with email {email} already exists in Salesforce with ID {sf_contact_id}. Cannot process donor create event further.'
            raise Exception(error_message)

    def process_update_event(self, event_data):
        donor = self.donor_mapper.map_donor_update_event(**event_data)
        stripe_customer_id = donor.get('External_Contact_ID__c')
        stripe_updates = donor.pop('stripe_updates', None)
        email = donor.get('Email')
        if email is None:
            raise Exception('Donor email is null.  Cannot process donor update event further.')
        sf_contact_id = self.salesforce_donor_service.get_contact_id(email)
        if not sf_contact_id:
            error_message = f'Stripe customer with email {email} does not exist in Salesforce. Cannot process donor update event further.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        else:
            self._update_donor_in_salesforce(sf_contact_id, donor)
            if stripe_updates:
                self._update_donor_in_stripe(stripe_customer_id, stripe_updates)

    def _create_donor_in_salesforce(self, donor):
        email = donor.get('Email')
        print(
            f'Creating Stripe customer {donor.get('FirstName')} {donor.get('LastName')} with email {email} in Salesforce')
        response = self.salesforce_donor_service.create(**donor)
        if 'success' in response:
            success = response.get('success')
            if success:
                print(
                    f'Created Stripe customer with email {email} successfully in Salesforce with ID {response.get('id')}')
            else:
                errors = response.get('errors')
                error_message = f'Did not create Stripe customer with {email} successfully in Salesforce due to: {errors}'
                raise Exception(error_message)

    def _update_donor_in_stripe(self, stripe_customer_id: str, stripe_updates: dict) -> None:
        self.stripe_donor_service.update(stripe_customer_id, stripe_updates)

    def _update_donor_in_salesforce(self, sf_contact_id: str, donor: dict) -> None:
        response = self.salesforce_donor_service.update(sf_contact_id=sf_contact_id, **donor)
        if response != 204:
            errors = response.get('errors')
            error_message = f'Did not update Salesforce Contact {sf_contact_id} successfully in Salesforce due to {errors}'
            print(error_message)
            raise Exception(error_message)
        print(
            f'Updated Salesforce Contact {sf_contact_id} successfully in Salesforce.')
