from donors.get_donor_events import get_donor_events


def test_get_donor_events_works():
    events = get_donor_events()
    assert events is not None
