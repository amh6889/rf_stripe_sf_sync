from donors.stripe_donor_service import StripeDonorService


def test_get_email_works_when_donor_does_not_exist():
    # arrange
    donor = StripeDonorService()
    # act
    exists = donor.get_donor_email('amh6889@gmail.com')
    # assert
    assert exists is False


def test_stripe_update_customer():
    # arrange
    donor = StripeDonorService()
    stripe_customer_id = 'cus_QQWGdqZVFJarM9'
    street_address = '1234 Cool Lane'
    city = 'San Jose'
    state = 'CA'
    zip_code = '95124'
    country = 'US'
    address = {'city': city}
    updates = {'address': address}
    # act
    response = donor.update(stripe_customer_id, updates)
    # assert
    assert response is not None


def test_get_email_works():
    # arrange
    donor = StripeDonorService()
    stripe_customer_id = 'cus_PjBU4vGjx2wr3I'
    # act
    email = donor.get_donor_email(stripe_customer_id)
    # assert
    assert email is not None
    assert email == 'thisisatestemailhomey@gmail.com'
