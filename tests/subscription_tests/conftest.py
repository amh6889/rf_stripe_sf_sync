import json

import pytest

from donors.donor import Donor
from subscriptions.subscription import Subscription


#@pytest.fixture(autouse=True)
@pytest.fixture
def mocked_donor_id(mocker):
    mocker.patch.object(Donor, 'exists_by_email', return_value="123456")

#@pytest.fixture(autouse=True)
@pytest.fixture
def mocked_sf_recurring_donation_id(mocker):
    mocker.patch.object(Subscription, 'exists', return_value={'id': '12345', 'sf_contact_id': '12345'})

@pytest.fixture
def open_active_subscription_json():
    return json.dumps({
    "id": "evt_1PFUWHL1MLd6bigCVAZSTwAY",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1715490021,
    "data": {
        "object": {
            "id": "sub_1PFUWGL1MLd6bigCFPlOUlAD",
            "object": "subscription",
            "application": "ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK",
            "application_fee_percent": None,
            "automatic_tax": {
                "enabled": False,
                "liability": None
            },
            "billing_cycle_anchor": 1715490020,
            "billing_cycle_anchor_config": None,
            "billing_thresholds": None,
            "cancel_at": None,
            "cancel_at_period_end": False,
            "canceled_at": None,
            "cancellation_details": {
                "comment": None,
                "feedback": None,
                "reason": None
            },
            "collection_method": "charge_automatically",
            "created": 1715490020,
            "currency": "usd",
            "current_period_end": 1718168420,
            "current_period_start": 1715490020,
            "customer": "cus_Q5frnnA09N8teA",
            "days_until_due": None,
            "default_payment_method": "pm_1PFUWEL1MLd6bigCTmHNXMmz",
            "default_source": None,
            "default_tax_rates": [],
            "description": None,
            "discount": None,
            "discounts": [],
            "ended_at": None,
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
                        "id": "si_Q5fsKjBb2W26aP",
                        "object": "subscription_item",
                        "billing_thresholds": None,
                        "created": 1715490020,
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
                        "quantity": 555,
                        "subscription": "sub_1PFUWGL1MLd6bigCFPlOUlAD",
                        "tax_rates": []
                    }
                ],
                "has_more": False,
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1PFUWGL1MLd6bigCFPlOUlAD"
            },
            "latest_invoice": "in_1PFUWGL1MLd6bigC0GTmyKFu",
            "livemode": False,
            "metadata": {
                "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 338509469"
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
            "quantity": 555,
            "schedule": None,
            "start_date": 1715490020,
            "status": "incomplete",
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
        "id": "req_EY9LePtsEx7kgF",
        "idempotency_key": "4d702001-ef82-40a5-8075-6aa9895f50cc"
    },
    "type": "customer.subscription.created"
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

@pytest.fixture
def subscription_update_event_json():
    return json.dumps({'id': 'evt_1PVm1GL1MLd6bigCoqQjk6zQ', 'object': 'event', 'api_version': '2022-11-15', 'created': 1719370537, 'data': {'object': {'id': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'object': 'subscription', 'application': 'ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK', 'application_fee_percent': None, 'automatic_tax': {'enabled': False, 'liability': None}, 'billing_cycle_anchor': 1719370533, 'billing_cycle_anchor_config': None, 'billing_thresholds': None, 'cancel_at': None, 'cancel_at_period_end': False, 'canceled_at': None, 'cancellation_details': {'comment': None, 'feedback': None, 'reason': None}, 'collection_method': 'charge_automatically', 'created': 1719370533, 'currency': 'usd', 'current_period_end': 1721962533, 'current_period_start': 1719370533, 'customer': 'cus_QMV1TWElciMIsp', 'days_until_due': None, 'default_payment_method': 'pm_1PVm1AL1MLd6bigCRlSbSUHf', 'default_source': None, 'default_tax_rates': [], 'description': None, 'discount': None, 'discounts': [], 'ended_at': None, 'invoice_settings': {'account_tax_ids': None, 'issuer': {'type': 'self'}}, 'items': {'object': 'list', 'data': [{'id': 'si_QMV1IuZHIUIeZT', 'object': 'subscription_item', 'billing_thresholds': None, 'created': 1719370534, 'discounts': [], 'metadata': {}, 'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True, 'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100', 'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd', 'interval': 'month', 'interval_count': 1, 'livemode': False, 'metadata': {}, 'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq', 'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None, 'usage_type': 'licensed'}, 'price': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'price', 'active': True, 'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd', 'custom_unit_amount': None, 'livemode': False, 'lookup_key': None, 'metadata': {}, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq', 'recurring': {'aggregate_usage': None, 'interval': 'month', 'interval_count': 1, 'meter': None, 'trial_period_days': None, 'usage_type': 'licensed'}, 'tax_behavior': 'exclusive', 'tiers_mode': None, 'transform_quantity': None, 'type': 'recurring', 'unit_amount': 100, 'unit_amount_decimal': '100'}, 'quantity': 987, 'subscription': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'tax_rates': []}], 'has_more': False, 'total_count': 1, 'url': '/v1/subscription_items?subscription=sub_1PVm1CL1MLd6bigCoJNJkhJi'}, 'latest_invoice': 'in_1PVm1CL1MLd6bigCx2nkQ8lL', 'livemode': False, 'metadata': {'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 343927769'}, 'next_pending_invoice_item_invoice': None, 'on_behalf_of': None, 'pause_collection': None, 'payment_settings': {'payment_method_options': None, 'payment_method_types': None, 'save_default_payment_method': 'off'}, 'pending_invoice_item_interval': None, 'pending_setup_intent': None, 'pending_update': None, 'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True, 'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100', 'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd', 'interval': 'month', 'interval_count': 1, 'livemode': False, 'metadata': {}, 'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq', 'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None, 'usage_type': 'licensed'}, 'quantity': 987, 'schedule': None, 'start_date': 1719370533, 'status': 'active', 'test_clock': None, 'transfer_data': None, 'trial_end': None, 'trial_settings': {'end_behavior': {'missing_payment_method': 'create_invoice'}}, 'trial_start': None}, 'previous_attributes': {'status': 'incomplete'}}, 'livemode': False, 'pending_webhooks': 1, 'request': {'id': 'req_37pTMnB2c23SCI', 'idempotency_key': 'e4a69b4e-d993-4a85-9dab-061028dd3245'}, 'type': 'customer.subscription.updated'})
