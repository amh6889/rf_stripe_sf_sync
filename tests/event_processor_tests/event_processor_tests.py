from event_processor.event_processor import EventProcessor


def test_retrieving_events_works():
    events = EventProcessor.get_events()
    assert events is not None


