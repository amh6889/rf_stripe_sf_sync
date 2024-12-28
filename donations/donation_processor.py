import time

from donations.donation import Donation
from donations.donation_mapper import DonationMapper


def create_donation_in_salesforce(stripe_invoice_id, donation):
    create_response = Donation.create(**donation)
    if 'success' in create_response:
        success = create_response.get('success')
        if success:
            salesforce_id = create_response.get('id')
            print(
                f'Created Stripe donation {stripe_invoice_id} successfully in Salesforce with ID {salesforce_id}')
        else:
            errors = create_response.get('errors')
            error_message = f'Did not create Stripe donation {stripe_invoice_id} successfully in Salesforce due to: {errors}'
            raise Exception(error_message)


def update_donation_in_salesforce(stripe_invoice_id, sf_donation_id, donation):
    response = Donation.update(sf_donation_id, **donation)
    if response != 204:
        errors = response.get('errors')
        error_message = f'Did not update Stripe charge {stripe_invoice_id} successfully in Salesforce due to {errors}'
        print(error_message)
        raise Exception(error_message)
    print(f'Updated Stripe charge {stripe_invoice_id} successfully in Salesforce.')


class DonationProcessor:
    @staticmethod
    def process_create_event(donation_event):
        donation = DonationMapper.map_donation(**donation_event)
        stripe_invoice_id = donation.get('Stripe_Invoice_ID__c')
        if not stripe_invoice_id:
            raise Exception('Stripe charge ID is null.  Cannot process donation create event further.')
        sf_donation_id = Donation.exists(stripe_invoice_id)
        if not sf_donation_id:
            create_donation_in_salesforce(stripe_invoice_id, donation)
        else:
            error_message = f'Stripe charge {stripe_invoice_id} already exists in Salesforce with Donation ID {sf_donation_id}. Cannot process donation create event further.'
            print(error_message)
            raise Exception(error_message)

    @staticmethod
    def process_refund_event(refund_event):
        sf_donation_id, refund = DonationMapper.map_refund(**refund_event)
        stripe_charge_id = refund.get('Stripe_Invoice_ID__c')
        response = Donation.update(sf_donation_id, **refund)
        if response != 204:
            errors = response.get('errors')
            error_message = f'Did not update Stripe charge {stripe_charge_id} successfully as refund in Salesforce due to {errors}'
            print(error_message)
            raise Exception(error_message)
        print(f'Updated Stripe charge {stripe_charge_id} successfully in Salesforce as a refund.')

    @staticmethod
    def process_update_event(donation_event):
        donation = DonationMapper.map_donation(**donation_event)
        stripe_invoice_id = donation.get('Stripe_Invoice_ID__c')
        if not stripe_invoice_id:
            raise Exception('Stripe charge ID is null.  Cannot process donation update event further.')
        sf_donation_id = Donation.exists(stripe_invoice_id)
        if not sf_donation_id:
            error_message = f'Stripe charge {stripe_invoice_id} does not exist in Salesforce. Cannot process donation update event.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        else:
            update_donation_in_salesforce(stripe_invoice_id, sf_donation_id, donation)
