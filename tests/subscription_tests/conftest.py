import json

import pytest

from donors.donor import Donor
from subscriptions.subscription import Subscription


@pytest.fixture(autouse=True)
def mocked_donor_id(mocker):
    mocker.patch.object(Donor, 'exists_by_email', return_value="123456")

@pytest.fixture(autouse=True)
def mocked_sf_recurring_donation_id(mocker):
    mocker.patch.object(Subscription, 'exists', return_value={'id': '12345', 'sf_contact_id': '12345'})

@pytest.fixture
def open_subscription_json():
    return json.dumps({
        "id": "evt_1OuRZEL1MLd6bigCNHOdtRuT",
        "data": {
            "object": {
                "id": "sub_1OuRZCL1MLd6bigCf9ifDf0R",
                "plan": {
                    "id": "price_1OuRZCL1MLd6bigCz2Odee5l",
                    "active": False,
                    "amount": 10000,
                    "object": "plan",
                    "created": 1710473782,
                    "product": "prod_PjvEAdHZmRent5",
                    "currency": "usd",
                    "interval": "month",
                    "livemode": False,
                    "metadata": {},
                    "nickname": None,
                    "tiers_mode": None,
                    "usage_type": "licensed",
                    "amount_decimal": "10000",
                    "billing_scheme": "per_unit",
                    "interval_count": 1,
                    "aggregate_usage": None,
                    "transform_usage": None,
                    "trial_period_days": None
                },
                "items": {
                    "url": "/v1/subscription_items?subscription=sub_1OuRZCL1MLd6bigCf9ifDf0R",
                    "data": [
                        {
                            "id": "si_PjvQ486UOCqyTW",
                            "plan": {
                                "id": "price_1OuRZCL1MLd6bigCz2Odee5l",
                                "active": False,
                                "amount": 10000,
                                "object": "plan",
                                "created": 1710473782,
                                "product": "prod_PjvEAdHZmRent5",
                                "currency": "usd",
                                "interval": "month",
                                "livemode": False,
                                "metadata": {},
                                "nickname": None,
                                "tiers_mode": None,
                                "usage_type": "licensed",
                                "amount_decimal": "10000",
                                "billing_scheme": "per_unit",
                                "interval_count": 1,
                                "aggregate_usage": None,
                                "transform_usage": None,
                                "trial_period_days": None
                            },
                            "price": {
                                "id": "price_1OuRZCL1MLd6bigCz2Odee5l",
                                "type": "recurring",
                                "active": False,
                                "object": "price",
                                "created": 1710473782,
                                "product": "prod_PjvEAdHZmRent5",
                                "currency": "usd",
                                "livemode": False,
                                "metadata": {},
                                "nickname": None,
                                "recurring": {
                                    "interval": "month",
                                    "usage_type": "licensed",
                                    "interval_count": 1,
                                    "aggregate_usage": None,
                                    "trial_period_days": None
                                },
                                "lookup_key": None,
                                "tiers_mode": None,
                                "unit_amount": 10000,
                                "tax_behavior": "unspecified",
                                "billing_scheme": "per_unit",
                                "custom_unit_amount": None,
                                "transform_quantity": None,
                                "unit_amount_decimal": "10000"
                            },
                            "object": "subscription_item",
                            "created": 1710473783,
                            "metadata": {},
                            "quantity": 1,
                            "tax_rates": [],
                            "subscription": "sub_1OuRZCL1MLd6bigCf9ifDf0R",
                            "billing_thresholds": None
                        }
                    ],
                    "object": "list",
                    "has_more": False,
                    "total_count": 1
                },
                "object": "subscription",
                "status": "active",
                "created": 1710473782,
                "currency": "usd",
                "customer": "cus_PjBU4vGjx2wr3I",
                "discount": None,
                "ended_at": None,
                "livemode": False,
                "metadata": {},
                "quantity": 1,
                "schedule": None,
                "cancel_at": None,
                "trial_end": None,
                "start_date": 1710473782,
                "test_clock": None,
                "application": None,
                "canceled_at": None,
                "description": None,
                "trial_start": None,
                "on_behalf_of": None,
                "automatic_tax": {
                    "enabled": False,
                    "liability": None
                },
                "transfer_data": None,
                "days_until_due": None,
                "default_source": None,
                "latest_invoice": "in_1OuRZCL1MLd6bigCh5nxzBxZ",
                "pending_update": None,
                "trial_settings": {
                    "end_behavior": {
                        "missing_payment_method": "create_invoice"
                    }
                },
                "invoice_settings": {
                    "issuer": {
                        "type": "self"
                    },
                    "account_tax_ids": None
                },
                "pause_collection": None,
                "payment_settings": {
                    "payment_method_types": None,
                    "payment_method_options": None,
                    "save_default_payment_method": "off"
                },
                "collection_method": "charge_automatically",
                "default_tax_rates": [],
                "billing_thresholds": None,
                "current_period_end": 1713152182,
                "billing_cycle_anchor": 1710473782,
                "cancel_at_period_end": False,
                "cancellation_details": {
                    "reason": None,
                    "comment": None,
                    "feedback": None
                },
                "current_period_start": 1710473782,
                "pending_setup_intent": None,
                "default_payment_method": None,
                "application_fee_percent": None,
                "billing_cycle_anchor_config": None,
                "pending_invoice_item_interval": None,
                "next_pending_invoice_item_invoice": None
            }
        },
        "type": "customer.subscription.created",
        "object": "event",
        "created": 1710473784,
        "request": {
            "id": "req_bqfLoByWhhpd50",
            "idempotency_key": "8b36254e-868b-4621-83aa-98d634310106"
        },
        "livemode": False,
        "api_version": "2022-11-15",
        "pending_webhooks": 3
    })


