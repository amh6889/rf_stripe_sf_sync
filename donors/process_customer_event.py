
def process_customer_event(donor_events):
    for donor_event in donor_events:
        if donor_event['event_type'] == 'customer.created':
            process_customer_event(donor_event)
            return True
        else:
            return False
