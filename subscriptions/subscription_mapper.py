import locale
from datetime import datetime, UTC

from donors.donor import Donor
from subscriptions.subscription import Subscription


class SubscriptionMapper:

    @staticmethod
    def map_active_subscription(**event_data):
        data = event_data['data']['object']
        status = data.get('status')
        mapped_status, closed_reason = SubscriptionMapper._map_status(status)
        subscription_id = data.get('id')
        sf_campaign_id = None
        mapped_payment_method_type = None
        anet_subscription_id = None
        if metadata := data.get('metadata'):
            if campaign_code := metadata.get('campaign_code'):
                sf_campaign_id = Subscription.get_campaign_id(campaign_code)
            anet_subscription_id = metadata.get('anetSubscriptionId')

        amount = data['plan']['amount'] * data['quantity']
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        formatted_amount = locale.currency(amount / 100, symbol=False)
        created = data.get('created')
        day_of_month, date_start = SubscriptionMapper._parse_epoch_time(created)
        stripe_customer_id = data['customer']
        email = Donor.get_email(stripe_customer_id)
        salesforce_id = Donor.exists_by_email(email)
        interval = data['plan']['interval']
        installment_period = SubscriptionMapper._map_installment_period(interval)

        if payment_method := Subscription.get_payment_method(subscription_id):
            if payment_method_type := payment_method.get('type'):
                mapped_payment_method_type = SubscriptionMapper._map_payment_method(payment_method_type)

        installment_frequency = data['plan']['interval_count']

        subscription = {'Stripe_Subscription_ID__c': subscription_id, 'npe03__Amount__c': formatted_amount,
                        'npe03__Date_Established__c': date_start,
                        'npsp__StartDate__c': date_start, 'npsp__EndDate__c': None,
                        'Donation_Source__c': 'RF Web-form',
                        'npsp__Status__c': mapped_status, 'npsp__ClosedReason__c': closed_reason,
                        'npe03__Recurring_Donation_Campaign__c': sf_campaign_id,
                        'npsp__RecurringType__c': 'Open', 'npe03__Installment_Period__c': installment_period,
                        'npsp__Day_of_Month__c': day_of_month,
                        'npsp__InstallmentFrequency__c': installment_frequency,
                        'npsp__PaymentMethod__c': mapped_payment_method_type,
                        'npe03__Installments__c': None, 'npe03__Contact__c': salesforce_id,
                        'ANET_ARB_ID__c': anet_subscription_id}
        return subscription

    @staticmethod
    def _parse_epoch_time(epoch_time):
        date_time = datetime.fromtimestamp(epoch_time, UTC)
        return date_time.day, date_time.isoformat()

    @staticmethod
    def _map_installment_period(interval):
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

    @staticmethod
    def _map_status(status):
        subscription_status = ''
        closed_reason = ''
        match status:
            case "active":
                subscription_status = 'Active'
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
            case "unpaid":
                subscription_status = 'Suspended'
                closed_reason = 'Unknown'
            case _:
                print("Unknown status:" + str(status))
        return subscription_status, closed_reason

    @staticmethod
    def _map_payment_method(payment_method_type):
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

    @staticmethod
    def map_canceled_subscription(**event_data):
        try:
            data = event_data['data']['object']
            status = data['status']
            mapped_status, closed_reason = SubscriptionMapper._map_status(status)
            subscription_id = data['id']
            subscription = {'Stripe_Subscription_ID__c': subscription_id, 'npsp__Status__c': mapped_status,
                            'npsp__ClosedReason__c': closed_reason}

            return subscription
        except Exception as error:
            print(f'Error mapping canceled subscription due to {error}')
