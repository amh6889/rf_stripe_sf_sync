#!/home/stripe/apps/stripe_env/bin/python
import os
import sys

import pika

from donors.donor_event_processor import DonorEventProcessor
from donors.donor_mapper import DonorMapper
from donors.salesforce_donor_service import SalesforceDonorService
from donors.stripe_donor_service import StripeDonorService
from event_processor.event_processor import EventProcessor

if __name__ == '__main__':
    try:
        donor_mapper = DonorMapper()
        stripe_donor = StripeDonorService()
        salesforce_donor = SalesforceDonorService()
        donor_event_processor = DonorEventProcessor(donor_mapper, stripe_donor, salesforce_donor)
        event_processor = EventProcessor()

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
