import json

import pytest
from mock.mock import MagicMock

from donors.donor_event_processor import DonorEventProcessor


def test_stripe_create_event_handles_salesforce_donor_that_already_exists(donor_with_metadata_address_dict):
    # arrange
    mocked_donor_mapper = MagicMock()
    mocked_donor_mapper.map_donor_create_event.return_value = {'FirstName': 'Bill', 'LastName': 'Nye',
                                                               'npe01__HomeEmail__c': 'bill_nye_test@gmail.com',
                                                               'Email': 'bill_nye_test@gmail.com',
                                                               'MailingStreet': '901 Alum Springs Rd',
                                                               'MailingCity': 'Forest',
                                                               'MailingState': 'VA', 'MailingPostalCode': '24551',
                                                               'MailingCountry': None, 'Phone': None,
                                                               'npe01__Preferred_Email__c': 'Personal',
                                                               'External_Contact_ID__c': '12345',
                                                               'HasOptedOutOfEmail': True, 'DoNotMail__c': True}
    mocked_stripe_donor_service = MagicMock()
    #mocked_stripe_donor_service.update.return_value = {'success': True}

    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_donor_service.get_contact_id.return_value = '12345'

    donor_event_processor = DonorEventProcessor(mocked_donor_mapper, mocked_stripe_donor_service,
                                                mocked_salesforce_donor_service)
    # act
    with pytest.raises(Exception, match='Stripe customer with email bill_nye_test@gmail.com already exists in Salesforce with ID 12345. Cannot process donor create event further.'):
        created_id = donor_event_processor.process_create_event(donor_with_metadata_address_dict)
        # assert
        assert created_id is not None
        assert created_id == '12345'

def test_stripe_create_event_works_when_salesforce_contact_does_not_exist(donor_with_metadata_address_dict):
    # arrange
    mocked_donor_mapper = MagicMock()
    mocked_donor_mapper.map_donor_create_event.return_value = {'FirstName': 'Bill', 'LastName': 'Nye',
                                                               'npe01__HomeEmail__c': 'bill_nye_test@gmail.com',
                                                               'Email': 'bill_nye_test@gmail.com',
                                                               'MailingStreet': '901 Alum Springs Rd',
                                                               'MailingCity': 'Forest',
                                                               'MailingState': 'VA', 'MailingPostalCode': '24551',
                                                               'MailingCountry': None, 'Phone': None,
                                                               'npe01__Preferred_Email__c': 'Personal',
                                                               'External_Contact_ID__c': '12345',
                                                               'HasOptedOutOfEmail': True, 'DoNotMail__c': True}
    mocked_stripe_donor_service = MagicMock()

    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_donor_service.get_contact_id.return_value = None
    mocked_salesforce_donor_service.create.return_value = {'errors': [], 'id': '003e0000003GuNXAA0', 'success': True}

    donor_event_processor = DonorEventProcessor(mocked_donor_mapper, mocked_stripe_donor_service,
                                                mocked_salesforce_donor_service)
    # act
    created_id = donor_event_processor.process_create_event(donor_with_metadata_address_dict)
    # assert
    assert created_id is not None
    assert created_id == '003e0000003GuNXAA0'


def test_stripe_update_event(donor_with_address_line2_missing):
    donor_event_processor = DonorEventProcessor()
    donor_event = json.loads(donor_with_address_line2_missing)
    response = donor_event_processor.process_update_event(donor_event)
    assert response is not None
