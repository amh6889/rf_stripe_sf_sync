import pytest

from donations.donation_stripe_service import StripeDonationService
from utils.stripe_connection import StripeConnection

@pytest.mark.integration
def test_retrieving_stripe_subscription_id_from_payment_intent_works():
    connection = StripeConnection()
    stripe_donation_service = StripeDonationService(connection)
    invoice_id = 'in_1P2gUyL1MLd6bigC8TQkFBy2'
    subscription_id = stripe_donation_service.get_stripe_subscription_by_invoice_id(invoice_id)
    assert subscription_id is not None
