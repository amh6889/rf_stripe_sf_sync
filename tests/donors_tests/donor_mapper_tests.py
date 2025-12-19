import json

import pytest

from donors.donor_mapper import DonorMapper, get_first_and_last_name, filter_donor

@pytest.mark.unit
def test_parse_name_four_names_works():
    full_name = 'Wing Pong Robert Luk'
    first_name, last_name = get_first_and_last_name(full_name)
    assert first_name == 'Wing'
    assert last_name == 'Pong Robert Luk'

@pytest.mark.unit
def test_parse_name_three_names_works():
    full_name = 'Billy Bob Thumb'
    first_name, last_name = get_first_and_last_name(full_name)
    assert first_name == 'Billy'
    assert last_name == 'Bob Thumb'

@pytest.mark.unit
def test_parse_name_two_names_works():
    full_name = 'Billy Bob'
    first_name, last_name = get_first_and_last_name(full_name)
    print(first_name)
    assert first_name == 'Billy'
    assert last_name == 'Bob'

@pytest.mark.unit
def test_filter_donor_works():
    donor = {'FirstName': None, 'LastName': 'Turkey',
             'MailingStreet': '12345 Bob Villa Way',
             'MailingState': 'VA', 'MailingCity': None,
             'MailingCountry': None, 'MailingPostalCode': None}
    filtered_donor = filter_donor(donor)
    assert filtered_donor is not None
    assert filtered_donor.get('FirstName') is None
    assert filtered_donor.get('LastName') == 'Turkey'
    assert filtered_donor.get('MailingStreet') == '12345 Bob Villa Way'
    assert filtered_donor.get('MailingState') == 'VA'
    assert filtered_donor.get('MailingCity') is None
    assert filtered_donor.get('MailingCountry') is None
    assert filtered_donor.get('MailingPostalCode') is None

@pytest.mark.unit
def test_donor_processor_maps_works_with_donor_create_event_metadata_receipt_email_mail(donor_with_metadata_receipt):
    donor_mapper = DonorMapper()
    mapped_donor = donor_mapper.map_create_event(donor_with_metadata_receipt)
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
    assert mapped_donor['HasOptedOutOfEmail'] is False
    assert mapped_donor['DoNotMail__c'] is False
    assert mapped_donor['ReceiptDelivery__c'] == 'Email + Mail'

@pytest.mark.unit
def test_donor_processor_maps_works_with_donor_metadata_opt_out(donor_with_metadata_opt_out):
    #arrange
    donor_mapper = DonorMapper()
    #act
    mapped_donor = donor_mapper.map_create_event(donor_with_metadata_opt_out)
    #assert
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
    assert mapped_donor['HasOptedOutOfEmail'] is True
    assert mapped_donor['DoNotMail__c'] is True

@pytest.mark.unit
def test_donor_processor_maps_works_with_donor_metadata_name(donor_with_metadata_name):
    donor_mapper = DonorMapper()
    mapped_donor = donor_mapper.map_create_event(donor_with_metadata_name)
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

@pytest.mark.unit
def test_donor_processor_maps_works_with_no_donor_metadata_address(donor_with_no_metadata_address_dict):
    donor_mapper = DonorMapper()
    mapped_donor = donor_mapper.map_create_event(donor_with_no_metadata_address_dict)
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

@pytest.mark.unit
def test_donor_processor_maps_works_with_donor_metadata_address(donor_with_metadata_address_dict):
    donor_mapper = DonorMapper()
    mapped_donor = donor_mapper.map_create_event(donor_with_metadata_address_dict)
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

@pytest.mark.unit
def test_donor_processor_maps_works_with_donor_address(donor_with_address_dict):
    donor_mapper = DonorMapper()
    mapped_donor = donor_mapper.map_create_event(donor_with_address_dict)
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
