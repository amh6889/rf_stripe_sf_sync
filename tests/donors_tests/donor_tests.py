import json

from donors.donor import Donor
from donors.donor_processor import DonorProcessor


def test_donor_does_not_exist():
    email = 'sometestemail@gmail.com'
    exists = Donor.exists_by_email(email)
    assert exists is None


def test_donor_exist():
    email = 'do_test@gmail.com'
    donor = Donor.exists_by_email(email)
    assert donor is not None


def test_create_donor_succeeds():
    donor = {'FirstName': 'Melinda', 'LastName': 'Trump', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail9998@gmail.com',
             'Email': 'testemail9998@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True,
             "MailingStreet": "5668 Lilac Blossom Lane", "MailingCity": "San Jose", "MailingState": "CA",
             "MailingCountry": "United States",
             "MailingPostalCode": "95124"}
    response = Donor.create(**donor)
    assert response.get('success') is True


def test_create_donor_errors():
    donor = {'FirstName': 'Melinda', 'LastName': 'Trump', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail9999@gmail.com',
             'Email': 'testemail9999@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True,
             "MailingStreet": "5668 Lilac Blossom Lane", "MailingCity": "San Jose", "MailingState": "CA",
             "MailingCountry": "United States",
             "MailingPostalCode": "95124"}
    response = Donor.create(**donor)
    assert response.get('success') is False


