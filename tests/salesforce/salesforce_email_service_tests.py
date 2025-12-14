from salesforce.salesforce_email_service import SalesforceEmailService


def test_send_email_works():
    #arrange
    salesforce_email_service = SalesforceEmailService()
    stripe_subscription_id = "sub_1QON1WL1MLd6bigC8Sr2sEo9"
    last4 = "1111"
    #act
    salesforce_email_service.send_email(stripe_subscription_id, last4)
    #assert