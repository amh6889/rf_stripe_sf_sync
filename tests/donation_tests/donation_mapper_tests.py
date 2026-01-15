import pytest
from mock.mock import MagicMock

from donations.donation_mapper import DonationMapper

@pytest.mark.unit
def test_map_closed_won_one_time_card_donation_succeeds(successful_one_time_donation_dict):
    # arrange
    mocked_stripe_donation_service = MagicMock()
    mocked_stripe_donation_service.get_stripe_subscription_by_invoice_id.return_value = None

    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_donor_service.get_contact_id.return_value = '123456'

    mocked_salesforce_subscription_service = MagicMock()
    mocked_salesforce_subscription_service.get_by_stripe_id.return_value = None

    mocked_stripe_donor_service = MagicMock()
    mocked_stripe_donor_service.get_donor_email.return_value = "test_email@gmail.com"

    donation_mapper = DonationMapper(mocked_salesforce_subscription_service, mocked_salesforce_donor_service, mocked_stripe_donation_service,
                                     mocked_stripe_donor_service)

    mapped_invoice = donation_mapper.map_donation(successful_one_time_donation_dict)
    assert mapped_invoice['Stripe_Invoice_ID__c'] == 'ch_3P2n9UL1MLd6bigC19aOqPGG'
    assert mapped_invoice['CloseDate'] == '2024-04-07T04:16:22+00:00'
    assert mapped_invoice['StageName'] == 'Closed Won'
    assert mapped_invoice['Name'] == '$444.00 RF Web-form'
    assert mapped_invoice['Donation_Source__c'] == 'RF Web-form'
    assert mapped_invoice['npe03__Recurring_Donation__c'] is None
    assert mapped_invoice['Stripe_Subscription_ID__c'] is None
    assert mapped_invoice['Card_Last_4__c'] == '4242'
    assert mapped_invoice['npsp__Primary_Contact__c'] == '123456'
    assert mapped_invoice['npe01__Contact_Id_for_Role__c'] == '123456'
    assert mapped_invoice['Stripe_Subscription_ID__c'] is None
    assert mapped_invoice['Amount'] == '444.00'

@pytest.mark.unit
def test_map_closed_won_subscription_card_donation_succeeds(successful_subscription_donation_dict):
    # arrange
    mocked_stripe_donation_service = MagicMock()
    mocked_stripe_donation_service.get_stripe_subscription_by_invoice_id.return_value = '1111'

    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_donor_service.get_contact_id.return_value = '12345'

    mocked_salesforce_subscription_service = MagicMock()
    mocked_salesforce_subscription_service.get_by_stripe_id.return_value = {'id': '99999', 'sf_contact_id': '12345'}

    mocked_stripe_donor_service = MagicMock()
    mocked_stripe_donor_service.get_donor_email.return_value = "test_email@gmail.com"

    donation_mapper = DonationMapper(mocked_salesforce_subscription_service, mocked_salesforce_donor_service,
                                     mocked_stripe_donor_service, mocked_stripe_donation_service)
    # act
    mapped_invoice = donation_mapper.map_donation(successful_subscription_donation_dict)
    # assert
    assert mapped_invoice['Stripe_Invoice_ID__c'] == 'ch_3P2gUyL1MLd6bigC0mZJcaso'
    assert mapped_invoice['CloseDate'] == '2024-04-06T21:10:07+00:00'
    assert mapped_invoice['StageName'] == 'Closed Won'
    assert mapped_invoice['Name'] == '$999.00 RF Web-form'
    assert mapped_invoice['Donation_Source__c'] == 'RF Web-form'
    assert mapped_invoice['npe03__Recurring_Donation__c'] == '99999'
    assert mapped_invoice['Card_Last_4__c'] == '4242'
    assert mapped_invoice['npsp__Primary_Contact__c'] == '12345'
    assert mapped_invoice['npe01__Contact_Id_for_Role__c'] == '12345'
    assert mapped_invoice['Stripe_Subscription_ID__c'] == '1111'
    assert mapped_invoice['Amount'] == '999.00'

@pytest.mark.unit
def test_map_donation_refund_succeeds():
    # arrange
    mocked_stripe_donation_service = MagicMock()
    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_subscription_service = MagicMock()
    mocked_stripe_donor_service = MagicMock()

    donation_mapper = DonationMapper(mocked_salesforce_subscription_service, mocked_salesforce_donor_service,
                                     mocked_stripe_donor_service, mocked_stripe_donation_service)

    stripe_invoice_id = '1111'
    mapped_refund = donation_mapper.map_refund(stripe_invoice_id)
    assert mapped_refund['Stripe_Invoice_ID__c'] == '1111'
    assert mapped_refund['StageName'] == 'Withdrawn'

@pytest.mark.integration
def test_map_donation_creation_suceeds_with_honoree_contact():
    #arrange

    # act
    donation_mapper = DonationMapper(None, None,)