@pytest.fixture
def canceled_subscription_json():
    return json.dumps({
    "id": "evt_1PCBNeL1MLd6bigCMmvVHJoF",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1714701466,
    "data": {
        "object": {
            "id": "sub_1P1hCDL1MLd6bigCTMM9YrD9",
            "object": "subscription",
            "application": "ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK",
            "application_fee_percent": None,
            "automatic_tax": {
                "enabled": False,
                "liability": None
            },
            "billing_cycle_anchor": 1712202157,
            "billing_cycle_anchor_config": None,
            "billing_thresholds": None,
            "cancel_at": None,
            "cancel_at_period_end": False,
            "canceled_at": 1714701465,
            "cancellation_details": {
                "comment": None,
                "feedback": None,
                "reason": "cancellation_requested"
            },
            "collection_method": "charge_automatically",
            "created": 1712202157,
            "currency": "usd",
            "current_period_end": 1714794157,
            "current_period_start": 1712202157,
            "customer": "cus_PrQ2qIHY8Jzywm",
            "days_until_due": None,
            "default_payment_method": "pm_1P1hCCL1MLd6bigCde45mpoC",
            "default_source": None,
            "default_tax_rates": [],
            "description": None,
            "discount": None,
            "discounts": [],
            "ended_at": 1714701465,
            "invoice_settings": {
                "account_tax_ids": None,
                "issuer": {
                    "type": "self"
                }
            },
            "items": {
                "object": "list",
                "data": [
                    {
                        "id": "si_PrQ28sJ5vSov5C",
                        "object": "subscription_item",
                        "billing_thresholds": None,
                        "created": 1712202158,
                        "discounts": [],
                        "metadata": {},
                        "plan": {
                            "id": "price_1OxZPCL1MLd6bigCglyGWwz9",
                            "object": "plan",
                            "active": True,
                            "aggregate_usage": None,
                            "amount": 100,
                            "amount_decimal": "100",
                            "billing_scheme": "per_unit",
                            "created": 1711218898,
                            "currency": "usd",
                            "interval": "month",
                            "interval_count": 1,
                            "livemode": False,
                            "metadata": {},
                            "meter": None,
                            "nickname": None,
                            "product": "prod_Pn9imCT8L9sSWq",
                            "tiers_mode": None,
                            "transform_usage": None,
                            "trial_period_days": None,
                            "usage_type": "licensed"
                        },
                        "price": {
                            "id": "price_1OxZPCL1MLd6bigCglyGWwz9",
                            "object": "price",
                            "active": True,
                            "billing_scheme": "per_unit",
                            "created": 1711218898,
                            "currency": "usd",
                            "custom_unit_amount": None,
                            "livemode": False,
                            "lookup_key": None,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_Pn9imCT8L9sSWq",
                            "recurring": {
                                "aggregate_usage": None,
                                "interval": "month",
                                "interval_count": 1,
                                "meter": None,
                                "trial_period_days": None,
                                "usage_type": "licensed"
                            },
                            "tax_behavior": "exclusive",
                            "tiers_mode": None,
                            "transform_quantity": None,
                            "type": "recurring",
                            "unit_amount": 100,
                            "unit_amount_decimal": "100"
                        },
                        "quantity": 1,
                        "subscription": "sub_1P1hCDL1MLd6bigCTMM9YrD9",
                        "tax_rates": []
                    }
                ],
                "has_more": False,
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1P1hCDL1MLd6bigCTMM9YrD9"
            },
            "latest_invoice": "in_1P1hCDL1MLd6bigCHsJ3eO2v",
            "livemode": False,
            "metadata": {
                "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 334286604"
            },
            "next_pending_invoice_item_invoice": None,
            "on_behalf_of": None,
            "pause_collection": None,
            "payment_settings": {
                "payment_method_options": None,
                "payment_method_types": None,
                "save_default_payment_method": "off"
            },
            "pending_invoice_item_interval": None,
            "pending_setup_intent": None,
            "pending_update": None,
            "plan": {
                "id": "price_1OxZPCL1MLd6bigCglyGWwz9",
                "object": "plan",
                "active": True,
                "aggregate_usage": None,
                "amount": 100,
                "amount_decimal": "100",
                "billing_scheme": "per_unit",
                "created": 1711218898,
                "currency": "usd",
                "interval": "month",
                "interval_count": 1,
                "livemode": False,
                "metadata": {},
                "meter": None,
                "nickname": None,
                "product": "prod_Pn9imCT8L9sSWq",
                "tiers_mode": None,
                "transform_usage": None,
                "trial_period_days": None,
                "usage_type": "licensed"
            },
            "quantity": 1,
            "schedule": None,
            "start_date": 1712202157,
            "status": "canceled",
            "test_clock": None,
            "transfer_data": None,
            "trial_end": None,
            "trial_settings": {
                "end_behavior": {
                    "missing_payment_method": "create_invoice"
                }
            },
            "trial_start": None
        }
    },
    "livemode": False,
    "pending_webhooks": 0,
    "request": {
        "id": "req_5zMHKtj6Nq5ARg",
        "idempotency_key": None
    },
    "type": "customer.subscription.deleted"
})
