import json
from datetime import datetime, UTC

import pytest
from mock.mock import MagicMock

from donors.salesforce_donor_service import SalesforceDonorService
from donors.stripe_donor_service import StripeDonorService
from subscriptions.salesforce_subscription_service import SalesforceSubscriptionService
from subscriptions.stripe_subscription_service import StripeSubscriptionService
from subscriptions.subscription_mapper import SubscriptionMapper, get_start_date
from utils.stripe_connection import StripeConnection


def test_map_subscription_with_subscription_schedule_is_correct():
    pass


# TODO: mock getting payment method data from Stripe for test
@pytest.mark.unit
def test_map_open_active_subscription_works_with_create_event(open_active_subscription_dict):
    # arrange
    mocked_stripe_donation_service = MagicMock()
    mocked_stripe_donation_service.get_stripe_subscription_by_invoice_id.return_value = None

    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_donor_service.get_contact_id.return_value = '123456'

    mocked_salesforce_subscription_service = MagicMock()
    mocked_salesforce_subscription_service.get_by_stripe_id.return_value = None
    mocked_salesforce_subscription_service.get_campaign_id.return_value = '12345'

    mocked_stripe_subscription_service = MagicMock()
    mocked_stripe_subscription_service.get_by_stripe_id.return_value = None
    mocked_stripe_subscription_service.get_stripe_payment_method.return_value = {'type': 'card'}

    mocked_stripe_donor_service = MagicMock()
    mocked_stripe_donor_service.get_donor_email.return_value = "test_email@gmail.com"

    subscription_mapper = SubscriptionMapper(stripe_subscription=mocked_stripe_subscription_service,
                                             salesforce_subscription=mocked_salesforce_subscription_service,
                                             stripe_donor=mocked_stripe_donor_service,
                                             salesforce_donor=mocked_salesforce_donor_service)

    # act
    mapped_subscription = subscription_mapper.map_create_event(**open_active_subscription_dict)
    # assert
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1PFUWGL1MLd6bigCFPlOUlAD'
    assert mapped_subscription['npe03__Amount__c'] == '555.00'
    assert mapped_subscription['npe03__Date_Established__c'] == '2024-05-12T05:00:20+00:00'
    assert mapped_subscription['npsp__StartDate__c'] == '2024-05-12T05:00:20+00:00'
    assert mapped_subscription['Donation_Source__c'] == 'RF Web-form'
    assert mapped_subscription['npsp__Status__c'] == 'Paused'
    assert mapped_subscription['npsp__ClosedReason__c'] is None
    assert mapped_subscription['npe03__Recurring_Donation_Campaign__c'] == '12345'
    assert mapped_subscription['npsp__RecurringType__c'] == 'Open'
    assert mapped_subscription['npe03__Installment_Period__c'] == 'Monthly'
    assert mapped_subscription['npsp__Day_of_Month__c'] == 12
    assert mapped_subscription['npsp__InstallmentFrequency__c'] == 1
    assert mapped_subscription['npsp__PaymentMethod__c'] == 'Credit Card'
    assert mapped_subscription['npe03__Contact__c'] == '123456'

@pytest.mark.unit
def test_map_open_canceled_subscription_works_with_delete_event(canceled_subscription_dict):
    # arrange
    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_subscription_service = MagicMock()
    mocked_stripe_subscription_service = MagicMock()
    mocked_stripe_donor_service = MagicMock()

    subscription_mapper = SubscriptionMapper(stripe_subscription=mocked_stripe_subscription_service,
                                             salesforce_subscription=mocked_salesforce_subscription_service,
                                             stripe_donor=mocked_stripe_donor_service,
                                             salesforce_donor=mocked_salesforce_donor_service)
    # act
    mapped_subscription = subscription_mapper.map_delete_event(**canceled_subscription_dict)

    # assert
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1P1hCDL1MLd6bigCTMM9YrD9'
    assert mapped_subscription['npsp__Status__c'] == 'Canceled'
    assert mapped_subscription['npsp__ClosedReason__c'] == 'Webform Canceled'


@pytest.mark.unit
def test_unit_map_imported_anet_subscription_works_with_create_event(fixed_active_subscription_dict, mocked_subscription_schedule):
    # arrange
    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_subscription_service = MagicMock()
    mocked_stripe_subscription_service = MagicMock()
    mocked_stripe_subscription_service.get_subscription_schedule.return_value = mocked_subscription_schedule
    mocked_stripe_donor_service = MagicMock()

    subscription_mapper = SubscriptionMapper(stripe_subscription=mocked_stripe_subscription_service,
                                             salesforce_subscription=mocked_salesforce_subscription_service,
                                             stripe_donor=mocked_stripe_donor_service,
                                             salesforce_donor=mocked_salesforce_donor_service)
    # act
    mapped_subscription = subscription_mapper.map_create_event(**fixed_active_subscription_dict)
    # assert
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1QjZZiL1MLd6bigC1zMiPpEz'
    assert mapped_subscription['ANET_ARB_ID__c'] == '65804855'


@pytest.mark.integration
def test_integration_map_imported_anet_subscription_works(fixed_active_subscription_dict, mocked_subscription_schedule):
    # arrange
    stripe_connection = StripeConnection()
    stripe_subscription_service = StripeSubscriptionService(stripe_connection)
    salesforce_subscription_service = SalesforceSubscriptionService()
    stripe_donor_service = StripeDonorService(stripe_connection)
    salesforce_donor_service = SalesforceDonorService()

    subscription_mapper = SubscriptionMapper(stripe_subscription=stripe_subscription_service,
                                             salesforce_subscription=salesforce_subscription_service,
                                             stripe_donor=stripe_donor_service,
                                             salesforce_donor=salesforce_donor_service)
    # act
    mapped_subscription = subscription_mapper.map_create_event(**fixed_active_subscription_dict)
    # assert
    assert mapped_subscription['Stripe_Subscription_ID__c'] == 'sub_1QjZZiL1MLd6bigC1zMiPpEz'
    assert mapped_subscription['ANET_ARB_ID__c'] == '65804855'


def test_get_start_date_works():
    data = {'created': 1710473782}
    start_date = get_start_date(data)
    assert start_date == datetime(2024, 3, 15, 3, 36, 22, tzinfo=UTC)
    assert start_date.isoformat() == '2024-03-15T03:36:22+00:00'
    assert start_date.day == 15
