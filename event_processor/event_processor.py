import json
import traceback

from donations.donation_event_processor import DonationEventProcessor
from donors.donor_event_processor import DonorEventProcessor
from subscriptions.subscription_event_processor import SubscriptionEventProcessor
from utils import slack_notifier
from datetime import datetime


class EventProcessor:
    def __init__(self, donation_event_processor: DonationEventProcessor, subscription_event_processor: SubscriptionEventProcessor,
                 donor_event_processor: DonorEventProcessor):
        self.donation_event_processor = donation_event_processor
        self.donor_event_processor = donor_event_processor
        self.subscription_event_processor = subscription_event_processor

    @staticmethod
    def process_dead_letter_messages(ch, method, properties, body):
        try:
            dead_letter_json = json.loads(body)
            print(dead_letter_json)
            slack_notifier.send_message(str(dead_letter_json))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as error:
            print(error)

    def process_donor_event(self, ch, method, properties, body):
        try:
            start_time = datetime.now()
            donor_event = json.loads(body)
            print(f'Processing donor event at {start_time}: {donor_event}')
            event_type = donor_event.get('type')
            event_id = donor_event.get('id')
            match event_type:
                case 'customer.created':
                    print(f'Processing donor create event id: {event_id}')
                    self.donor_event_processor.process_create_event(donor_event)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor create event id: {event_id}')
                case 'customer.updated':
                    print(f'Processing donor update event id: {event_id}')
                    self.donor_event_processor.process_update_event(donor_event)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor update event id: {event_id}')
                case _:
                    print(f'Unknown donor event type: {event_type}')
        except Exception as e:
            error_time = datetime.now()
            print(f'Error in process_donor_event at {error_time} due to: {e}')
            if properties.headers.get('x-delivery-count') == 30:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(
                    f'ERROR PROCESSING DONOR EVENT AT {error_time}:\n{body}\nERROR MESSAGE: {e}\nSTACK TRACE: {stack_trace}')
            ch.basic_nack(delivery_tag=method.delivery_tag)

    @staticmethod
    def process_subscription_event(ch, method, properties, body):
        try:
            start_time = datetime.now()
            subscription_event = json.loads(body)
            print(f'Processing subscription event at {start_time}: {subscription_event}')
            match subscription_event['type']:
                case 'customer.subscription.created':
                    SubscriptionEventProcessor.process_create_event(subscription_event)
                    print(f'Subscription create event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'customer.subscription.updated':
                    SubscriptionEventProcessor.process_update_event(subscription_event)
                    print(f'Subscription update event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'customer.subscription.deleted':
                    SubscriptionEventProcessor.process_delete_event(subscription_event)
                    print(f'Subscription delete event id: {subscription_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case _:
                    print(f'Unknown subscription event: {subscription_event['type']}')
        except Exception as e:
            error_time = datetime.now()
            print(f'Error in process_subscription_event at {error_time} due to {e}')
            if properties.headers.get('x-delivery-count') == 30:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(
                    f'ERROR PROCESSING SUBSCRIPTION EVENT AT {error_time}:\n{body}\nERROR MESSAGE: {e}\nSTACK TRACE: {stack_trace}')
            ch.basic_nack(delivery_tag=method.delivery_tag)

    @staticmethod
    def process_donation_event(ch, method, properties, body):
        try:
            start_time = datetime.now()
            donation_event = json.loads(body)
            print(f'Processing donation event at {start_time}: {donation_event}')
            match donation_event['type']:
                case 'charge.succeeded':
                    DonationEventProcessor.process_create_event(donation_event)
                    print(f'Donation create event id: {donation_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'charge.refunded':
                    DonationEventProcessor.process_refund_event(donation_event)
                    print(f'Donation refund event id: {donation_event['id']} processed successfully')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case _:
                    print(f'Unknown donation event: {donation_event['type']}')
        except Exception as e:
            error_time = datetime.now()
            print(f'Error in process_subscription_event at {error_time} due to {e}')
            if properties.headers.get('x-delivery-count') == 30:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(
                    f'ERROR PROCESSING DONATION EVENT at {error_time}:\n{body}\nERROR MESSAGE: {e}\nSTACK TRACE: {stack_trace}')
            ch.basic_nack(delivery_tag=method.delivery_tag)
