from events.event_service import EventService


def test_retrieving_events_works():
    events = EventService.get_events()
    assert events is not None

def test_subscription_event_works():
    pass
