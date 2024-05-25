import json

import mock

from subscriptions.subscription import Subscription
from subscriptions.subscription_processor import SubscriptionProcessor
from unittest.mock import Mock, MagicMock
from donors.donor import Donor
from unittest.mock import Mock


def test_subscription_does_not_exist():
    sub_id = '99999'
    sub = Subscription.exists(sub_id)
    assert sub is None


def test_subscription_exists():
    sub_id = '12345'
    sub = Subscription.exists(sub_id)
    assert sub is not None


def test_get_subscription_metadata_succeeds():
    metadata = Subscription.get_metadata()
    assert metadata is not None


def test_create_subscription_metadata_succeeds():
    metadata = Subscription.create_metadata()
    assert metadata is not None


def test_create_subscription_succeeds():
    subscription = {'Stripe_Subscription_ID__c': '1', 'npe03__Amount__c': '5',
                    'npe03__Date_Established__c': '2023-06-08',
                    'npsp__StartDate__c': '2023-06-08', 'npsp__EndDate__c': None,
                    'Donation_Source__c': 'RF Web-form',
                    'npsp__Status__c': 'Active', 'npsp__ClosedReason__c': None,
                    'npe03__Recurring_Donation_Campaign__c': None,
                    'npsp__RecurringType__c': 'Open', 'npe03__Installment_Period__c': 'Monthly',
                    'npsp__Day_of_Month__c': '17',
                    'npsp__InstallmentFrequency__c': '1', 'npsp__PaymentMethod__c': 'Credit Card',
                    'npe03__Installments__c': None, 'npe03__Contact__c': '0030b00002TWs3eAAD'}
    response = Subscription.create(**subscription)
    assert response.get('success') is True
    assert type(response) is dict


def test_create_subscription_errors():
    subscription = {'Stripe_Subscription_ID__c': '1', 'npe03__Amount__c': '5',
                    'npe03__Date_Established__c': '2023-06-08',
                    'npsp__StartDate__c': '2023-06-08', 'npsp__EndDate__c': None,
                    'Donation_Source__c': 'RF Web-form',
                    'npsp__Status__c': 'Active', 'npsp__ClosedReason__c': None,
                    'npe03__Recurring_Donation_Campaign__c': None,
                    'npsp__RecurringType__c': 'Open', 'npe03__Installment_Period__c': 'Monthly',
                    'npsp__Day_of_Month__c': '17',
                    'npsp__InstallmentFrequency__c': '1', 'npsp__PaymentMethod__c': 'Credit Card',
                    'npe03__Installments__c': None}
    response = Subscription.create(**subscription)
    assert response.get('success') is False
    assert type(response) is dict


def test_update_subscription_succeeds():
    subscription = {'Stripe_Subscription_ID__c': '1', 'npe03__Amount__c': '55',
                    'npe03__Date_Established__c': '2023-06-08',
                    'npsp__StartDate__c': '2023-09-08', 'npsp__EndDate__c': None,
                    'Donation_Source__c': 'RF Web-form',
                    'npsp__Status__c': 'Active', 'npsp__ClosedReason__c': None,
                    'npe03__Recurring_Donation_Campaign__c': None,
                    'npsp__RecurringType__c': 'Open', 'npe03__Installment_Period__c': 'Monthly',
                    'npsp__Day_of_Month__c': '17',
                    'npsp__InstallmentFrequency__c': '1', 'npsp__PaymentMethod__c': 'Credit Card',
                    'npe03__Installments__c': None}
    recurring_donation_id = 'a09Ox0000036AW1IAM'
    response = Subscription.update(recurring_donation_id, **subscription)
    assert response is 204


def test_update_subscription_errors():
    subscription = {'Stripe_Subscription_ID__c': '1', 'npe03__Amount__c': '55',
                    'npe03__Date_Established__c': '2023-06-08',
                    'npsp__StartDate__c': '2023-09-08', 'npsp__EndDate__c': None,
                    'Donation_Source__c': 'RF Web-form',
                    'npsp__Status__c': 'Active', 'npsp__ClosedReason__c': None,
                    'npe03__Recurring_Donation_Campaign__c': None,
                    'npsp__RecurringType__c': 'Open', 'npe03__Installment_Period__c': 'Monthly',
                    'npsp__Day_of_Month__c': '17',
                    'npsp__InstallmentFrequency__c': '1', 'npsp__PaymentMethod__c': 'Credit Card',
                    'npe03__Installments__c': None, 'npe03__Contact__c': '0030b00002TWs3eAAB'}
    recurring_donation_id = 'a09Ox0000036AW1IAM'
    response = Subscription.update(recurring_donation_id, **subscription)
    assert response is not 204


