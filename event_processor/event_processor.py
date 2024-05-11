import json

from donations.donation_processor import DonationProcessor
from donors.donor_processor import DonorProcessor
import utils.database_connection
from subscriptions.subscription_processor import SubscriptionProcessor


class EventProcessor:

    @staticmethod
    def process_donor_event(ch, method, properties, body):
        try:
            donor_event = json.loads(body)
            print(f'donor event: {donor_event}')
            if donor_event['type'] == 'customer.created':
                response = DonorProcessor.process_create_event(donor_event)
                if response:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor create event: {donor_event}')
                else:
                    print(f'Error processing donor create event: {donor_event}')
            else:
                response = DonorProcessor.process_update_event(donor_event)
                if response:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    print(f'Error processing donor update event: {donor_event}')
        except Exception as e:
            print(f'Error in process_donor_event due to {e}')

    @staticmethod
    def process_subscription_event(ch, method, properties, body):
        subscription_event = json.loads(body)
        print(f'donor event: {subscription_event}')
        if subscription_event['type'] == 'customer.subscription.created':
            response = SubscriptionProcessor.process_create_event(subscription_event)
            if response:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print(f'Error processing subscription create event: {subscription_event}')
        elif subscription_event['type'] == 'customer.subscription.deleted':
            response = SubscriptionProcessor.process_delete_event(subscription_event)
            if response:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print(f'Error processing subscription delete event: {subscription_event}')
        else:
            response = SubscriptionProcessor.process_update_event(subscription_event)
            if response:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print(f'Error processing subscription update event: {subscription_event}')

    @staticmethod
    def process_donation_event(ch, method, properties, body):
        try:
            donation_event = json.loads(body)
            print(f'donation event: {donation_event}')
            if donation_event['type'] == 'customer.created':
                response = DonationProcessor.process_create_event(donation_event)
                if response:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    print(f'Error processing donation create event: {donation_event}')
            else:
                response = DonationProcessor.process_update_event(donation_event)
                if response:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    print(f'Error processing donation update event: {donation_event}')
        except Exception as e:
            print(f'Error in process_donation_event due to {e}')

