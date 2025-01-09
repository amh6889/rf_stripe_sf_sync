import json


from donors.donor_event_processor import DonorEventProcessor


def test_stripe_create_event(donor_with_no_metadata_address_json, mocked_donor_mapper, mocked_stripe_donor_service, mocked_salesforce_donor_service):
    donor_event_processor = DonorEventProcessor(mocked_donor_mapper, mocked_stripe_donor_service,
                                                mocked_salesforce_donor_service)
    donor_event = json.loads(donor_with_no_metadata_address_json)
    response = donor_event_processor.process_create_event(donor_event)
    assert response is not None


def test_stripe_update_event(donor_with_address_line2_missing):
    donor_event_processor = DonorEventProcessor()
    donor_event = json.loads(donor_with_address_line2_missing)
    response = donor_event_processor.process_update_event(donor_event)
    assert response is not None
