import json

import pytest
from mock.mock import MagicMock

from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService
from subscriptions.subscription_stripe_service import StripeSubscriptionService
from subscriptions.subscription_event_service import SubscriptionEventService
from subscriptions.subscription_mapper import SubscriptionMapper
from utils.stripe_connection import StripeConnection


@pytest.mark.unit
def test_subscription_error_8_18_24(subscription_error_8_18_24):
    event_data = json.loads(subscription_error_8_18_24)
    subscription = SubscriptionEventService.process_update_event(event_data)
    assert subscription is not None


@pytest.mark.unit
def test_process_update_event(subscription_update_event_dict):
    event_data = json.loads(subscription_update_event_dict)
    response = SubscriptionEventService.process_update_event(event_data)
    assert response is True


@pytest.mark.unit
def test_process_create_event(subscription_create_event_dict):
    event_data = json.loads(subscription_create_event_dict)
    response = SubscriptionEventService.process_create_event(event_data)
    assert response is True


@pytest.mark.unit
def test_process_delete_event(subscription_delete_event_dict):
    # arrange
    mocked_subscription_mapper = MagicMock()
    mocked_subscription_mapper.map_delete_event.return_value = {'Stripe_Subscription_ID__c': '12345',
                                                                'npsp__Status__c': 'Canceled',
                                                                'npsp__ClosedReason__c': 'Webform Canceled'}
    mocked_salesforce_subscription = MagicMock()
    mocked_salesforce_subscription.update.return_value = 204
    mocked_salesforce_subscription.get_by_stripe_id.return_value = {'id': '999999', 'sf_contact_id': '88888'}
    subscription_event_processor = SubscriptionEventService(mapper=mocked_subscription_mapper,
                                                            salesforce_subscription=mocked_salesforce_subscription)
    # act
    response = subscription_event_processor.process_delete_event(subscription_delete_event_dict)
    # assert
    assert response is True


@pytest.mark.integration
def test_integration_process_delete_event(subscription_delete_event_dict):
    # arrange
    stripe_connection = StripeConnection()
    stripe_subscription_service = StripeSubscriptionService(stripe_connection)
    salesforce_subscription_service = SalesforceSubscriptionService()
    subscription_mapper = SubscriptionMapper(stripe_subscription=stripe_subscription_service,
                                             salesforce_subscription=salesforce_subscription_service)

    subscription_event_processor = SubscriptionEventService(mapper=subscription_mapper,
                                                            salesforce_subscription=salesforce_subscription_service)
    # act
    response = subscription_event_processor.process_delete_event(subscription_delete_event_dict)
    # assert
    assert response is True
