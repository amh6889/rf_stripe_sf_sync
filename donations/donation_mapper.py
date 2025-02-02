import locale
import time
from builtins import str
from datetime import datetime, UTC

from donations.donation_stripe_service import StripeDonationService
from donors.donor_salesforce_service import SalesforceDonorService
from donors.donor_stripe_service import StripeDonorService
from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService


def get_closed_date(data: dict) -> str:
    epoch_time = data.get('created')
    date_time = datetime.fromtimestamp(epoch_time, UTC)
    return date_time.isoformat()


def map_stage_name(data: dict) -> str:
    stripe_donation_status = data.get('status')
    stage_name = 'Unknown'
    if stripe_donation_status == 'succeeded':
        stage_name = 'Closed Won'
    if stripe_donation_status == 'failed':
        stage_name = 'Withdrawn'
    if stripe_donation_status == 'pending':
        stage_name = 'Pledged'
    return stage_name


def get_payment_method_last_4(data: dict) -> str:
    stripe_payment_method = data.get('payment_method_details')
    payment_method_type = stripe_payment_method.get('type')
    if payment_method_type == 'card':
        last_4_digits = stripe_payment_method['card']['last4']
    elif payment_method_type == 'us_bank_account':
        last_4_digits = stripe_payment_method['us_bank_account']['last4']
    else:
        print(f'Payment method type {payment_method_type} is not supported')
        raise Exception(f'Payment method type {payment_method_type} is not supported')
    return last_4_digits


def get_amount(data: dict):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    formatted_amount = locale.currency(data.get('amount') / 100, symbol=False)
    return formatted_amount


# TODO: figure out situation below if salesforce id of existing subscription is different than one in event data.  This sometimes happened with ANET when a husband and wife had a subscription each had their own subscriptions in ANET but the wife had used the husband's email instead of her own and messed up the sync
class DonationMapper:

    def __init__(self, salesforce_subscription: SalesforceSubscriptionService, salesforce_donor: SalesforceDonorService,
                 stripe_donor: StripeDonorService, stripe_donation: StripeDonationService):
        self.salesforce_donor = salesforce_donor
        self.stripe_donor = stripe_donor
        self.stripe_donation = stripe_donation
        self.salesforce_subscription = salesforce_subscription

    def map_donation(self, **event_data):
        donation_source = 'RF Web-form'
        salesforce_id = None
        data = event_data['data']['object']
        charge_id = data.get('id')
        amount = get_amount(data)
        stripe_customer_id = data.get('customer')
        donor_email = self.stripe_donor.get_donor_email(stripe_customer_id)
        if donor_email:
            salesforce_id = self.salesforce_donor.get_contact_id(donor_email)
        if not salesforce_id:
            time.sleep(30)
            raise Exception(
                f'Donation event error: Stripe customer {stripe_customer_id} with email {donor_email} does not exist in Salesforce')

        closed_date = get_closed_date(data)
        stage_name = map_stage_name(data)
        last_4_digits = get_payment_method_last_4(data)

        stripe_subscription_id = None
        salesforce_subscription_id = None
        if stripe_invoice_id := data.get('invoice'):
            if stripe_subscription_id := self.stripe_donation.get_stripe_subscription_by_invoice_id(stripe_invoice_id):
                salesforce_subscription_id = self._get_salesforce_recurring_donation_id(stripe_subscription_id)

        donation = {'npe01__Contact_Id_for_Role__c': salesforce_id,
                    'npsp__Primary_Contact__c': salesforce_id,
                    'Amount': amount,
                    'CloseDate': closed_date,
                    'Donation_Source__c': donation_source,
                    'StageName': stage_name,
                    'Name': f'${amount} {donation_source}',
                    'npe03__Recurring_Donation__c': salesforce_subscription_id,
                    'Card_Last_4__c': last_4_digits,
                    'Stripe_Invoice_ID__c': charge_id,
                    'Stripe_Subscription_ID__c': stripe_subscription_id
                    }
        return donation

    def map_refund(self, stripe_charge_id: str) -> dict:
        donation = {'StageName': 'Withdrawn', 'Stripe_Invoice_ID__c': stripe_charge_id}
        return donation

    def _get_salesforce_recurring_donation_id(self, stripe_subscription_id: str) -> str:
        salesforce_recurring_donation_id = None
        if stripe_subscription_id:
            if salesforce_recurring_donation := self.salesforce_subscription.get_by_stripe_id(stripe_subscription_id):
                salesforce_recurring_donation_id = salesforce_recurring_donation.get('id')
                # salesforce_id = salesforce_recurring_donation['sf_contact_id']
            else:
                time.sleep(30)
                raise Exception(
                    f'Donation event error: Stripe subscription {stripe_subscription_id} does not exist in Salesforce')
        return salesforce_recurring_donation_id
