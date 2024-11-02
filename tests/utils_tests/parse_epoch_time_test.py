from donations.donation_processor import DonationProcessor


def test_parse_epoch_time():
    epoch_time = 123456
    normal_time = DonationProcessor._parse_epoch_time(epoch_time)
    assert normal_time == ''
