import json

from subscriptions.subscription_event_processor import SubscriptionEventProcessor


def test_subscription_error_8_18_24(subscription_error_8_18_24):
    event_data = json.loads(subscription_error_8_18_24)
    subscription = SubscriptionEventProcessor.process_update_event(event_data)
    assert subscription is not None


def test_process_update_event(subscription_update_event_json):
    event_data = json.loads(subscription_update_event_json)
    response = SubscriptionEventProcessor.process_update_event(event_data)
    assert response is True


def test_process_create_event(subscription_create_event_json):
    event_data = json.loads(subscription_create_event_json)
    response = SubscriptionEventProcessor.process_create_event(event_data)
    assert response is True


def test_process_delete_event(subscription_delete_event_json):
    event_data = json.loads(subscription_delete_event_json)
    response = SubscriptionEventProcessor.process_delete_event(event_data)
    assert response is True
