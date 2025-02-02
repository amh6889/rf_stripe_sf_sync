#!/home/stripe/apps/stripe_env/bin/python
import os
import sys

import pika

from donations.donation_event_service import DonationEventService
from donations.donation_mapper import DonationMapper
from donations.donation_salesforce_service import SalesforceDonationService
from donations.donation_stripe_service import StripeDonationService
from donors.donor_event_service import DonorEventService
from donors.donor_mapper import DonorMapper
from donors.donor_salesforce_service import SalesforceDonorService
from donors.donor_stripe_service import StripeDonorService
from events.event_service import EventService
from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService
from subscriptions.subscription_stripe_service import StripeSubscriptionService
from subscriptions.subscription_event_service import SubscriptionEventService
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
        donor_event_service = DonorEventService(donor_mapper=donor_mapper,
                                                stripe_donor=stripe_donor_service,
                                                salesforce_donor=salesforce_donor_service)

        # instantiate subscription services
        salesforce_subscription_service = SalesforceSubscriptionService()
        stripe_subscription_service = StripeSubscriptionService(stripe_connection)
        subscription_mapper = SubscriptionMapper(stripe_subscription=stripe_subscription_service,
                                                 salesforce_subscription=salesforce_subscription_service,
                                                 stripe_donor=stripe_donor_service,
                                                 salesforce_donor=salesforce_donor_service)
        subscription_event_service = SubscriptionEventService(mapper=subscription_mapper,
                                                              salesforce_subscription=
                                                              salesforce_subscription_service)

        # instantiate donation services
        salesforce_donation_service = SalesforceDonationService()
        stripe_donation_service = StripeDonationService(stripe_connection)
        donation_mapper = DonationMapper(salesforce_subscription=salesforce_subscription_service,
                                         salesforce_donor=salesforce_donor_service,
                                         stripe_donor=stripe_donor_service,
                                         stripe_donation=stripe_donation_service)
        donation_event_service = DonationEventService(donation_mapper=donation_mapper,
                                                      salesforce_donation=salesforce_donation_service)

        event_processor = EventService(donation_event_service=donation_event_service,
                                       subscription_event_service=subscription_event_service,
                                       donor_event_service=donor_event_service)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # channel.queue_declare(queue='stripe_donor_q', durable=True)
        # channel.queue_declare(queue='stripe_donations_q', durable=True)
        # channel.queue_declare(queue='stripe_subscriptions_q', durable=True)

        channel.basic_consume(queue='stripe_donor_q', on_message_callback=event_processor.process_donor_event,
                              auto_ack=False)
        channel.basic_consume(queue='stripe_donations_q', on_message_callback=event_processor.process_donation_event,
                              auto_ack=False)
        channel.basic_consume(queue='stripe_subscriptions_q',
                              on_message_callback=event_processor.process_subscription_event,
                              auto_ack=False)
        channel.basic_consume(queue='dead_letter_q',
                              on_message_callback=event_processor.process_dead_letter_messages,
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
