import pytest

from subscriptions.subscription_stripe_service import StripeSubscriptionService
from utils.stripe_connection import StripeConnection

@pytest.mark.integration
def test_get_subscription_schedule_works_when_subscription_schedule_id_exists():
    # arrange
    stripe_connection = StripeConnection()
    subscription_service = StripeSubscriptionService(stripe_connection)
    subscription_schedule_id = 'sub_sched_1QaNtTL1MLd6bigC9AQHNWKK'
    # act
    subscription_schedule = subscription_service.get_subscription_schedule(subscription_schedule_id)
    # assert
    print(subscription_schedule)
    assert subscription_schedule is not None

@pytest.mark.integration
def test_get_subscription_schedule_works_when_subscription_schedule_id_does_not_exist():
    # arrange
    stripe_connection = StripeConnection()
    subscription_service = StripeSubscriptionService(stripe_connection)
    subscription_schedule_id = '12345'
    # act
    with pytest.raises(Exception, match="No such subscription schedule: '12345'"):
        subscription_schedule = subscription_service.get_subscription_schedule(subscription_schedule_id)
        # assert
        assert subscription_schedule is not None