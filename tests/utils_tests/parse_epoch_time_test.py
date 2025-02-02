from donations.donation_event_service import DonationEventService


def test_parse_epoch_time():
    epoch_time = 123456
    normal_time = DonationEventService._parse_epoch_time(epoch_time)
    assert normal_time == ''
