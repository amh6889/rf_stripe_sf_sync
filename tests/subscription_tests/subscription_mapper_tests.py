import json
from datetime import datetime, UTC

from subscriptions.subscription_mapper import SubscriptionMapper


# TODO: mock getting payment method data from Stripe for test
def test_map_open_incomplete_subscription_works(mocked_donor_id, open_active_subscription_json):
    subscription = json.loads(open_active_subscription_json)
    mapped_subscription = SubscriptionMapper.map_active_subscription(**subscription)
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


def test_map_open_canceled_subscription_works(canceled_subscription_json):
    subscription = json.loads(canceled_subscription_json)
    mapped_subscription = SubscriptionMapper.map_canceled_subscription(**subscription)
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1P1hCDL1MLd6bigCTMM9YrD9'
    assert mapped_subscription['npsp__Status__c'] == 'Canceled'
    assert mapped_subscription['npsp__ClosedReason__c'] == 'Webform Canceled'


# TODO: need to fix the assertions below once we implement a stripe schedule with form assembly or custom UI
def test_map_fixed_active_subscription_works(mocked_donor_id, fixed_active_subscription_json):
    subscription = json.loads(fixed_active_subscription_json)
    mapped_subscription = SubscriptionMapper.map_active_subscription(**subscription)
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


# TODO: need to fix the assertions below once we implement a stripe schedule with form assembly or custom UI
def test_map_fixed_canceled_subscription_works(fixed_canceled_subscription_json):
    subscription = json.loads(fixed_canceled_subscription_json)
    mapped_subscription = SubscriptionMapper.map_canceled_subscription(**subscription)
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


def test_get_start_date_works():
    epoch_time = 1710473782
    start_date = SubscriptionMapper._get_start_date(epoch_time)
    assert start_date == datetime(2024, 3, 15, 3, 36, 22, tzinfo=UTC)
    assert start_date.isoformat() == '2024-03-15T03:36:22+00:00'
    assert start_date.day == 15
