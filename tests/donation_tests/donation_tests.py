from donations.donation import Donation


def test_donation_does_not_exist():
    invoice_id = '99999'
    donation_id = Donation.exists(invoice_id)
    assert donation_id is None


def test_donation_exists():
    invoice_id = '12345'
    donation_id = Donation.exists(invoice_id)
    assert donation_id is not None


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
    response = Donation.update('006Ox000008NqZCIA0',**invoice)
    assert response is 204


def test_map_donation_works():
    invoice = {'Stripe_Invoice_ID__c': '12345', 'Amount': '55',
               'CloseDate': '2023-06-08',
               'StageName': 'Closed Won',
               'Donation_Source__c': 'RF Web-form',
               'Name': '$5 RF Web-form',
               'npe03__Recurring_Donation__c': None,
               'Stripe_Subscription_ID__c': '12345', 'Card_Last_4__c': '5555'
               }
    response = DonationProcessor._map_donation(invoice)