def test_map_open_incomplete_subscription_works(mocked_donor_id, open_active_subscription_json):
    subscription = json.loads(open_active_subscription_json)
    mapped_subscription = SubscriptionProcessor._map_active_subscription(**subscription)
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1PFUWGL1MLd6bigCFPlOUlAD'
    assert mapped_subscription['npe03__Amount__c'] == '555.00'
    assert mapped_subscription['npe03__Date_Established__c'] == '2024-05-12T05:00:20+00:00'
    assert mapped_subscription['npsp__StartDate__c'] == '2024-05-12T05:00:20+00:00'
    assert mapped_subscription['npsp__EndDate__c'] is None
    assert mapped_subscription['Donation_Source__c'] == 'RF Web-form'
    assert mapped_subscription['npsp__Status__c'] == 'Paused'
    assert mapped_subscription['npsp__ClosedReason__c'] is ''
    assert mapped_subscription['npe03__Recurring_Donation_Campaign__c'] is None
    assert mapped_subscription['npsp__RecurringType__c'] == 'Open'
    assert mapped_subscription['npe03__Installment_Period__c'] == 'Monthly'
    assert mapped_subscription['npsp__Day_of_Month__c'] == 12
    assert mapped_subscription['npsp__InstallmentFrequency__c'] == 1
    assert mapped_subscription['npsp__PaymentMethod__c'] == 'Credit Card'
    assert mapped_subscription['npe03__Installments__c'] is None
    assert mapped_subscription['npe03__Contact__c'] == '123456'

def test_map_open_canceled_subscription_works(mocked_sf_recurring_donation_id, canceled_subscription_json):
    subscription = json.loads(canceled_subscription_json)
    mapped_subscription = SubscriptionProcessor._map_canceled_subscription(**subscription)
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1P1hCDL1MLd6bigCTMM9YrD9'
    assert mapped_subscription['npsp__Status__c'] == 'Canceled'
    assert mapped_subscription['npsp__ClosedReason__c'] == 'Webform Canceled'


#TODO: need to fix the assertions below once we implement a stripe schedule with form assembly or custom UI
def test_map_fixed_active_subscription_works(mocked_donor_id, fixed_active_subscription_json):
    subscription = json.loads(fixed_active_subscription_json)
    mapped_subscription = SubscriptionProcessor._map_active_subscription(**subscription)
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1OxZRmL1MLd6bigCGpI8nX8p'
    assert mapped_subscription['npe03__Amount__c'] == '100.00'
    assert mapped_subscription['npe03__Date_Established__c'] == '2024-03-23T18:37:38+00:00'
    assert mapped_subscription['npsp__StartDate__c'] == '2024-03-23T18:37:38+00:00'
    assert mapped_subscription['npsp__EndDate__c'] is None
    assert mapped_subscription['Donation_Source__c'] == 'RF Web-form'
    assert mapped_subscription['npsp__Status__c'] == 'Canceled'
    assert mapped_subscription['npsp__ClosedReason__c'] == 'Webform Canceled'
    assert mapped_subscription['npe03__Recurring_Donation_Campaign__c'] is None
    assert mapped_subscription['npsp__RecurringType__c'] == 'Open'
    assert mapped_subscription['npe03__Installment_Period__c'] == 'Monthly'
    assert mapped_subscription['npsp__Day_of_Month__c'] == 23
    assert mapped_subscription['npsp__InstallmentFrequency__c'] == 1
    assert mapped_subscription['npsp__PaymentMethod__c'] == 'Credit Card'
    assert mapped_subscription['npe03__Installments__c'] is None
    assert mapped_subscription['npe03__Contact__c'] == '123456'

#TODO: need to fix the assertions below once we implement a stripe schedule with form assembly or custom UI
def test_map_fixed_canceled_subscription_works(mocked_donor_id, fixed_canceled_subscription_json):
    subscription = json.loads(fixed_canceled_subscription_json)
    mapped_subscription = SubscriptionProcessor._map_canceled_subscription(**subscription)
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1OxZRmL1MLd6bigCGpI8nX8p'
    assert mapped_subscription['npe03__Amount__c'] == 100
    assert mapped_subscription['npe03__Date_Established__c'] == '2024-03-23T18:37:38+00:00'
    assert mapped_subscription['npsp__StartDate__c'] == '2024-03-23T18:37:38+00:00'
    assert mapped_subscription['npsp__EndDate__c'] is None
    assert mapped_subscription['Donation_Source__c'] == 'RF Web-form'
    assert mapped_subscription['npsp__Status__c'] == 'Canceled'
    assert mapped_subscription['npsp__ClosedReason__c'] == 'Webform Canceled'
    assert mapped_subscription['npe03__Recurring_Donation_Campaign__c'] is None
    assert mapped_subscription['npsp__RecurringType__c'] == 'Open'
    assert mapped_subscription['npe03__Installment_Period__c'] == 'Monthly'
    assert mapped_subscription['npsp__Day_of_Month__c'] == 23
    assert mapped_subscription['npsp__InstallmentFrequency__c'] == 1
    assert mapped_subscription['npsp__PaymentMethod__c'] == 'Credit Card'
    assert mapped_subscription['npe03__Installments__c'] is None
    assert mapped_subscription['npe03__Contact__c'] == '123456'


def test_parse_epoch_time_works():
    epoch_time = 1710473782
    date_time = SubscriptionProcessor._parse_epoch_time(epoch_time)
    assert date_time[1] == '2024-03-15T03:36:22+00:00'
    assert date_time[0] == 15


def test_get_payment_method_through_default_pm_works():
    subscription_id = 'sub_1OxWHkL1MLd6bigCBIbCyVnC'
    subscription = Subscription.get_payment_method(subscription_id)
    assert subscription is not None
    assert subscription['card']['last4'] == '4242'


def test_get_payment_method_through_invoice_works():
    subscription_id = 'sub_1OuRZCL1MLd6bigCf9ifDf0R'
    subscription = Subscription.get_payment_method(subscription_id)
    payment_method_type = subscription['type']
    assert subscription is not None
    assert subscription[payment_method_type]['last4'] == '4242'
