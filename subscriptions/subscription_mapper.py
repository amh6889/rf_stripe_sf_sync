import locale
import time
from datetime import datetime, UTC, date, timedelta

from donors.donor_salesforce_service import SalesforceDonorService
from donors.donor_stripe_service import StripeDonorService
from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService
from subscriptions.subscription_stripe_service import StripeSubscriptionService


def get_amount(data: dict) -> str:
    amount = data['plan']['amount'] * data['quantity']
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    formatted_amount = locale.currency(amount / 100, symbol=False)
    return formatted_amount


def get_start_date(data: dict) -> datetime:
    epoch_time = data.get('billing_cycle_anchor')
    start_date = datetime.fromtimestamp(epoch_time, UTC)
    return start_date


def get_end_date(data: dict) -> datetime:
    epoch_time = data.get('end_date')
    end_date = datetime.fromtimestamp(epoch_time, UTC)
    return end_date


def map_payment_method(payment_method_type):
    mapped_payment_method_type = ''
    match payment_method_type:
        case "card":
            mapped_payment_method_type = 'Credit Card'
        case "us_bank_account":
            mapped_payment_method_type = 'ACH/EFT'
        case "acss_debit":
            mapped_payment_method_type = 'ACH/EFT/Canadian Bank'
        case "au_becs_debit":
            mapped_payment_method_type = 'ACH/EFT/Australian Bank'
        case "bacs_debit":
            mapped_payment_method_type = 'ACH/EFT/UK Bank'
        case "cashapp":
            mapped_payment_method_type = 'Cash App'
        case "paypal":
            mapped_payment_method_type = 'Pay Pal'
        case _:
            print("Unknown payment method:" + str(payment_method_type))
    return mapped_payment_method_type


def map_installment_period(data: dict) -> str:
    interval = data['plan']['interval']
    installment_period = ''
    match interval:
        case "month":
            installment_period = 'Monthly'
        case "week":
            installment_period = 'Weekly'
        case "year":
            installment_period = 'Yearly'
        case _:
            print("Unknown interval:" + str(interval))
    return installment_period


def map_status(status: str) -> tuple[str, str]:
    subscription_status = None
    closed_reason = None
    match status:
        case "active":
            subscription_status = 'Active'
        case "completed":
            subscription_status = 'Expired'
            closed_reason = 'Commitment Completed'
        case "incomplete":
            subscription_status = 'Paused'
        case "incomplete_expired":
            subscription_status = 'Canceled'
            closed_reason = 'Webform Canceled'
        case "past_due":
            subscription_status = 'Suspended'
            closed_reason = 'Unknown'
        case "canceled":
            subscription_status = 'Canceled'
            closed_reason = 'Webform Canceled'
        case "released":
            subscription_status = 'Canceled'
            closed_reason = 'Unknown'
        case "unpaid":
            subscription_status = 'Suspended'
            closed_reason = 'Unknown'
        case _:
            print("Unknown status:" + str(status))
    return subscription_status, closed_reason


def get_anet_subscription_id(subscription_schedule: dict) -> str:
    if subscription_schedule_metadata := subscription_schedule.get('metadata'):
        anet_subscription_id = subscription_schedule_metadata.get('anetSubscriptionId')
        return anet_subscription_id


def map_recurring_type(subscription: dict) -> str:
    recurring_type = 'Open'
    if subscription.get('cancel_at'):
        recurring_type = 'Fixed'
    return recurring_type


def map_anet_subscription(subscription_id: str, anet_subscription_id: str, mapped_status: str, closed_reason: str) -> dict:
    mapped_subscription = {'Stripe_Subscription_ID__c': subscription_id,
                           'ANET_ARB_ID__c': anet_subscription_id,
                           'npsp__Status__c': mapped_status,
                           'npsp__ClosedReason__c': closed_reason
                           }
    return mapped_subscription

def map_donation_source(data: dict) -> str:
    donation_source = 'RF Web-form'
    if metadata := data.get('metadata'):
        if source := metadata.get('donation_source'):
            donation_source = source
    return donation_source


