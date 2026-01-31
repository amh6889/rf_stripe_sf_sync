import pytest

from donations.donation_event_service import DonationEventService
from donations.donation_mapper import DonationMapper
from donations.donation_salesforce_service import SalesforceDonationService
from donations.donation_stripe_service import StripeDonationService

from donors.donor_salesforce_service import SalesforceDonorService
from donors.donor_stripe_service import StripeDonorService
from salesforce.salesforce_email_service import SalesforceEmailService
from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService
from utils.stripe_connection import StripeConnection


@pytest.mark.integration
def test_donation_failure_event_works(donation_failure_event):
    #arrange
    stripe_connection = StripeConnection()
    salesforce_subscription_service = SalesforceSubscriptionService()
    salesforce_donor_service = SalesforceDonorService()
    salesforce_donation_service = SalesforceDonationService()
    stripe_donation_service = StripeDonationService(stripe_connection)
    stripe_donor_service = StripeDonorService(stripe_connection)
    salesforce_email_service = SalesforceEmailService()
    donation_mapper = DonationMapper(salesforce_subscription=salesforce_subscription_service,
                                     salesforce_donor=salesforce_donor_service,
                                     stripe_donor=stripe_donor_service,
                                     stripe_donation=stripe_donation_service)
    donation_event_service = DonationEventService(donation_mapper=donation_mapper,
                                                  salesforce_donation=salesforce_donation_service,
                                                  stripe_donation_service=stripe_donation_service,
                                                  email_donation_service=salesforce_email_service)
    #act
    success = donation_event_service.process_failure_event(donation_failure_event)
    #assert
    assert success is True


@pytest.mark.integration
def test_donation_create_event_works(donation_failure_event_1_31_26):
    #arrange
    stripe_connection = StripeConnection()
    salesforce_subscription_service = SalesforceSubscriptionService()
    salesforce_donor_service = SalesforceDonorService()
    salesforce_donation_service = SalesforceDonationService()
    stripe_donation_service = StripeDonationService(stripe_connection)
    stripe_donor_service = StripeDonorService(stripe_connection)
    salesforce_email_service = SalesforceEmailService()
    donation_mapper = DonationMapper(salesforce_subscription=salesforce_subscription_service,
                                     salesforce_donor=salesforce_donor_service,
                                     stripe_donor=stripe_donor_service,
                                     stripe_donation=stripe_donation_service)
    donation_event_service = DonationEventService(donation_mapper=donation_mapper,
                                                  salesforce_donation=salesforce_donation_service,
                                                  stripe_donation_service=stripe_donation_service,
                                                  email_donation_service=salesforce_email_service)
    #act
    sf_donation_id = donation_event_service.process_create_event(donation_failure_event_1_31_26)
    #assert
    assert sf_donation_id is not None