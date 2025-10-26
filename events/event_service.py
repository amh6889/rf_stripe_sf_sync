import json
import traceback

from donations.donation_event_service import DonationEventService
from donors.donor_event_service import DonorEventService
from subscriptions.subscription_event_service import SubscriptionEventService
from utils import slack_notifier
from datetime import datetime


class EventService:
    def __init__(self, donation_event_service: DonationEventService, subscription_event_service: SubscriptionEventService,
                 donor_event_service: DonorEventService):
        self.donation_event_service = donation_event_service
        self.donor_event_service = donor_event_service
        self.subscription_event_service = subscription_event_service

    def process_dead_letter_messages(self, ch, method, properties, body):
        try:
            print(body)
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
                    self.donor_event_service.process_create_event(donor_event)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor create event id: {event_id}')
                case 'customer.updated':
                    print(f'Processing donor update event id: {event_id}')
                    self.donor_event_service.process_update_event(donor_event)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    print(f'Successfully processed donor update event id: {event_id}')
                case _:
                    print(f'Unknown donor event type: {event_type}')
        except Exception as e:
            error_time = datetime.now()
            print(f'Error in process_donor_event at {error_time} due to: {e}')
            if properties.headers.get('x-delivery-count') == 30:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(f"""
                ERROR PROCESSING DONATION {event_type.upper()} EVENT AT {error_time} due to: {e}
                STACK TRACE: 
                {stack_trace}
                EVENT CONTENT: 
                {donor_event}
                """)
            ch.basic_nack(delivery_tag=method.delivery_tag)


    def process_subscription_event(self, ch, method, properties, body):
        try:
            start_time = datetime.now()
            subscription_event = json.loads(body)
            print(f'Processing subscription event at {start_time}: {subscription_event}')
            event_id = subscription_event.get('id')
            event_type = subscription_event.get('type')
            match event_type:
                case 'customer.subscription.created':
                    print(f'Processing subscription create event id: {event_id}')
                    self.subscription_event_service.process_create_event(subscription_event)
                    print(f'Successfully processed subscription create event id: {event_id}')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'customer.subscription.updated':
                    print(f'Processing subscription update event id: {event_id}')
                    self.subscription_event_service.process_update_event(subscription_event)
                    print(f'Successfully processed subscription update event id: {event_id}')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'customer.subscription.deleted':
                    print(f'Processing subscription delete event id: {event_id}')
                    self.subscription_event_service.process_delete_event(subscription_event)
                    print(f'Successfully processed subscription delete event id: {event_id}')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case _:
                    print(f'Unknown subscription event: {event_type}')
        except Exception as e:
            error_time = datetime.now()
            print(f'Error in process_subscription_event at {error_time} due to {e}')
            if properties.headers.get('x-delivery-count') == 30:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(f"""
                ERROR PROCESSING SUBSCRIPTION {event_type.upper()} EVENT AT {error_time} due to: {e}
                STACK TRACE: 
                {stack_trace}
                EVENT CONTENT: 
                {subscription_event}
                """)
            ch.basic_nack(delivery_tag=method.delivery_tag)


    def process_donation_event(self, ch, method, properties, body):
        try:
            start_time = datetime.now()
            donation_event = json.loads(body)
            print(f'Processing donation event at {start_time}: {donation_event}')
            event_type = donation_event.get('type')
            event_id = donation_event.get('id')
            match event_type:
                case 'charge.succeeded':
                    print(f'Processing donation create event id: {event_id}')
                    self.donation_event_service.process_create_event(donation_event)
                    print(f'Successfully processed donation create event id: {event_id}')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case 'charge.refunded':
                    print(f'Processing donation refund event id: {event_id}')
                    self.donation_event_service.process_refund_event(donation_event)
                    print(f'Successfully processed donation refund event id: {event_id}')
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                case _:
                    print(f'Unknown donation event: {event_type}')
        except Exception as e:
            error_time = datetime.now()
            print(f'Error in process_subscription_event at {error_time} due to {e}')
            if properties.headers.get('x-delivery-count') == 30:
                stack_trace = traceback.format_exc()
                slack_notifier.send_message(f"""
                ERROR PROCESSING DONATION {event_type.upper()} EVENT AT {error_time} due to: {e}
                STACK TRACE: 
                {stack_trace}
                EVENT CONTENT: 
                {donation_event}
                """)
            ch.basic_nack(delivery_tag=method.delivery_tag)
