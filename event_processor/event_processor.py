import json

from donations.donation_processor import DonationProcessor
from donors.donor_processor import DonorProcessor
from subscriptions.subscription_processor import SubscriptionProcessor
from utils import slack_notifier


#TODO: make a poison queue for messages that are repeatedly processed.  Perhaps after 10 times of processing message put it on a poison queue and send a slack message
class EventProcessor:

    @staticmethod
    def process_dead_letter_messages(ch, method, properties, body):
        try:
            dead_letter_json = json.loads(body)
            print(dead_letter_json)
            slack_notifier.send_message(str(dead_letter_json))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as error:
            print(error)

    @staticmethod
    def process_donor_event(ch, method, properties, body):
        try:
            donor_event = json.loads(body)
            print(f'donor event: {donor_event}')
            if donor_event['type'] == 'customer.created':
                response = DonorProcessor.process_create_event(donor_event)
                if response:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor create event id: {donor_event['id']}')
                else:
                    message = f'Error processing donor create event id: {donor_event['id']}: {donor_event}'
                    print(message)
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            elif donor_event['type'] == 'customer.updated':
                response = DonorProcessor.process_update_event(donor_event)
                if response:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor update event id: {donor_event['id']}')
                else:
                    message = f'Error processing donor update event id: {donor_event['id']}: {donor_event}'
                    print(message)
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                print(f'Unknown donor event type: {donor_event['type']}')
        except Exception as e:
            print(f'Error in process_donor_event due to {e}')

    @staticmethod
    def process_subscription_event(ch, method, properties, body):
        try:
            subscription_event = json.loads(body)
            print(f'subscription  event: {subscription_event}')
            if subscription_event['type'] == 'customer.subscription.created':
                response = SubscriptionProcessor.process_create_event(subscription_event)
                if response:
                    print(f'Subscription create event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    message = f'Error processing subscription create event id: {subscription_event['id']}: {subscription_event}'
                    print(message)
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            elif subscription_event['type'] == 'customer.subscription.deleted':
                success = SubscriptionProcessor.process_delete_event(subscription_event)
                if success:
                    print(f'Subscription delete event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    message = f'Error processing subscription delete event id: {subscription_event['id']}: {subscription_event}'
                    print(message)
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            elif subscription_event['type'] == 'customer.subscription.updated':
                response = SubscriptionProcessor.process_update_event(subscription_event)
                if response:
                    print(f'Subscription update event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    message = f'Error processing subscription update event id: {subscription_event['id']}: {subscription_event}'
                    print(message)
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                print(f'Unknown subscription event: {subscription_event['type']}')
        except Exception as e:
            print(f'Error in process_subscription_event due to {e}')

    @staticmethod
    def process_donation_event(ch, method, properties, body):
        try:
            donation_event = json.loads(body)
            print(f'donation event: {donation_event}')
            if donation_event['type'] == 'charge.succeeded':
                response = DonationProcessor.process_create_event(donation_event)
                if response:
                    print(f'Donation create event id: {donation_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    message = f'Error processing donation create event id: {donation_event['id']}: {donation_event}'
                    print(message)
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            elif donation_event['type'] == 'charge.refunded':
                response = DonationProcessor.process_update_event(donation_event)
                if response:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    message = f'Error processing donation update event id: {donation_event['id']}: {donation_event}'
                    print(message)
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            else:
                print(f'Unknown donation event: {donation_event['type']}')
        except Exception as e:
            print(f'Error in process_donation_event due to {e}')