def test_update_donor_succeeds():
    donor = {'FirstName': 'Ted', 'LastName': 'Turner', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail99@gmail.com',
             'Email': 'testemail99@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
    sf_contact_id = '003Ox00000Acq6HIAR'
    response = Donor.update(sf_contact_id, **donor)
    assert response is 204


def test_update_donor_errors():
    donor = {'FirstName': 'Ted', 'LastName': 'Turner', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail99@gmail.com',
             'Email': 'testemail99@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
    sf_contact_id = '003Ox00000Acq6HIAX'
    response = Donor.update(sf_contact_id, **donor)
    print(response)
    assert response is not 204


def test_donor_processor_maps_works_with_donor_address(donor_with_address_json):
    donor = json.loads(donor_with_address_json)
    mapped_donor = DonorProcessor._map_donor(**donor)
    assert mapped_donor['FirstName'] == 'Ted'
    assert mapped_donor['LastName'] == 'Hunt Mendoza'
    assert mapped_donor['npe01__HomeEmail__c'] == 'testemail99@gmail.com'
    assert mapped_donor['Email'] == 'testemail99@gmail.com'
    assert mapped_donor['MailingStreet'] == '406 Stonemill Dr Apt I'
    assert mapped_donor['MailingCity'] == 'Lynchburg'
    assert mapped_donor['MailingState'] == 'VA'
    assert mapped_donor['MailingPostalCode'] == '24502'
    assert mapped_donor['MailingCountry'] == 'US'
    assert mapped_donor['Phone'] == '+14347280720'
    assert mapped_donor['npe01__Preferred_Email__c'] == 'Personal'
    assert mapped_donor['External_Contact_ID__c'] == 'cus_PcdyPDFvTFM1gP'


def test_donor_processor_maps_works_with_donor_metadata_address(donor_with_metadata_address_json):
    donor = json.loads(donor_with_metadata_address_json)
    mapped_donor = DonorProcessor._map_donor(**donor)
    assert mapped_donor['FirstName'] == 'Turd'
    assert mapped_donor['LastName'] == 'Ferguson'
    assert mapped_donor['npe01__HomeEmail__c'] == 'turdfergusion_test@gmail.com'
    assert mapped_donor['Email'] == 'turdfergusion_test@gmail.com'
    assert mapped_donor['MailingStreet'] == '4554 Thomas Jefferson Rd'
    assert mapped_donor['MailingCity'] == 'Forest'
    assert mapped_donor['MailingState'] == 'VA'
    assert mapped_donor['MailingPostalCode'] == '24551'
    assert mapped_donor['MailingCountry'] == 'United States'
    assert mapped_donor['Phone'] is None
    assert mapped_donor['npe01__Preferred_Email__c'] == 'Personal'
    assert mapped_donor['External_Contact_ID__c'] == 'cus_Q4X90EUjCmX1wg'


def test_donor_processor_maps_works_with_no_donor_metadata_address(donor_with_no_metadata_address_json):
    donor = json.loads(donor_with_no_metadata_address_json)
    mapped_donor = DonorProcessor._map_donor(**donor)
    assert mapped_donor['FirstName'] == 'Turd'
    assert mapped_donor['LastName'] == 'Ferguson'
    assert mapped_donor['npe01__HomeEmail__c'] == 'turdfergusion_test@gmail.com'
    assert mapped_donor['Email'] == 'turdfergusion_test@gmail.com'
    assert mapped_donor['MailingStreet'] is None
    assert mapped_donor['MailingCity'] is None
    assert mapped_donor['MailingState'] is None
    assert mapped_donor['MailingPostalCode'] is None
    assert mapped_donor['MailingCountry'] is None
    assert mapped_donor['Phone'] is None
    assert mapped_donor['npe01__Preferred_Email__c'] == 'Personal'
    assert mapped_donor['External_Contact_ID__c'] == 'cus_Q4X90EUjCmX1wg'


def test_donor_processor_maps_works_with_donor_metadata_name(donor_with_metadata_name):
    donor = json.loads(donor_with_metadata_name)
    mapped_donor = DonorProcessor._map_donor(**donor)
    assert mapped_donor['FirstName'] == 'Allan'
    assert mapped_donor['LastName'] == 'Sanchez'
    assert mapped_donor['npe01__HomeEmail__c'] == 'allansr20@gmail.com'
    assert mapped_donor['Email'] == 'allansr20@gmail.com'
    assert mapped_donor['MailingStreet'] == 'Av. 0AS, Calle 42'
    assert mapped_donor['MailingCity'] == 'Alajuela'
    assert mapped_donor['MailingState'] == 'Alajuela'
    assert mapped_donor['MailingPostalCode'] == '20102'
    assert mapped_donor['MailingCountry'] == 'Costa Rica'
    assert mapped_donor['Phone'] is None
    assert mapped_donor['npe01__Preferred_Email__c'] == 'Personal'
    assert mapped_donor['External_Contact_ID__c'] == 'cus_QToxMZVIxZRAtF'


def test_donor_processor_maps_works_with_donor_metadata_opt_out(donor_with_metadata_opt_out):
    donor = json.loads(donor_with_metadata_opt_out)
    mapped_donor = DonorProcessor._map_donor_create_event(**donor)
    assert mapped_donor['FirstName'] == 'Bill'
    assert mapped_donor['LastName'] == 'Nye'
    assert mapped_donor['npe01__HomeEmail__c'] == 'bill_nye_test@gmail.com'
    assert mapped_donor['Email'] == 'bill_nye_test@gmail.com'
    assert mapped_donor['MailingStreet'] == '901 Alum Springs Rd'
    assert mapped_donor['MailingCity'] == 'Forest'
    assert mapped_donor['MailingState'] == 'VA'
    assert mapped_donor['MailingPostalCode'] == '24551'
    assert mapped_donor['MailingCountry'] is None
    assert mapped_donor['Phone'] is None
    assert mapped_donor['npe01__Preferred_Email__c'] == 'Personal'
    assert mapped_donor['External_Contact_ID__c'] == 'cus_QUl5PhyHKkQnDC'
    assert mapped_donor['HasOptedOutOfEmail'] is True
    assert mapped_donor['DoNotMail__c'] is True

def test_donor_processor_maps_works_with_donor_create_event_metadata_receipt_email_mail(donor_with_metadata_receipt):
    donor = json.loads(donor_with_metadata_receipt)
    mapped_donor = DonorProcessor._map_donor_create_event(**donor)
    assert mapped_donor['FirstName'] == 'Bill'
    assert mapped_donor['LastName'] == 'Nye'
    assert mapped_donor['npe01__HomeEmail__c'] == 'bill_nye_test@gmail.com'
    assert mapped_donor['Email'] == 'bill_nye_test@gmail.com'
    assert mapped_donor['MailingStreet'] == '901 Alum Springs Rd'
    assert mapped_donor['MailingCity'] == 'Forest'
    assert mapped_donor['MailingState'] == 'VA'
    assert mapped_donor['MailingPostalCode'] == '24551'
    assert mapped_donor['MailingCountry'] is None
    assert mapped_donor['Phone'] is None
    assert mapped_donor['npe01__Preferred_Email__c'] == 'Personal'
    assert mapped_donor['External_Contact_ID__c'] == 'cus_QUl5PhyHKkQnDC'
    assert mapped_donor['HasOptedOutOfEmail'] is False
    assert mapped_donor['DoNotMail__c'] is False
    assert mapped_donor['ReceiptDelivery__c'] == 'Email + Mail'


def test_parse_name_two_names_works():
    full_name = 'Billy Bob'
    first_name, last_name = DonorProcessor._parse_name(full_name)
    print(first_name)
    assert first_name == 'Billy'
    assert last_name == 'Bob'


def test_parse_name_three_names_works():
    full_name = 'Billy Bob Thumb'
    first_name, last_name = DonorProcessor._parse_name(full_name)
    assert first_name == 'Billy'
    assert last_name == 'Bob Thumb'


def test_parse_name_four_names_works():
    full_name = 'Wing Pong Robert Luk'
    first_name, last_name = DonorProcessor._parse_name(full_name)
    assert first_name == 'Wing'
    assert last_name == 'Pong Robert Luk'


def test_get_email_works():
    stripe_customer_id = 'cus_PjBU4vGjx2wr3I'
    email = Donor.get_email(stripe_customer_id)
    assert email is not None
    assert email == 'thisisatestemailhomey@gmail.com'


def test_reserved_characters_email_does_not_exist():
    email = 'ade-^?|"\'rogers-wright@hotmail.co.uk'
    contact_id = Donor.exists_by_email(email)
    assert contact_id is None


def test_reserved_characters_email_exists():
    email = 'ade-rogers-wright@hotmail.co.uk'
    contact_id = Donor.exists_by_email(email)
    assert contact_id is not None
    assert contact_id == '0030b00002TWpQwAAL'


def test_stripe_update_customer():
    stripe_customer_id = 'cus_QQWGdqZVFJarM9'
    street_address = '1234 Cool Lane'
    city = 'San Jose'
    state = 'CA'
    zip_code = '95124'
    country = 'US'
    address = {'city': city}
    updates = {'address': address}
    response = Donor.update_stripe_customer(stripe_customer_id, updates)
    assert response is not None


def test_stripe_update_event(donor_with_address_line2_missing):
    donor_event = json.loads(donor_with_address_line2_missing)
    response = DonorProcessor.process_update_event(donor_event)
    assert response is not None
