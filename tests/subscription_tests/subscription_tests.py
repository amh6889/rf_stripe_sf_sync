from subscriptions.subscription_processor import SubscriptionProcessor


def test_subscription_does_not_exist():
    sub_id = '99999'
    sub = SubscriptionProcessor.subscription_exists(sub_id)
    assert sub is None


def test_subscription_exists():
    sub_id = '12345'
    sub = SubscriptionProcessor.subscription_exists(sub_id)
    assert sub is not None


def test_get_subscription_metadata_succeeds():
    metadata = SubscriptionProcessor.get_metadata()
    assert metadata is not None


def test_create_subscription_metadata_succeeds():
    metadata = SubscriptionProcessor.create_metadata()
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
    response = SubscriptionProcessor.create_subscription(**subscription)
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
    response = SubscriptionProcessor.create_subscription(**subscription)
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
    response = SubscriptionProcessor.update_subscription(recurring_donation_id, **subscription)
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
    response = SubscriptionProcessor.update_subscription(recurring_donation_id, **subscription)
    assert response is not 204
