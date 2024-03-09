from donors.process_customer_event import process_customer_event


def test_process_customer_event():
    events = [{"event_type": 'customer.created'}]
    success = process_customer_event(events)
    assert success is True

