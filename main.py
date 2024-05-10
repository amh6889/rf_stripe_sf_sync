import os
import sys

import pika

from event_processor.event_processor import EventProcessor


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='stripe_donor_q', durable=True)
    channel.queue_declare(queue='stripe_donations_q', durable=True)
    channel.queue_declare(queue='stripe_subscriptions_q', durable=True)

    channel.basic_consume(queue='stripe_donor_q', on_message_callback=EventProcessor.process_donor_event,
                          auto_ack=False)
    channel.basic_consume(queue='stripe_donations_q', on_message_callback=EventProcessor.process_donation_event,
                          auto_ack=False)
    channel.basic_consume(queue='stripe_subscriptions_q', on_message_callback=EventProcessor.process_subscription_event,
                          auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
