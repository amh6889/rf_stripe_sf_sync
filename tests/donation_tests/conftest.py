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
    "id": "evt_3P2n9UL1MLd6bigC1QFCdJOw",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1712463382,
    "data": {
        "object": {
            "id": "ch_3P2n9UL1MLd6bigC19aOqPGG",
            "object": "charge",
            "amount": 44400,
            "amount_captured": 44400,
            "amount_refunded": 0,
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
            "receipt_url": "https://pay.stripe.com/receipts/payment/CAcaFwoVYWNjdF8xS2pjVVFMMU1MZDZiaWdDKJe8yLAGMgZkgluA81o6LBZ89Vomt7W0lk_MKhMM4uGfM98z9YxjMnWEfErPxGHcZMcLMWO1laApmaX7",
            "refunded": False,
            "review": None,
            "shipping": None,
            "source": None,
            "source_transfer": None,
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
    "type": "charge.succeeded"
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
    "id": "evt_3P2gUyL1MLd6bigC0y7msSzJ",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1712437808,
    "data": {
        "object": {
            "id": "ch_3P2gUyL1MLd6bigC0mZJcaso",
            "object": "charge",
            "amount": 99900,
            "amount_captured": 99900,
            "amount_refunded": 0,
            "application": "ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK",
            "application_fee": None,
            "application_fee_amount": None,
            "balance_transaction": "txn_3P2gUyL1MLd6bigC0Q935piD",
            "billing_details": {
                "address": {
                    "city": "Lynchburg",
                    "country": "US",
                    "line1": "406 Stonemill Dr",
                    "line2": None,
                    "postal_code": "24502",
                    "state": "State"
                },
                "email": None,
                "name": "Boba Fett",
                "phone": None
            },
            "calculated_statement_descriptor": "REASONABLE FAITH",
            "captured": True,
            "created": 1712437807,
            "currency": "usd",
            "customer": "cus_PsRNJif1dO5m7o",
            "description": "Subscription creation",
            "destination": None,
            "dispute": None,
            "disputed": False,
            "failure_balance_transaction": None,
            "failure_code": None,
            "failure_message": None,
            "fraud_details": {},
            "invoice": "in_1P2gUyL1MLd6bigC8TQkFBy2",
            "livemode": False,
            "metadata": {},
            "on_behalf_of": None,
            "order": None,
            "outcome": {
                "network_status": "approved_by_network",
                "reason": None,
                "risk_level": "normal",
                "risk_score": 64,
                "seller_message": "Payment complete.",
                "type": "authorized"
            },
            "paid": True,
            "payment_intent": "pi_3P2gUyL1MLd6bigC01NCKGjt",
            "payment_method": "pm_1P2gUwL1MLd6bigC7hGWKgdf",
            "payment_method_details": {
                "card": {
                    "amount_authorized": 99900,
                    "brand": "visa",
                    "checks": {
                        "address_line1_check": "pass",
                        "address_postal_code_check": "pass",
                        "cvc_check": "pass"
                    },
                    "country": "US",
                    "exp_month": 11,
                    "exp_year": 2025,
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
                        "maximum_amount_capturable": 99900,
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
            "receipt_url": "https://pay.stripe.com/receipts/invoices/CAcaFwoVYWNjdF8xS2pjVVFMMU1MZDZiaWdDKLH0xrAGMgZ27ggWUog6LBaFaJRVgIuUbnbbdYHCOzV2ZV7g3XCKJvO6PVlesylDPF-lHtL4OaHQQH3J?s=ap",
            "refunded": False,
            "review": None,
            "shipping": None,
            "source": None,
            "source_transfer": None,
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
    "type": "charge.succeeded"
}
    )
