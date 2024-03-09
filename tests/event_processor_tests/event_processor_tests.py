


def getting_customer_events_works():
    event_type = 'customer_event'
    customer_events = EventProcessor.get_events(event_type)