import json

from donations.donation import Donation
from donations.donation_event_processor import DonationEventProcessor


def test_donation_does_not_exist():
    invoice_id = '99999'
    donation_id = Donation.exists(invoice_id)
    assert donation_id is None


def test_donation_exists():
    invoice_id = '12345'
    donation_id = Donation.exists(invoice_id)
    assert donation_id is not None


def test_retrieving_stripe_subscription_id_from_payment_intent_works():
    invoice_id = 'in_1P2gUyL1MLd6bigC8TQkFBy2'
    subscription_id = Donation.get_stripe_subscription_id(invoice_id)
    assert subscription_id is not None


def test_create_donation_succeeds():
    invoice = {'Stripe_Invoice_ID__c': '12345', 'Amount': '5',
               'CloseDate': '2023-06-08',
               'StageName': 'Closed Won',
               'Donation_Source__c': 'RF Web-form',
               'Name': '$5 RF Web-form',
               'npe03__Recurring_Donation__c': None,
               'Stripe_Subscription_ID__c': None, 'Card_Last_4__c': '5555',
               'npsp__Primary_Contact__c': '0030b00002TWs3eAAD', 'npe01__Contact_Id_for_Role__c': '0030b00002TWs3eAAD'}
    response = Donation.create(**invoice)
    assert response.get('success') is True
    assert type(response) is dict


def test_create_donation_errors():
    invoice = {'Stripe_Invoice_ID__c': '12345', 'Amount': '5',
               'CloseDate': '2023-06-08',
               'StageName': 'Closed Won',
               'Donation_Source__c': 'RF Web-form',
               'Name': '$5 RF Web-form',
               'npe03__Recurring_Donation__c': None,
               'Stripe_Subscription_ID__c': None, 'Card_Last_4__c': '5555',
               'npsp__Day_of_Month__c': '17',
               'npsp__Primary_Contact__c': '0030b00002TWs3eAAD', 'npe01__Contact_Id_for_Role__c': '0030b00002TWs3eAAD'}
    response = Donation.create(**invoice)
    assert response.get('success') is False
    assert type(response) is dict


def test_update_donation_succeeds():
    invoice = {'Stripe_Invoice_ID__c': '12345', 'Amount': '55',
               'CloseDate': '2023-06-08',
               'StageName': 'Closed Won',
               'Donation_Source__c': 'RF Web-form',
               'Name': '$5 RF Web-form',
               'npe03__Recurring_Donation__c': None,
               'Stripe_Subscription_ID__c': '12345', 'Card_Last_4__c': '5555'
               }
    response = Donation.update('006Ox000008NqZCIA0', **invoice)
    assert response is 204


def test_map_closed_won_one_time_card_donation_succeeds(mocked_donor_email, mocked_donor_id,
                                                        successful_one_time_donation_json):
    invoice = json.loads(successful_one_time_donation_json)
    mapped_invoice = DonationEventProcessor._map_donation(**invoice)
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
    assert mapped_invoice['Stripe_Subscription_ID__c'] == None
    assert mapped_invoice['Amount'] == '444.00'


def test_map_closed_won_subscription_card_donation_succeeds(mocked_donor_email, mocked_stripe_subscription_id,
                                                            mocked_sf_recurring_donation_id,
                                                            mocked_donor_id, successful_subscription_donation_json):
    invoice = json.loads(successful_subscription_donation_json)
    mapped_invoice = DonationEventProcessor._map_donation(**invoice)
    assert mapped_invoice['Stripe_Invoice_ID__c'] == 'ch_3P2gUyL1MLd6bigC0mZJcaso'
    assert mapped_invoice['CloseDate'] == '2024-04-06T21:10:07+00:00'
    assert mapped_invoice['StageName'] == 'Closed Won'
    assert mapped_invoice['Name'] == '$999.00 RF Web-form'
    assert mapped_invoice['Donation_Source__c'] == 'RF Web-form'
    assert mapped_invoice['npe03__Recurring_Donation__c'] is '12345'
    assert mapped_invoice['Stripe_Subscription_ID__c'] is '123456'
    assert mapped_invoice['Card_Last_4__c'] == '4242'
    assert mapped_invoice['npsp__Primary_Contact__c'] == '12345'
    assert mapped_invoice['npe01__Contact_Id_for_Role__c'] == '12345'
    assert mapped_invoice['Stripe_Subscription_ID__c'] == '123456'
    assert mapped_invoice['Amount'] == '999.00'


def test_map_donation_refund_succeeds(refunded_donation_json):
    invoice = json.loads(refunded_donation_json)
    mapped_refund = DonationEventProcessor._map_refund(**invoice)
    assert mapped_refund['Id'] == '1111'
    assert mapped_refund['StageName'] == 'Withdrawn'
