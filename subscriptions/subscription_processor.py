import datetime
import locale
from donors.donor import Donor
from subscriptions.subscription import Subscription


class SubscriptionProcessor:

    @staticmethod
    def _map_active_subscription(**event_data):
        data = event_data['data']['object']
        status = data['status']
        mapped_status, closed_reason = SubscriptionProcessor._map_status(status)
        subscription_id = data['id']

        amount = data['plan']['amount'] * data['quantity']
        locale.setlocale(locale.LC_ALL, '')
        formatted_amount = locale.currency(amount / 100, symbol=False)
        created = data['created']
        start_date = data['start_date']
        day_of_month, date_start = SubscriptionProcessor._parse_epoch_time(created)
        stripe_customer_id = data['customer']
        email = Donor.get_email(stripe_customer_id)
        salesforce_id = Donor.exists_by_email(email)
        interval = data['plan']['interval']
        installment_period = SubscriptionProcessor._map_installment_period(interval)
        payment_method = Subscription.get_payment_method(subscription_id)
        payment_method_type = payment_method['type']
        mapped_payment_method_type = SubscriptionProcessor._map_payment_method(payment_method_type)
        # last4 = payment_method_type[payment_method_type]['last4']
        installment_frequency = data['plan']['interval_count']

        subscription = {'Stripe_Subscription_ID__c': subscription_id, 'npe03__Amount__c': formatted_amount,
                        'npe03__Date_Established__c': date_start,
                        'npsp__StartDate__c': date_start, 'npsp__EndDate__c': None,
                        'Donation_Source__c': 'RF Web-form',
                        'npsp__Status__c': mapped_status, 'npsp__ClosedReason__c': closed_reason,
                        'npe03__Recurring_Donation_Campaign__c': None,
                        'npsp__RecurringType__c': 'Open', 'npe03__Installment_Period__c': installment_period,
                        'npsp__Day_of_Month__c': day_of_month,
                        'npsp__InstallmentFrequency__c': installment_frequency,
                        'npsp__PaymentMethod__c': mapped_payment_method_type,
                        'npe03__Installments__c': None, 'npe03__Contact__c': salesforce_id}
        return subscription

    @staticmethod
    def _parse_epoch_time(epoch_time):
        date_time = datetime.datetime.fromtimestamp(epoch_time, datetime.UTC)
        return date_time.day, date_time.isoformat()

    @staticmethod
    def process_create_event(event_data):
        try:
            subscription = SubscriptionProcessor._map_active_subscription(**event_data)
            sf_subscription_id = Subscription.exists(subscription['Stripe_Subscription_ID__c'])
            if not sf_subscription_id:
                create_response = Subscription.create(**subscription)
                if 'success' in create_response:
                    success = create_response['success']
            else:
                success = True
                print(
                    f'Stripe subscription {subscription['Stripe_Subscription_ID__c']} already exists in Salesforce. Cannot process create event.')
            return success
        except Exception as error:
            print(error)
            return False

    @staticmethod
    def process_update_event(event_data):
        update_success = False
        try:
            subscription = SubscriptionProcessor._map_active_subscription(**event_data)
            sf_subscription_id = Subscription.exists(subscription['Stripe_Subscription_ID__c'])
            if not sf_subscription_id:
                print(
                    f'Stripe subscription {subscription['Stripe_Subscription_ID__c']} does not exist in Salesforce. Cannot process update event.')
            else:
                response = Subscription.update(sf_subscription_id, **subscription)
                if response == 204:
                    update_success = True
        except Exception as error:
            print(error)
        return update_success



    @staticmethod
    def process_delete_event(subscription_event):
        update_success = False
        try:
            subscription = SubscriptionProcessor._map_canceled_subscription(**subscription_event)
            sf_subscription_id = Subscription.exists(subscription['Stripe_Subscription_ID__c'])
            if not sf_subscription_id:
                print(
                    f'Stripe subscription {subscription['Stripe_Subscription_ID__c']} does not exist in Salesforce. Cannot process delete event.')

            else:
                response = Subscription.update(sf_subscription_id, **subscription)
                if response == 204:
                    update_success = True
        except Exception as error:
            print(error)
        return update_success

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
    def _map_canceled_subscription(**event_data):
        try:
            data = event_data['data']['object']
            status = data['status']
            mapped_status, closed_reason = SubscriptionProcessor._map_status(status)
            subscription_id = data['id']
            subscription = {'Stripe_Subscription_ID__c':subscription_id, 'npsp__Status__c': mapped_status,
                            'npsp__ClosedReason__c': closed_reason}

            return subscription
        except Exception as error:
            print(f'Error mapping canceled subscription due to {error}')


