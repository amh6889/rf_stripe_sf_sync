import json

import pytest

from donations.donation import Donation
from donors.donor import Donor
from subscriptions.subscription import Subscription


@pytest.fixture(autouse=True)
def mocked_donor_id(mocker):
    mocker.patch.object(Donor, 'exists_by_email', return_value="123456")

@pytest.fixture(autouse=True)
def mocked_donation_id(mocker):
    mocker.patch.object(Donation, 'exists', return_value="1111")

@pytest.fixture(autouse=True)
def mocked_stripe_subscription_id(mocker):
    mocker.patch.object(Donation, 'get_stripe_subscription_id', return_value="123456")

@pytest.fixture(autouse=True)
def mocked_sf_recurring_donation_id(mocker):
    mocker.patch.object(Subscription, 'exists', return_value={'id': '12345', 'sf_contact_id': '12345'})

@pytest.fixture(autouse=True)
def mocked_donor_email(mocker):
    mocker.patch.object(Donor, 'get_email', return_value="test_email@gmail.com")


@pytest.fixture
def successful_one_time_donation_json():
    return json.dumps({
        "id": "evt_3P2n9UL1MLd6bigC1PiqDXcA",
        "object": "event",
        "api_version": "2022-11-15",
        "created": 1712463382,
        "data": {
            "object": {
                "id": "pi_3P2n9UL1MLd6bigC19xRICS0",
                "object": "payment_intent",
                "amount": 44400,
                "amount_capturable": 0,
                "amount_details": {
                    "tip": {}
                },
                "amount_received": 44400,
                "application": "ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK",
                "application_fee_amount": None,
                "automatic_payment_methods": None,
                "canceled_at": None,
                "cancellation_reason": None,
                "capture_method": "automatic",
                "client_secret": "pi_3P2n9UL1MLd6bigC19xRICS0_secret_xo8o0WZuPEUepQdCvdZ1HPWBe",
                "confirmation_method": "automatic",
                "created": 1712463380,
                "currency": "usd",
                "customer": "cus_PsYFCxLSS3BlcX",
                "description": None,
                "invoice": None,
                "last_payment_error": None,
                "latest_charge": "ch_3P2n9UL1MLd6bigC19aOqPGG",
                "livemode": False,
                "metadata": {
                    "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 334671314"
                },
                "next_action": None,
                "on_behalf_of": None,
                "payment_method": "pm_1P2n9SL1MLd6bigCN9jtjuUN",
                "payment_method_configuration_details": None,
                "payment_method_options": {
                    "card": {
                        "installments": None,
                        "mandate_options": None,
                        "network": None,
                        "request_three_d_secure": "automatic"
                    }
                },
                "payment_method_types": [
                    "card"
                ],
                "processing": None,
                "receipt_email": None,
                "review": None,
                "setup_future_usage": None,
                "shipping": None,
                "source": None,
                "statement_descriptor": None,
                "statement_descriptor_suffix": None,
                "status": "succeeded",
                "transfer_data": None,
                "transfer_group": None
            }
        },
        "livemode": False,
        "pending_webhooks": 0,
        "request": {
            "id": "req_wCEvVgUcopOa1x",
            "idempotency_key": "8222b55d-0a4b-4b61-8eb8-e37a09e81314"
        },
        "type": "payment_intent.succeeded"
    })

