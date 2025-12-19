import time

from donors.donor_mapper import DonorMapper
from donors.donor_salesforce_service import SalesforceDonorService
from donors.donor_stripe_service import StripeDonorService


class DonorEventService:
    def __init__(self, donor_mapper: DonorMapper, stripe_donor: StripeDonorService,
                 salesforce_donor: SalesforceDonorService) -> None:
        self.donor_mapper = donor_mapper
        self.stripe_donor_service = stripe_donor
        self.salesforce_donor_service = salesforce_donor

    def process_create_event(self, event_data: dict) -> str:
        donor = self.donor_mapper.map_create_event(event_data)
        if email := donor.get('Email'):
            if sf_contact_id := self.salesforce_donor_service.get_contact_id(email=email):
                error_message = f'Stripe customer with email {email} already exists in Salesforce with ID {sf_contact_id}. Cannot process donor create event further.'
                raise Exception(error_message)
            else:
                stripe_updates = donor.pop('stripe_updates', None)
                sf_contact_id = self._create_donor_in_salesforce(donor)
                if stripe_updates:
                    stripe_customer_id = stripe_updates.get('id')
                    updated_donor = self._update_donor_in_stripe(stripe_customer_id, stripe_updates)
                    print(
                        f'Successfully updated stripe donor {updated_donor.get('id')} in Stripe with the following updates: {stripe_updates}')
            return sf_contact_id
        else:
            raise Exception('Donor email is null.  Cannot process donor create event further.')


    def process_update_event(self, event_data: dict) -> bool:
        donor = self.donor_mapper.map_update_event(event_data)
        if email := donor.get('Email'):
            stripe_updates = donor.pop('stripe_updates', None)
            if sf_contact_id := self.salesforce_donor_service.get_contact_id(email):
                self._update_donor_in_salesforce(sf_contact_id, donor)
                print(
                    f'Updated Salesforce Contact {sf_contact_id} successfully in Salesforce.')
                if stripe_updates:
                    stripe_customer_id = stripe_updates.pop('id')
                    updated_donor = self._update_donor_in_stripe(stripe_customer_id, stripe_updates)
                    print(
                        f'Successfully updated stripe donor {updated_donor.get('id')} in Stripe with the following updates: {stripe_updates}')
            else:
                error_message = f'Stripe customer with email {email} does not exist in Salesforce. Cannot process donor update event further.'
                print(error_message)
                time.sleep(30)
                raise Exception(error_message)
        else:
            raise Exception('Donor email is null.  Cannot process donor update event further.')
        success = True
        return success

    def _create_donor_in_salesforce(self, donor: dict) -> str:
        email = donor.get('Email')
        print(
            f'Creating Stripe customer {donor.get('FirstName')} {donor.get('LastName')} with email {email} in Salesforce')
        response = self.salesforce_donor_service.create(donor)
        if 'success' in response:
            success = response.get('success')
            if success:
                salesforce_created_id = response.get('id')
                print(
                    f'Created Stripe customer {donor.get('FirstName')} {donor.get('LastName')} with email {email} successfully in Salesforce with ID {salesforce_created_id}')
                return salesforce_created_id
            else:
                errors = response.get('errors')
                salesforce_error = None
                if len(errors) > 0:
                    salesforce_error = errors[0].get('message')
                error_message = f'Did not create Stripe customer with {email} successfully in Salesforce due to: {salesforce_error}'
                raise Exception(error_message)

    def _update_donor_in_stripe(self, stripe_customer_id: str, stripe_updates: dict) -> dict:
        return self.stripe_donor_service.update(stripe_customer_id, stripe_updates)

    def _update_donor_in_salesforce(self, sf_contact_id: str, donor: dict) -> None:
        response = self.salesforce_donor_service.update(sf_contact_id=sf_contact_id, donor)
        if response != 204:
            error_message = f'Did not update Salesforce Contact {sf_contact_id} successfully in Salesforce due to {response}'
            print(error_message)
            raise Exception(error_message)
