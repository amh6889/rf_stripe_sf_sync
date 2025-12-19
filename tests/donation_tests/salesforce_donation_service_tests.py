import pytest

from donations.donation_salesforce_service import SalesforceDonationService


@pytest.mark.integration
def test_create_donation_succeeds():
    # arrange
    salesforce_donation_service = SalesforceDonationService()
    invoice = {'Stripe_Invoice_ID__c': '12345', 'Amount': '5',
               'CloseDate': '2023-06-08',
               'StageName': 'Closed Won',
               'Donation_Source__c': 'RF Web-form',
               'Name': '$5 RF Web-form',
               'npe03__Recurring_Donation__c': None,
               'Stripe_Subscription_ID__c': None, 'Card_Last_4__c': '5555',
               'npsp__Primary_Contact__c': '0030b00002TWs3eAAD', 'npe01__Contact_Id_for_Role__c': '0030b00002TWs3eAAD'}
    response = salesforce_donation_service.create(invoice)
    assert response.get('success') is True
    assert type(response) is dict


@pytest.mark.integration
def test_create_donation_errors():
    # arrange
    salesforce_donation_service = SalesforceDonationService()
    invoice = {'Stripe_Invoice_ID__c': '12345', 'Amount': '5',
               'CloseDate': '2023-06-08',
               'StageName': 'Closed Won',
               'Donation_Source__c': 'RF Web-form',
               'Name': '$5 RF Web-form',
               'npe03__Recurring_Donation__c': None,
               'Stripe_Subscription_ID__c': None, 'Card_Last_4__c': '5555',
               'npsp__Day_of_Month__c': '17',
               'npsp__Primary_Contact__c': '0030b00002TWs3eAAD', 'npe01__Contact_Id_for_Role__c': '0030b00002TWs3eAAD'}
    # act
    response = salesforce_donation_service.create(invoice)
    # assert
    assert response.get('success') is False
    assert type(response) is dict


@pytest.mark.integration
def test_update_donation_succeeds():
    # arrange
    salesforce_donation_service = SalesforceDonationService()
    invoice = {'Stripe_Invoice_ID__c': '12345', 'Amount': '55',
               'CloseDate': '2023-06-08',
               'StageName': 'Closed Won',
               'Donation_Source__c': 'RF Web-form',
               'Name': '$5 RF Web-form',
               'npe03__Recurring_Donation__c': None,
               'Stripe_Subscription_ID__c': '12345', 'Card_Last_4__c': '5555'
               }
    # act
    response = salesforce_donation_service.update('006Ox000008NqZCIA0', invoice)
    # assert
    assert response is 204


@pytest.mark.integration
def test_donation_does_not_exist():
    # arrange
    salesforce_donation_service = SalesforceDonationService()
    invoice_id = '99999'
    # act
    donation_id = salesforce_donation_service.exists(invoice_id)
    # assert
    assert donation_id is None


@pytest.mark.integration
def test_donation_exists():
    # arrange
    salesforce_donation_service = SalesforceDonationService()
    invoice_id = '12345'
    # act
    donation_id = salesforce_donation_service.exists(invoice_id)
    # assert
    assert donation_id is not None