@pytest.fixture
def refunded_donation_json():
    return json.dumps({
    "id": "evt_3P2n9UL1MLd6bigC1DaWCS36",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1714697065,
    "data": {
        "object": {
            "id": "ch_3P2n9UL1MLd6bigC19aOqPGG",
            "object": "charge",
            "amount": 44400,
            "amount_captured": 44400,
            "amount_refunded": 44400,
            "application": "ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK",
            "application_fee": None,
            "application_fee_amount": None,
            "balance_transaction": "txn_3P2n9UL1MLd6bigC1v4JwQCl",
            "billing_details": {
                "address": {
                    "city": "Lynchburg",
                    "country": "US",
                    "line1": "Apt I",
                    "line2": None,
                    "postal_code": "24502",
                    "state": "State"
                },
                "email": None,
                "name": "test test",
                "phone": None
            },
            "calculated_statement_descriptor": "REASONABLE FAITH",
            "captured": True,
            "created": 1712463382,
            "currency": "usd",
            "customer": "cus_PsYFCxLSS3BlcX",
            "description": None,
            "destination": None,
            "dispute": None,
            "disputed": False,
            "failure_balance_transaction": None,
            "failure_code": None,
            "failure_message": None,
            "fraud_details": {},
            "invoice": None,
            "livemode": False,
            "metadata": {
                "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 334671314"
            },
            "on_behalf_of": None,
            "order": None,
            "outcome": {
                "network_status": "approved_by_network",
                "reason": None,
                "risk_level": "normal",
                "risk_score": 20,
                "seller_message": "Payment complete.",
                "type": "authorized"
            },
            "paid": True,
            "payment_intent": "pi_3P2n9UL1MLd6bigC19xRICS0",
            "payment_method": "pm_1P2n9SL1MLd6bigCN9jtjuUN",
            "payment_method_details": {
                "card": {
                    "amount_authorized": 44400,
                    "brand": "visa",
                    "checks": {
                        "address_line1_check": "pass",
                        "address_postal_code_check": "pass",
                        "cvc_check": "pass"
                    },
                    "country": "US",
                    "exp_month": 11,
                    "exp_year": 2029,
                    "extended_authorization": {
                        "status": "disabled"
                    },
                    "fingerprint": "oicy5vjauTBFwHOp",
                    "funding": "credit",
                    "incremental_authorization": {
                        "status": "unavailable"
                    },
                    "installments": None,
                    "last4": "4242",
                    "mandate": None,
                    "multicapture": {
                        "status": "unavailable"
                    },
                    "network": "visa",
                    "network_token": {
                        "used": False
                    },
                    "overcapture": {
                        "maximum_amount_capturable": 44400,
                        "status": "unavailable"
                    },
                    "three_d_secure": None,
                    "wallet": None
                },
                "type": "card"
            },
            "radar_options": {},
            "receipt_email": None,
            "receipt_number": None,
            "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xS2pjVVFMMU1MZDZiaWdDKOnm0LEGMgZlzlREXnk6LBaYDg5icVsM40ubst2N4LQ6uoUMUFAOEzvMxwE3M5gD1CXCCt9Ih8oG7iRv",
            "refunded": True,
            "review": None,
            "shipping": None,
            "source": None,
            "source_transfer": None,
            "statement_descriptor": None,
            "statement_descriptor_suffix": None,
            "status": "succeeded",
            "transfer_data": None,
            "transfer_group": None
        },
        "previous_attributes": {
            "amount_refunded": 0,
            "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xS2pjVVFMMU1MZDZiaWdDKOjm0LEGMgZ1eSIanR06LBZcYX_mxGOg4Ht6ORvdivTy3ShDKx_qGZdc7jOt1JmrGo8G-W_5vkWkgNIE",
            "refunded": False
        }
    },
    "livemode": False,
    "pending_webhooks": 0,
    "request": {
        "id": "req_MpwPDBou1hVZEj",
        "idempotency_key": "46fccec2-f0c3-4427-8cbe-7d0ec867090a"
    },
    "type": "charge.refunded"
})


@pytest.fixture
def successful_subscription_donation_json():
    return json.dumps({
        "id": "evt_3P2gUyL1MLd6bigC0CDH7eZn",
        "object": "event",
        "api_version": "2022-11-15",
        "created": 1712437808,
        "data": {
            "object": {
                "id": "pi_3P2gUyL1MLd6bigC01NCKGjt",
                "object": "payment_intent",
                "amount": 99900,
                "amount_capturable": 0,
                "amount_details": {
                    "tip": {}
                },
                "amount_received": 99900,
                "application": "ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK",
                "application_fee_amount": None,
                "automatic_payment_methods": None,
                "canceled_at": None,
                "cancellation_reason": None,
                "capture_method": "automatic",
                "client_secret": "pi_3P2gUyL1MLd6bigC01NCKGjt_secret_qjifWMUoTVmXlnTr6gzA9CJJv",
                "confirmation_method": "automatic",
                "created": 1712437804,
                "currency": "usd",
                "customer": "cus_PsRNJif1dO5m7o",
                "description": "Subscription creation",
                "invoice": "in_1P2gUyL1MLd6bigC8TQkFBy2",
                "last_payment_error": None,
                "latest_charge": "ch_3P2gUyL1MLd6bigC0mZJcaso",
                "livemode": False,
                "metadata": {},
                "next_action": None,
                "on_behalf_of": None,
                "payment_method": "pm_1P2gUwL1MLd6bigC7hGWKgdf",
                "payment_method_configuration_details": None,
                "payment_method_options": {
                    "card": {
                        "installments": None,
                        "mandate_options": None,
                        "network": None,
                        "request_three_d_secure": "automatic"
                    },
                    "cashapp": {}
                },
                "payment_method_types": [
                    "card",
                    "cashapp"
                ],
                "processing": None,
                "receipt_email": None,
                "review": None,
                "setup_future_usage": "off_session",
                "shipping": None,
                "source": None,
                "statement_descriptor": None,
                "statement_descriptor_suffix": None,
                "status": "succeeded",
                "transfer_data": None,
                "transfer_group": None
            }
        },
        "livemode": False,
        "pending_webhooks": 0,
        "request": {
            "id": "req_D8CnyPIHd0KaGq",
            "idempotency_key": "7c0aa140-1032-4041-bc03-d989daa0aa10"
        },
        "type": "payment_intent.succeeded"
    }
    )