class SubscriptionMapper:

    def __init__(self, stripe_subscription: StripeSubscriptionService,
                 salesforce_subscription: SalesforceSubscriptionService,
                 stripe_donor: StripeDonorService, salesforce_donor: SalesforceDonorService):
        self.stripe_subscription = stripe_subscription
        self.salesforce_subscription = salesforce_subscription
        self.stripe_donor = stripe_donor
        self.salesforce_donor = salesforce_donor

    def map_create_event(self, event_data):
        data = event_data['data']['object']
        subscription_id = data.get('id')
        donation_source = map_donation_source(data)
        status = data.get('status')
        mapped_status, closed_reason = map_status(status)

        if subscription_schedule := self.get_subscription_schedule(data):
            if anet_subscription_id := get_anet_subscription_id(subscription_schedule):
                return map_anet_subscription(subscription_id, anet_subscription_id, mapped_status, closed_reason)

        recurring_type = map_recurring_type(data)
        status = data.get('status')
        mapped_status, closed_reason = map_status(status)
        sf_campaign_id = self.map_campaign_code(data)
        amount = get_amount(data)
        start_date = get_start_date(data)
        salesforce_id = self._get_salesforce_contact_id(data)
        installment_period = map_installment_period(data)
        payment_method_type = self._get_payment_method_type(subscription_id)
        installment_frequency = data['plan']['interval_count']

        mapped_subscription = {'Stripe_Subscription_ID__c': subscription_id,
                               'npe03__Amount__c': amount,
                               'npe03__Date_Established__c': start_date.isoformat(),
                               'npsp__StartDate__c': start_date.isoformat(),
                               'Donation_Source__c': donation_source,
                               'npsp__Status__c': mapped_status,
                               'npsp__ClosedReason__c': closed_reason,
                               'npe03__Recurring_Donation_Campaign__c': sf_campaign_id,
                               'npsp__RecurringType__c': recurring_type,
                               'npe03__Installment_Period__c': installment_period,
                               'npsp__Day_of_Month__c': start_date.day,
                               'npsp__InstallmentFrequency__c': installment_frequency,
                               'npsp__PaymentMethod__c': payment_method_type,
                               'npe03__Contact__c': salesforce_id}

        return mapped_subscription

    def map_campaign_code(self, data: dict) -> str:
        if metadata := data.get('metadata'):
            if campaign_code := metadata.get('campaign_code'):
                sf_campaign_id = self.salesforce_subscription.get_campaign_id(campaign_code)
                return sf_campaign_id

    def get_subscription_schedule(self, data: dict) -> dict:
        if schedule_id := data.get('schedule'):
            subscription_schedule = self.stripe_subscription.get_subscription_schedule(schedule_id)
            return subscription_schedule

    def map_update_event(self, event_data):
        data = event_data['data']['object']
        subscription_id = data.get('id')
        donation_source = map_donation_source(data)
        recurring_type = map_recurring_type(data)
        status = data.get('status')
        mapped_status, closed_reason = map_status(status)
        amount = get_amount(data)
        start_date = get_start_date(data)
        installment_period = map_installment_period(data)
        payment_method_type = self._get_payment_method_type(subscription_id)
        installment_frequency = data['plan']['interval_count']

        subscription = {'Stripe_Subscription_ID__c': subscription_id,
                        'npe03__Amount__c': amount,
                        'npe03__Date_Established__c': start_date.isoformat(),
                        'npsp__StartDate__c': start_date.isoformat(),
                        'Donation_Source__c': donation_source,
                        'npsp__Status__c': mapped_status,
                        'npsp__ClosedReason__c': closed_reason,
                        'npsp__RecurringType__c': recurring_type,
                        'npe03__Installment_Period__c': installment_period,
                        'npsp__Day_of_Month__c': start_date.day,
                        'npsp__InstallmentFrequency__c': installment_frequency,
                        'npsp__PaymentMethod__c': payment_method_type}

        return subscription

    def _get_salesforce_contact_id(self, data: dict) -> str:
        stripe_customer_id = data.get('customer')
        email = self.stripe_donor.get_donor_email(stripe_customer_id)
        salesforce_id = self.salesforce_donor.get_contact_id(email)
        if salesforce_id is None:
            time.sleep(30)
            raise Exception(
                f'Subscription mapper error: Stripe donor {stripe_customer_id} does not exist in Salesforce')
        return salesforce_id

    def _get_payment_method_type(self, subscription_id) -> str:
        if payment_method := self.stripe_subscription.get_stripe_payment_method(subscription_id):
            if payment_method_type := payment_method.get('type'):
                mapped_payment_method_type = map_payment_method(payment_method_type)
                return mapped_payment_method_type

    def _map_delete_event_end_date(self, stripe_subscription_id: str, ended_at_timestamp: int) -> str | None:
        if salesforce_recurring_donation := self.salesforce_subscription.get_by_stripe_id(stripe_subscription_id):
            salesforce_recurring_donation_type = salesforce_recurring_donation.get('type')
            if 'fixed' in salesforce_recurring_donation_type.lower():
                ended_at = datetime.fromtimestamp(ended_at_timestamp)
                end_date = str(ended_at.date())
            else:
                # the below is to handle the subscription errors that occured whenever a user cancels his subscription on the same day as a donation goes through
                ended_at = datetime.fromtimestamp(ended_at_timestamp)
                # Add one day to the current date
                tomorrow = ended_at + timedelta(days=1)
                end_date = str(tomorrow.date())
            return end_date

    def map_delete_event(self, event_data):
        data = event_data['data']['object']
        stripe_subscription_id = data.get('id')
        ended_at = data.get('ended_at')

        end_date = self._map_delete_event_end_date(stripe_subscription_id, ended_at)

        if schedule_id := data.get('schedule'):
            sub_schedule = self.stripe_subscription.get_subscription_schedule(schedule_id)
            status = sub_schedule.get('status')
        else:
            status = data.get('status')

        mapped_status, closed_reason = map_status(status)

        subscription = {'Stripe_Subscription_ID__c': stripe_subscription_id, 'npsp__Status__c': mapped_status,
                        'npsp__ClosedReason__c': closed_reason, 'npsp__EndDate__c': end_date}

        return subscription
