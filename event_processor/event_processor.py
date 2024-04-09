from donors.donor_processor import DonorProcessor
import utils.database_connection


class EventProcessor:

    @staticmethod
    def get_events():
        query = (
            "select * from stripe.stripe_event where is_synced = 'N' order by FIELD(EVENT_TYPE, 'customer.created','payment_intent.created','charge.succeeded','payment_intent.succeeded'),activity_date desc")
        events = []
        with utils.database_connection.db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            for row in cursor:
                print(row)
                events.append(row)
        print(events)
        return events

    @staticmethod
    def process_events(events):
        for event in events:
            event_type = event["event_type"]
            event_data = event["event_data"]
            match event_type:
                case "customer.created":
                    DonorProcessor.process_create_event(event_data)
                case "customer.updated":
                    DonorProcessor.process_update_event(event_data)
                case _:
                    print("Unknown event type")
