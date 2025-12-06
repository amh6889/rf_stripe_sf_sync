import time

from donations.donation_mapper import DonationMapper
from donations.donation_salesforce_service import SalesforceDonationService
from donations.donation_stripe_service import StripeDonationService
from email.salesforce_email_service import SalesforceEmailService


class DonationEventService:
    def __init__(self, donation_mapper: DonationMapper, salesforce_donation: SalesforceDonationService,
                 stripe_donation_service: StripeDonationService):
        self.donation_mapper = donation_mapper
        self.salesforce_donation = salesforce_donation
        self.stripe_donation_service = stripe_donation_service

    def process_create_event(self, donation_event):
        donation = self.donation_mapper.map_donation(**donation_event)
        stripe_invoice_id = donation.get('Stripe_Invoice_ID__c')
        sf_donation_id = self.salesforce_donation.exists(stripe_invoice_id)
        if not sf_donation_id:
            self._create_donation_in_salesforce(stripe_invoice_id, donation)
        else:
            error_message = f'Stripe charge {stripe_invoice_id} already exists in Salesforce with Donation ID {sf_donation_id}. Cannot process donation create event further.'
            print(error_message)
            raise Exception(error_message)

    def process_failure_event(self, failure_event):
        data = failure_event['data']['object']
        stripe_invoice_id = data.get('id')
        print(f'Processing donation failure event for invoice id {stripe_invoice_id}')
        billing_reason = data.get('billing_reason')
        accepted_failed_billing_reasons = ['subscription_cycle', 'subscription_update', 'subscription_update', 'upcoming']

        if billing_reason in accepted_failed_billing_reasons:
            try:
                salesforce_email_service = SalesforceEmailService()
                charge_id = data.get('charge')
                stripe_subscription_id = data.get('subscription')
                charge = self.stripe_donation_service.get_stripe_charge_by_id(charge_id)
                last4 = self.donation_mapper.get_payment_method_last_4(charge)
                salesforce_email_service.send_email(stripe_subscription_id, last4)
                #failure_message = charge.get('failure_message')
                #failure_code = charge.get('failure_code')
            except Exception as e:
                print(f'Error processing donation failure due to: {str(e)}')
                raise Exception(e)


    def process_refund_event(self, refund_event):
        data = refund_event['data']['object']
        stripe_charge_id = data.get('id')
        sf_donation_id = self.salesforce_donation.exists(stripe_charge_id)
        if sf_donation_id:
            refund = self.donation_mapper.map_refund(stripe_charge_id)
            self._update_donation_in_salesforce(stripe_charge_id, sf_donation_id, refund)
        else:
            error_message = f'Stripe charge {stripe_charge_id} does not exist in Salesforce. Cannot process donation refund event.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)

    def process_update_event(self, donation_event):
        donation = self.donation_mapper.map_donation(**donation_event)
        stripe_invoice_id = donation.get('Stripe_Invoice_ID__c')
        sf_donation_id = self.salesforce_donation.exists(stripe_invoice_id)
        if sf_donation_id:
            self._update_donation_in_salesforce(stripe_invoice_id, sf_donation_id, donation)
        else:
            error_message = f'Stripe charge {stripe_invoice_id} does not exist in Salesforce. Cannot process donation update event.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)

    def _create_donation_in_salesforce(self, stripe_invoice_id, donation):
        response = self.salesforce_donation.create(**donation)
        if 'success' in response:
            success = response.get('success')
            if success:
                salesforce_id = response.get('id')
                print(
                    f'Created Stripe donation {stripe_invoice_id} successfully in Salesforce with ID {salesforce_id}')
            else:
                errors = response.get('errors')
                error_message = f'Did not create Stripe donation {stripe_invoice_id} successfully in Salesforce due to: {errors}'
                raise Exception(error_message)

    def _update_donation_in_salesforce(self, stripe_invoice_id, sf_donation_id, donation):
        response = self.salesforce_donation.update(sf_donation_id, **donation)
        if response != 204:
            errors = response.get('errors')
            error_message = f'Did not update Stripe charge {stripe_invoice_id} successfully in Salesforce due to {errors}'
            print(error_message)
            raise Exception(error_message)
        print(f'Updated Stripe charge {stripe_invoice_id} successfully in Salesforce.')
