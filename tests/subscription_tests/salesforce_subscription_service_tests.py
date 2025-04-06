import pytest

from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService


@pytest.mark.integration
def test_get_campaign_id():
    # arrange
    salesforce_subscription_service = SalesforceSubscriptionService()
    campaign_name = 'C0425 - Spring Campaign 2025'
    # act
    campaign_id = salesforce_subscription_service.get_campaign_id(campaign_name)
    # assert
    assert campaign_id is not None
    assert campaign_id == '701Ox00000h97pXIAQ'
