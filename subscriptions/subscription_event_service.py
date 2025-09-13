import time

from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService
from subscriptions.subscription_mapper import SubscriptionMapper


class SubscriptionEventService:

    def __init__(self, mapper: SubscriptionMapper, salesforce_subscription: SalesforceSubscriptionService):
        self._mapper = mapper
        self._salesforce_subscription = salesforce_subscription

    def process_create_event(self, event_data: dict) -> str:
        salesforce_subscription_id = None
        subscription = self._mapper.map_create_event(**event_data)
        stripe_subscription_id = subscription.get('Stripe_Subscription_ID__c')
        if sf_subscription_id := self._salesforce_subscription.get_by_stripe_id(stripe_subscription_id):
            error_message = f'Stripe subscription {stripe_subscription_id} already exists in Salesforce with Recurring Donation ID {sf_subscription_id}. Cannot process subscription create event further.'
            print(error_message)
            raise Exception(error_message)
        else:
            if anet_subscription_id := subscription.get('ANET_ARB_ID__c'):
                salesforce_subscription_id = self._update_existing_salesforce_subscription(anet_subscription_id, stripe_subscription_id,
                                                              subscription)
            else:
                salesforce_subscription_id = self._create_salesforce_subscription(stripe_subscription_id, subscription)
        return salesforce_subscription_id

    def process_update_event(self, event_data: dict) -> bool:
        success = False
        subscription = self._mapper.map_update_event(**event_data)
        stripe_subscription_id = subscription.get('Stripe_Subscription_ID__c')
        if sf_subscription := self._salesforce_subscription.get_by_stripe_id(stripe_subscription_id):
            self._update_salesforce_subscription(sf_subscription, stripe_subscription_id, subscription)
        else:
            error_message = f'Stripe subscription {stripe_subscription_id} does not exist in Salesforce. Cannot process subscription update event further.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        success = True
        return success

    def process_delete_event(self, subscription_event: dict) -> bool:
        success = False
        subscription = self._mapper.map_delete_event(**subscription_event)
        stripe_subscription_id = subscription.get('Stripe_Subscription_ID__c')
        if sf_subscription := self._salesforce_subscription.get_by_stripe_id(stripe_subscription_id):
            self._update_salesforce_subscription(sf_subscription, stripe_subscription_id, subscription)
            print(
                f'Processed Stripe subscription {stripe_subscription_id}/Salesforce Recurring Donation ID '
                f'{sf_subscription.get('id')} as {subscription.get('npsp__Status__c')} successfully in Salesforce.')
        else:
            error_message = f'Stripe subscription {stripe_subscription_id} does not exist in Salesforce. Cannot process subscription delete event further.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        success = True
        return success

    def _create_salesforce_subscription(self, stripe_subscription_id: str, subscription: dict) -> str:
        salesforce_id = None
        response = self._salesforce_subscription.create(**subscription)
        if 'success' in response:
            success = response.get('success')
            if success:
                salesforce_id = response.get('id')
                print(
                    f'Created Stripe subscription {stripe_subscription_id} successfully in Salesforce with ID {salesforce_id}')
            else:
                errors = response.get('errors')
                error_message = f'Did not create Stripe subscription {stripe_subscription_id} successfully in Salesforce due to: {errors}'
                raise Exception(error_message)
        return salesforce_id

    def _update_existing_salesforce_subscription(self, anet_subscription_id: str, stripe_subscription_id: str, subscription: dict) -> str:
        if sf_subscription := self._salesforce_subscription.get_by_anet_id(anet_subscription_id):
            self._update_salesforce_subscription(sf_subscription, stripe_subscription_id, subscription)
            return sf_subscription.get('id')
        else:
            raise Exception(
                f"Cannot update Salesforce recurring donation with Stripe subscription ID {stripe_subscription_id} since it doesn't exist based on ANET subscription ID {anet_subscription_id}")


    def _update_salesforce_subscription(self, sf_subscription, stripe_subscription_id, subscription):
        sf_subscription_id = sf_subscription.get('id')
        response = self._salesforce_subscription.update(sf_subscription_id, **subscription)
        if response != 204:
            errors = response.get('errors')
            error_message = f'Did not update Stripe subscription {stripe_subscription_id} successfully in Salesforce due to {errors}'
            print(error_message)
            raise Exception(error_message)
        print(
            f'Updated Stripe subscription {stripe_subscription_id} successfully in Salesforce.')
