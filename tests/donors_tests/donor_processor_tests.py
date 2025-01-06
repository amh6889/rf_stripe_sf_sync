import json

from donors.donor import Donor
from donors.donor_event_processor import DonorEventProcessor


def test_stripe_create_event(donor_with_address_line2_missing):
    donor_event = json.loads(donor_with_address_line2_missing)
    response = DonorEventProcessor.process_create_event(donor_event)
    assert response is not None


def test_stripe_update_event(donor_with_address_line2_missing):
    donor_event = json.loads(donor_with_address_line2_missing)
    response = DonorEventProcessor.process_update_event(donor_event)
    assert response is not None
