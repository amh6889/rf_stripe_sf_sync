import time
import traceback

from donors.donor import Donor
from donors.donor_mapper import DonorMapper


def create_donor_in_salesforce(donor):
    email = donor.get('Email')
    print(
        f'Creating Stripe customer {donor.get('FirstName')} {donor.get('LastName')} with email {email} in Salesforce')
    create_response = Donor.create(**donor)
    if 'success' in create_response:
        success = create_response.get('success')
        if success:
            salesforce_id = create_response.get('id')
            print(
                f'Created Stripe customer with email {email} successfully in Salesforce with ID {salesforce_id}')
        else:
            errors = create_response.get('errors')
            error_message = f'Did not create Stripe customer with {email} successfully in Salesforce due to: {errors}'
            raise Exception(error_message)


def update_donor_in_salesforce(sf_contact_id: str, donor: dict) -> None:
    response = Donor.update(sf_contact_id, **donor)
    if response != 204:
        errors = response.get('errors')
        error_message = f'Did not update Salesforce Contact {sf_contact_id} successfully in Salesforce due to {errors}'
        print(error_message)
        raise Exception(error_message)
    print(
        f'Updated Salesforce Contact {sf_contact_id} successfully in Salesforce.')


def update_donor_in_Stripe(stripe_customer_id: str, stripe_updates: dict) -> None:
    Donor.update_stripe_customer(stripe_customer_id, stripe_updates)


class DonorProcessor:
    @staticmethod
    def process_create_event(event_data):
        donor = DonorMapper.map_donor_create_event(**event_data)
        stripe_customer_id = donor.get('External_Contact_ID__c')
        stripe_updates = donor.pop('stripe_updates', None)
        email = donor.get('Email')
        if email is None:
            raise Exception('Donor email is null.  Cannot process donor create event further.')
        sf_contact_id = Donor.exists_by_email(email)
        if not sf_contact_id:
            create_donor_in_salesforce(donor)
            if stripe_updates:
                update_donor_in_Stripe(stripe_customer_id, stripe_updates)
        else:
            error_message = f'Stripe customer with email {email} already exists in Salesforce with ID {sf_contact_id}. Cannot process donor create event further.'
            raise Exception(error_message)

    @staticmethod
    def process_update_event(event_data):
        donor = DonorMapper.map_donor_update_event(**event_data)
        stripe_customer_id = donor.get('External_Contact_ID__c')
        stripe_updates = donor.pop('stripe_updates', None)
        email = donor.get('Email')
        if email is None:
            raise Exception('Donor email is null.  Cannot process donor update event further.')
        sf_contact_id = Donor.exists_by_email(email)
        if not sf_contact_id:
            error_message = f'Stripe customer with email {email} does not exist in Salesforce. Cannot process donor update event further.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        else:
            update_donor_in_salesforce(sf_contact_id, donor)
            if stripe_updates:
                update_donor_in_Stripe(stripe_customer_id, stripe_updates)
