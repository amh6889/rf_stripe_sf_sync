import json

from subscriptions.subscription import Subscription


def test_subscription_does_not_exist():
    sub_id = '99999'
    sub = Subscription.get_salesforce_recurring_donation_by_stripe_id(sub_id)
    assert sub is None


def test_subscription_exists():
    sub_id = '12345'
    sub = Subscription.get_salesforce_recurring_donation_by_stripe_id(sub_id)
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


def test_get_payment_method_through_default_pm_works():
    subscription_id = 'sub_1OxWHkL1MLd6bigCBIbCyVnC'
    subscription = Subscription.get_stripe_payment_method(subscription_id)
    assert subscription is not None
    assert subscription['card']['last4'] == '4242'


def test_get_payment_method_through_invoice_works():
    subscription_id = 'sub_1OuRZCL1MLd6bigCf9ifDf0R'
    subscription = Subscription.get_stripe_payment_method(subscription_id)
    payment_method_type = subscription['type']
    assert subscription is not None
    assert subscription[payment_method_type]['last4'] == '4242'


def test_get_campaign_id_works_with_general_campaign():
    campaign_code = 'F000 - General'
    campaign_id = Subscription.get_campaign_id(campaign_code)
    assert campaign_id is not None
    assert campaign_id == '7015a000001SjmyAAC'


def test_get_campaign_id_works_with_non_general_campaign():
    campaign_code = 'C1022'
    campaign_id = Subscription.get_campaign_id(campaign_code)
    assert campaign_id is not None
    assert campaign_id == '7015a000001SpJnAAK'
