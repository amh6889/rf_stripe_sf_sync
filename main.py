#!/home/stripe/apps/stripe_env/bin/python
import os
import sys

import pika

from donations.donation_event_processor import DonationEventProcessor
from donations.donation_mapper import DonationMapper
from donations.salesforce_donation_service import SalesforceDonationService
from donations.stripe_donation_service import StripeDonationService
from donors.donor_event_processor import DonorEventProcessor
from donors.donor_mapper import DonorMapper
from donors.salesforce_donor_service import SalesforceDonorService
from donors.stripe_donor_service import StripeDonorService
from event_processor.event_processor import EventProcessor
from subscriptions.salesforce_subscription_service import SalesforceSubscriptionService
from subscriptions.stripe_subscription_service import StripeSubscriptionService
from subscriptions.subscription_event_processor import SubscriptionEventProcessor
from subscriptions.subscription_mapper import SubscriptionMapper
from utils.stripe_connection import StripeConnection

# TODO: finish creating all objects for application and injecting them into appropriate classes
if __name__ == '__main__':
    try:
        stripe_connection = StripeConnection()

        # instantiate donor services
        salesforce_donor_service = SalesforceDonorService()
        stripe_donor_service = StripeDonorService(stripe_connection)
        donor_mapper = DonorMapper()
        donor_event_processor = DonorEventProcessor(donor_mapper=donor_mapper,
                                                    stripe_donor=stripe_donor_service,
                                                    salesforce_donor=salesforce_donor_service)

        # instantiate subscription services
        salesforce_subscription_service = SalesforceSubscriptionService()
        stripe_subscription_service = StripeSubscriptionService(stripe_connection)
        subscription_mapper = SubscriptionMapper(stripe_subscription=stripe_subscription_service,
                                                 salesforce_subscription=salesforce_subscription_service,
                                                 stripe_donor=stripe_donor_service,
                                                 salesforce_donor=salesforce_donor_service)
        subscription_event_processor = SubscriptionEventProcessor(mapper=subscription_mapper,
                                                                  salesforce_subscription=
                                                                  salesforce_subscription_service)

        # instantiate donation services
        salesforce_donation_service = SalesforceDonationService()
        stripe_donation_service = StripeDonationService(stripe_connection)
        donation_mapper = DonationMapper(salesforce_subscription=salesforce_subscription_service,
                                         salesforce_donor=salesforce_donor_service,
                                         stripe_donor=stripe_donor_service,
                                         stripe_donation=stripe_donation_service)
        donation_event_processor = DonationEventProcessor(donation_mapper=donation_mapper,
                                                          salesforce_donation=salesforce_donation_service)

        event_processor = EventProcessor(donation_event_processor=donation_event_processor,
                                         subscription_event_processor=subscription_event_processor,
                                         donor_event_processor=donor_event_processor)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # channel.queue_declare(queue='stripe_donor_q', durable=True)
        # channel.queue_declare(queue='stripe_donations_q', durable=True)
        # channel.queue_declare(queue='stripe_subscriptions_q', durable=True)

        channel.basic_consume(queue='stripe_donor_q', on_message_callback=EventProcessor.process_donor_event,
                              auto_ack=False)
        channel.basic_consume(queue='stripe_donations_q', on_message_callback=EventProcessor.process_donation_event,
                              auto_ack=False)
        channel.basic_consume(queue='stripe_subscriptions_q',
                              on_message_callback=EventProcessor.process_subscription_event,
                              auto_ack=False)
        channel.basic_consume(queue='dead_letter_q',
                              on_message_callback=EventProcessor.process_dead_letter_messages,
                              auto_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as error:
        print(error)
        channel.close()
        connection.close()
