import json
import traceback

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
            match donor_event['type']:
                case 'customer.created':
                    DonorProcessor.process_create_event(donor_event)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor create event id: {donor_event['id']}')
                case 'customer.updated':
                    DonorProcessor.process_update_event(donor_event)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor update event id: {donor_event['id']}')
                case _:
                    print(f'Unknown donor event type: {donor_event['type']}')
        except Exception as e:
            print(f'Error in process_donor_event due to: {e}')
            if properties.headers.get('x-delivery-count') == 10:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(f'ERROR PROCESSING DONOR EVENT:\n{body}\nERROR MESSAGE: {e}\nSTACK TRACE: {stack_trace}')
            ch.basic_nack(delivery_tag=method.delivery_tag)

    @staticmethod
    def process_subscription_event(ch, method, properties, body):
        try:
            subscription_event = json.loads(body)
            print(f'subscription event: {subscription_event}')
            match subscription_event['type']:
                case 'customer.subscription.created':
                    SubscriptionProcessor.process_create_event(subscription_event)
                    print(f'Subscription create event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'customer.subscription.updated':
                    SubscriptionProcessor.process_update_event(subscription_event)
                    print(f'Subscription update event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'customer.subscription.deleted':
                    SubscriptionProcessor.process_delete_event(subscription_event)
                    print(f'Subscription delete event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case _:
                    print(f'Unknown subscription event: {subscription_event['type']}')
        except Exception as e:
            print(f'Error in process_subscription_event due to {e}')
            if properties.headers.get('x-delivery-count') == 10:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(f'ERROR PROCESSING SUBSCRIPTION EVENT:\n{body}\nERROR MESSAGE: {e}\nSTACK TRACE: {stack_trace}')
            ch.basic_nack(delivery_tag=method.delivery_tag)

    @staticmethod
    def process_donation_event(ch, method, properties, body):
        try:
            donation_event = json.loads(body)
            print(f'donation event: {donation_event}')
            match donation_event['type']:
                case 'charge.succeeded':
                    DonationProcessor.process_create_event(donation_event)
                    print(f'Donation create event id: {donation_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'charge.refunded':
                    DonationProcessor.process_update_event(donation_event)
                    print(f'Donation refund event id: {donation_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case _:
                    print(f'Unknown donation event: {donation_event['type']}')
        except Exception as e:
            print(f'Error in process_subscription_event due to {e}')
            if properties.headers.get('x-delivery-count') == 10:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(f'ERROR PROCESSING DONATION EVENT:\n{body}\nERROR MESSAGE: {e}\nSTACK TRACE: {stack_trace}')
            ch.basic_nack(delivery_tag=method.delivery_tag)

