import datetime
import locale
import time

from donors.donor import Donor
from subscriptions.subscription import Subscription
from subscriptions.subscription_mapper import SubscriptionMapper


def update_existing_anet_subscription(anet_subscription_id, stripe_subscription_id, subscription):
    sf_subscription = Subscription.search_by_anet_id(anet_subscription_id)
    if sf_subscription:
        update_subscription(sf_subscription, stripe_subscription_id, subscription)
    else:
        raise Exception(f"Cannot update Salesforce recurring donation with Stripe subscription ID {stripe_subscription_id} since it doesn't exist based on ANET subscription ID {anet_subscription_id}")


def update_subscription(sf_subscription, stripe_subscription_id, subscription):
    sf_subscription_id = sf_subscription.get('id')
    response = Subscription.update(sf_subscription_id, **subscription)
    if response != 204:
        errors = response.get('errors')
        error_message = f'Did not update Stripe subscription {stripe_subscription_id} successfully in Salesforce due to {errors}'
        print(error_message)
        raise Exception(error_message)
    print(
        f'Updated Stripe subscription {stripe_subscription_id} successfully in Salesforce.')


def create_subscription(stripe_subscription_id, subscription):
    create_response = Subscription.create(**subscription)
    if 'success' in create_response:
        success = create_response.get('success')
        if success:
            salesforce_id = create_response.get('id')
            print(
                f'Created Stripe subscription {stripe_subscription_id} successfully in Salesforce with ID {salesforce_id}')
        else:
            errors = create_response.get('errors')
            error_message = f'Did not create Stripe subscription {stripe_subscription_id} successfully in Salesforce due to: {errors}'
            raise Exception(error_message)


class SubscriptionProcessor:
    @staticmethod
    def process_create_event(event_data):
        subscription = SubscriptionMapper.map_active_subscription(**event_data)
        stripe_subscription_id = subscription.get('Stripe_Subscription_ID__c')
        if stripe_subscription_id is None:
            raise Exception('Stripe subscription ID is null.  Cannot process subscription create event further.')
        sf_subscription_id = Subscription.search_by_stripe_id(stripe_subscription_id)
        if not sf_subscription_id:
            anet_subscription_id = subscription.get('ANET_ARB_ID__c')
            if anet_subscription_id is not None:
                update_existing_anet_subscription(anet_subscription_id, stripe_subscription_id, subscription)
            else:
                create_subscription(stripe_subscription_id, subscription)
        else:
            error_message = f'Stripe subscription {stripe_subscription_id} already exists in Salesforce with Recurring Donation ID {sf_subscription_id}. Cannot process subscription create event further.'
            print(error_message)
            raise Exception(error_message)

    @staticmethod
    def process_update_event(event_data):
        subscription = SubscriptionMapper.map_active_subscription(**event_data)
        stripe_subscription_id = subscription.get('Stripe_Subscription_ID__c')
        if stripe_subscription_id is None:
            raise Exception('Stripe subscription ID is null.  Cannot process subscription update event further.')
        sf_subscription = Subscription.search_by_stripe_id(stripe_subscription_id)
        if not sf_subscription:
            error_message = f'Stripe subscription {stripe_subscription_id} does not exist in Salesforce. Cannot process subscription update event further.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        else:
            update_subscription(sf_subscription, stripe_subscription_id, subscription)

    @staticmethod
    def process_delete_event(subscription_event):
        subscription = SubscriptionMapper.map_canceled_subscription(**subscription_event)
        stripe_subscription_id = subscription.get('Stripe_Subscription_ID__c')
        if stripe_subscription_id is None:
            raise Exception('Stripe subscription ID is null.  Cannot process subscription delete event further.')
        sf_subscription = Subscription.search_by_stripe_id(stripe_subscription_id)
        if not sf_subscription:
            error_message = f'Stripe subscription {stripe_subscription_id} does not exist in Salesforce. Cannot process subscription delete event further.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        else:
            update_subscription(sf_subscription, stripe_subscription_id, subscription)
            print(
                f'Canceled Stripe subscription {stripe_subscription_id}/Salesforce Recurring Donation ID '
                f'{sf_subscription.get('id')} successfully in Salesforce.')
