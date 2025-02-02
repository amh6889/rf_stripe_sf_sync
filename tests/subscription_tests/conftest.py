import json

import pytest

from subscriptions.subscription_salesforce_service import SalesforceSubscriptionService


# @pytest.fixture(autouse=True)
# @pytest.fixture
# def mocked_donor_id(mocker):
#     mocker.patch.object(SalesforceDonorService, 'exists_by_email', return_value="123456")


# @pytest.fixture(autouse=True)
@pytest.fixture
def mocked_sf_recurring_donation_id(mocker):
    mocker.patch.object(SalesforceSubscriptionService, 'exists', return_value={'id': '12345', 'sf_contact_id': '12345'})

@pytest.fixture
def mocked_subscription_schedule():
    return {
  "application": None,
  "canceled_at": None,
  "completed_at": None,
  "created": 1735245775,
  "current_phase": {
    "end_date": 1740114000,
    "start_date": 1737435600
  },
  "customer": "cus_RTKTPO89z5Ge53",
  "default_settings": {
    "application_fee_percent": None,
    "automatic_tax": {
      "disabled_reason": None,
      "enabled": False,
      "liability": None
    },
    "billing_cycle_anchor": "automatic",
    "billing_thresholds": None,
    "collection_method": "charge_automatically",
    "default_payment_method": None,
    "default_source": None,
    "description": None,
    "invoice_settings": {
      "account_tax_ids": None,
      "days_until_due": None,
      "issuer": {
        "type": "self"
      }
    },
    "on_behalf_of": None,
    "transfer_data": None
  },
  "end_behavior": "release",
  "id": "sub_sched_1QaNtTL1MLd6bigC9AQHNWKK",
  "livemode": False,
  "metadata": {
    "anetSubscriptionId": "65804855"
  },
  "object": "subscription_schedule",
  "phases": [
    {
      "add_invoice_items": [],
      "application_fee_percent": None,
      "billing_cycle_anchor": None,
      "billing_thresholds": None,
      "collection_method": None,
      "coupon": None,
      "currency": "usd",
      "default_payment_method": None,
      "default_tax_rates": [],
      "description": None,
      "discounts": [],
      "end_date": 1740114000,
      "invoice_settings": None,
      "items": [
        {
          "billing_thresholds": None,
          "discounts": [],
          "metadata": {},
          "plan": "price_1QPdeSL1MLd6bigC8hHq4zFm",
          "price": "price_1QPdeSL1MLd6bigC8hHq4zFm",
          "quantity": 1,
          "tax_rates": []
        }
      ],
      "metadata": {},
      "on_behalf_of": None,
      "proration_behavior": "create_prorations",
      "start_date": 1737435600,
      "transfer_data": None,
      "trial_end": None
    }
  ],
  "released_at": None,
  "released_subscription": None,
  "renewal_interval": None,
  "status": "active",
  "subscription": "sub_1QjZZiL1MLd6bigC1zMiPpEz",
  "test_clock": None
}

@pytest.fixture
def fixed_active_subscription_dict():
    return {
    "id": "evt_1QjZZjL1MLd6bigC1mQePBRn",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1737435631,
    "data": {
        "object": {
            "id": "sub_1QjZZiL1MLd6bigC1zMiPpEz",
            "object": "subscription",
            "application": None,
            "application_fee_percent": None,
            "automatic_tax": {
                "disabled_reason": None,
                "enabled": False,
                "liability": None
            },
            "billing_cycle_anchor": 1737435600,
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
            "created": 1737435600,
            "currency": "usd",
            "current_period_end": 1740114000,
            "current_period_start": 1737435600,
            "customer": "cus_RTKTPO89z5Ge53",
            "days_until_due": None,
            "default_payment_method": None,
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
                        "id": "si_RcpEwuWfoPFsnS",
                        "object": "subscription_item",
                        "billing_thresholds": None,
                        "created": 1737435631,
                        "discounts": [],
                        "metadata": {},
                        "plan": {
                            "id": "price_1QPdeSL1MLd6bigC8hHq4zFm",
                            "object": "plan",
                            "active": True,
                            "aggregate_usage": None,
                            "amount": 5000,
                            "amount_decimal": "5000",
                            "billing_scheme": "per_unit",
                            "created": 1732684740,
                            "currency": "usd",
                            "interval": "month",
                            "interval_count": 1,
                            "livemode": False,
                            "metadata": {},
                            "meter": None,
                            "nickname": None,
                            "product": "prod_RIDuesaY2hbu6F",
                            "tiers_mode": None,
                            "transform_usage": None,
                            "trial_period_days": None,
                            "usage_type": "licensed"
                        },
                        "price": {
                            "id": "price_1QPdeSL1MLd6bigC8hHq4zFm",
                            "object": "price",
                            "active": True,
                            "billing_scheme": "per_unit",
                            "created": 1732684740,
                            "currency": "usd",
                            "custom_unit_amount": None,
                            "livemode": False,
                            "lookup_key": "1_month_5000_recurring_donation",
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_RIDuesaY2hbu6F",
                            "recurring": {
                                "aggregate_usage": None,
                                "interval": "month",
                                "interval_count": 1,
                                "meter": None,
                                "trial_period_days": None,
                                "usage_type": "licensed"
                            },
                            "tax_behavior": "unspecified",
                            "tiers_mode": None,
                            "transform_quantity": None,
                            "type": "recurring",
                            "unit_amount": 5000,
                            "unit_amount_decimal": "5000"
                        },
                        "quantity": 1,
                        "subscription": "sub_1QjZZiL1MLd6bigC1zMiPpEz",
                        "tax_rates": []
                    }
                ],
                "has_more": False,
                "total_count": 1,
                "url": "/v1/subscription_items?subscription=sub_1QjZZiL1MLd6bigC1zMiPpEz"
            },
            "latest_invoice": "in_1QjZZiL1MLd6bigCgdJSDASj",
            "livemode": False,
            "metadata": {},
            "next_pending_invoice_item_invoice": None,
            "on_behalf_of": None,
            "pause_collection": None,
            "payment_settings": {
                "payment_method_options": None,
                "payment_method_types": None,
                "save_default_payment_method": None
            },
            "pending_invoice_item_interval": None,
            "pending_setup_intent": None,
            "pending_update": None,
            "plan": {
                "id": "price_1QPdeSL1MLd6bigC8hHq4zFm",
                "object": "plan",
                "active": True,
                "aggregate_usage": None,
                "amount": 5000,
                "amount_decimal": "5000",
                "billing_scheme": "per_unit",
                "created": 1732684740,
                "currency": "usd",
                "interval": "month",
                "interval_count": 1,
                "livemode": False,
                "metadata": {},
                "meter": None,
                "nickname": None,
                "product": "prod_RIDuesaY2hbu6F",
                "tiers_mode": None,
                "transform_usage": None,
                "trial_period_days": None,
                "usage_type": "licensed"
            },
            "quantity": 1,
            "schedule": "sub_sched_1QaNtTL1MLd6bigC9AQHNWKK",
            "start_date": 1737435600,
            "status": "active",
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
        "id": None,
        "idempotency_key": None
    },
    "type": "customer.subscription.created"
}

@pytest.fixture
def open_active_subscription_dict():
    return {
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
                    "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 338509469",
                    "campaign_code": "F000"
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
    }


@pytest.fixture
def canceled_subscription_dict():
    return {
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
    }


@pytest.fixture
def subscription_error_8_18_24():
    return json.dumps(
        {'id': 'evt_1PozfsL1MLd6bigCILWLFYk3', 'object': 'event', 'api_version': '2022-11-15', 'created': 1723951260,
         'data': {'object': {'id': 'sub_1PdkqmL1MLd6bigCvl9AfiPa', 'object': 'subscription',
                             'application': 'ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK', 'application_fee_percent': None,
                             'automatic_tax': {'enabled': False, 'liability': None}, 'billing_cycle_anchor': 1721272668,
                             'billing_cycle_anchor_config': None, 'billing_thresholds': None, 'cancel_at': None,
                             'cancel_at_period_end': False, 'canceled_at': None,
                             'cancellation_details': {'comment': None, 'feedback': None, 'reason': None},
                             'collection_method': 'charge_automatically', 'created': 1721272668, 'currency': 'usd',
                             'current_period_end': 1726629468, 'current_period_start': 1723951068,
                             'customer': 'cus_QUkLINtx3jUr7v', 'days_until_due': None,
                             'default_payment_method': 'pm_1PdkqkL1MLd6bigCSceIpC60', 'default_source': None,
                             'default_tax_rates': [], 'description': None, 'discount': None, 'discounts': [],
                             'ended_at': None,
                             'invoice_settings': {'account_tax_ids': None, 'issuer': {'type': 'self'}},
                             'items': {'object': 'list', 'data': [
                                 {'id': 'si_QUkLKPwGLaWs5s', 'object': 'subscription_item', 'billing_thresholds': None,
                                  'created': 1721272669, 'discounts': [], 'metadata': {},
                                  'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                           'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                           'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                           'interval': 'month', 'interval_count': 1, 'livemode': False, 'metadata': {},
                                           'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                           'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                           'usage_type': 'licensed'},
                                  'price': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'price', 'active': True,
                                            'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                            'custom_unit_amount': None, 'livemode': False, 'lookup_key': None,
                                            'metadata': {}, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                            'recurring': {'aggregate_usage': None, 'interval': 'month',
                                                          'interval_count': 1, 'meter': None, 'trial_period_days': None,
                                                          'usage_type': 'licensed'}, 'tax_behavior': 'exclusive',
                                            'tiers_mode': None, 'transform_quantity': None, 'type': 'recurring',
                                            'unit_amount': 100, 'unit_amount_decimal': '100'}, 'quantity': 444,
                                  'subscription': 'sub_1PdkqmL1MLd6bigCvl9AfiPa', 'tax_rates': []}], 'has_more': False,
                                       'total_count': 1,
                                       'url': '/v1/subscription_items?subscription=sub_1PdkqmL1MLd6bigCvl9AfiPa'},
                             'latest_invoice': 'in_1PozfrL1MLd6bigCm34AiBgp', 'livemode': False, 'metadata': {
                 'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 346955642',
                 'campaign_code': 'F000 - General'}, 'next_pending_invoice_item_invoice': None, 'on_behalf_of': None,
                             'pause_collection': None,
                             'payment_settings': {'payment_method_options': None, 'payment_method_types': None,
                                                  'save_default_payment_method': 'off'},
                             'pending_invoice_item_interval': None, 'pending_setup_intent': None,
                             'pending_update': None,
                             'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                      'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                      'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                      'interval': 'month', 'interval_count': 1, 'livemode': False, 'metadata': {},
                                      'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                      'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                      'usage_type': 'licensed'}, 'quantity': 444, 'schedule': None,
                             'start_date': 1721272668, 'status': 'active', 'test_clock': None, 'transfer_data': None,
                             'trial_end': None,
                             'trial_settings': {'end_behavior': {'missing_payment_method': 'create_invoice'}},
                             'trial_start': None},
                  'previous_attributes': {'current_period_end': 1723951068, 'current_period_start': 1721272668,
                                          'latest_invoice': 'in_1PdkqmL1MLd6bigCLKZDEOvT'}}, 'livemode': False,
         'pending_webhooks': 1, 'request': {'id': None, 'idempotency_key': None},
         'type': 'customer.subscription.updated'})


@pytest.fixture
def subscription_update_event_dict():
    return {'id': 'evt_1PVm1GL1MLd6bigCoqQjk6zQ', 'object': 'event', 'api_version': '2022-11-15', 'created': 1719370537,
            'data': {'object': {'id': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'object': 'subscription',
                                'application': 'ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK', 'application_fee_percent': None,
                                'automatic_tax': {'enabled': False, 'liability': None},
                                'billing_cycle_anchor': 1719370533,
                                'billing_cycle_anchor_config': None, 'billing_thresholds': None, 'cancel_at': None,
                                'cancel_at_period_end': False, 'canceled_at': None,
                                'cancellation_details': {'comment': None, 'feedback': None, 'reason': None},
                                'collection_method': 'charge_automatically', 'created': 1719370533, 'currency': 'usd',
                                'current_period_end': 1721962533, 'current_period_start': 1719370533,
                                'customer': 'cus_QMV1TWElciMIsp', 'days_until_due': None,
                                'default_payment_method': 'pm_1PVm1AL1MLd6bigCRlSbSUHf', 'default_source': None,
                                'default_tax_rates': [], 'description': None, 'discount': None, 'discounts': [],
                                'ended_at': None,
                                'invoice_settings': {'account_tax_ids': None, 'issuer': {'type': 'self'}},
                                'items': {'object': 'list', 'data': [
                                    {'id': 'si_QMV1IuZHIUIeZT', 'object': 'subscription_item',
                                     'billing_thresholds': None,
                                     'created': 1719370534, 'discounts': [], 'metadata': {},
                                     'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                              'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                              'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                              'interval': 'month', 'interval_count': 1, 'livemode': False,
                                              'metadata': {},
                                              'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                              'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                              'usage_type': 'licensed'},
                                     'price': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'price',
                                               'active': True,
                                               'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                               'custom_unit_amount': None, 'livemode': False, 'lookup_key': None,
                                               'metadata': {}, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                               'recurring': {'aggregate_usage': None, 'interval': 'month',
                                                             'interval_count': 1, 'meter': None,
                                                             'trial_period_days': None,
                                                             'usage_type': 'licensed'}, 'tax_behavior': 'exclusive',
                                               'tiers_mode': None, 'transform_quantity': None, 'type': 'recurring',
                                               'unit_amount': 100, 'unit_amount_decimal': '100'}, 'quantity': 987,
                                     'subscription': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'tax_rates': []}],
                                          'has_more': False,
                                          'total_count': 1,
                                          'url': '/v1/subscription_items?subscription=sub_1PVm1CL1MLd6bigCoJNJkhJi'},
                                'latest_invoice': 'in_1PVm1CL1MLd6bigCx2nkQ8lL', 'livemode': False, 'metadata': {
                    'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 343927769'},
                                'next_pending_invoice_item_invoice': None, 'on_behalf_of': None,
                                'pause_collection': None,
                                'payment_settings': {'payment_method_options': None, 'payment_method_types': None,
                                                     'save_default_payment_method': 'off'},
                                'pending_invoice_item_interval': None, 'pending_setup_intent': None,
                                'pending_update': None,
                                'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                         'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                         'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                         'interval': 'month', 'interval_count': 1, 'livemode': False, 'metadata': {},
                                         'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                         'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                         'usage_type': 'licensed'}, 'quantity': 987, 'schedule': None,
                                'start_date': 1719370533, 'status': 'active', 'test_clock': None, 'transfer_data': None,
                                'trial_end': None,
                                'trial_settings': {'end_behavior': {'missing_payment_method': 'create_invoice'}},
                                'trial_start': None}, 'previous_attributes': {'status': 'incomplete'}},
            'livemode': False,
            'pending_webhooks': 1,
            'request': {'id': 'req_37pTMnB2c23SCI', 'idempotency_key': 'e4a69b4e-d993-4a85-9dab-061028dd3245'},
            'type': 'customer.subscription.updated'}


# TODO: make sure to grab actual create event json from Stripe (this is just copied form update event json)
@pytest.fixture
def subscription_create_event_dict():
    return {'id': 'evt_1PVm1GL1MLd6bigCoqQjk6zQ', 'object': 'event', 'api_version': '2022-11-15', 'created': 1719370537,
            'data': {'object': {'id': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'object': 'subscription',
                                'application': 'ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK', 'application_fee_percent': None,
                                'automatic_tax': {'enabled': False, 'liability': None},
                                'billing_cycle_anchor': 1719370533,
                                'billing_cycle_anchor_config': None, 'billing_thresholds': None, 'cancel_at': None,
                                'cancel_at_period_end': False, 'canceled_at': None,
                                'cancellation_details': {'comment': None, 'feedback': None, 'reason': None},
                                'collection_method': 'charge_automatically', 'created': 1719370533, 'currency': 'usd',
                                'current_period_end': 1721962533, 'current_period_start': 1719370533,
                                'customer': 'cus_QMV1TWElciMIsp', 'days_until_due': None,
                                'default_payment_method': 'pm_1PVm1AL1MLd6bigCRlSbSUHf', 'default_source': None,
                                'default_tax_rates': [], 'description': None, 'discount': None, 'discounts': [],
                                'ended_at': None,
                                'invoice_settings': {'account_tax_ids': None, 'issuer': {'type': 'self'}},
                                'items': {'object': 'list', 'data': [
                                    {'id': 'si_QMV1IuZHIUIeZT', 'object': 'subscription_item',
                                     'billing_thresholds': None,
                                     'created': 1719370534, 'discounts': [], 'metadata': {},
                                     'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                              'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                              'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                              'interval': 'month', 'interval_count': 1, 'livemode': False,
                                              'metadata': {},
                                              'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                              'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                              'usage_type': 'licensed'},
                                     'price': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'price',
                                               'active': True,
                                               'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                               'custom_unit_amount': None, 'livemode': False, 'lookup_key': None,
                                               'metadata': {}, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                               'recurring': {'aggregate_usage': None, 'interval': 'month',
                                                             'interval_count': 1, 'meter': None,
                                                             'trial_period_days': None,
                                                             'usage_type': 'licensed'}, 'tax_behavior': 'exclusive',
                                               'tiers_mode': None, 'transform_quantity': None, 'type': 'recurring',
                                               'unit_amount': 100, 'unit_amount_decimal': '100'}, 'quantity': 987,
                                     'subscription': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'tax_rates': []}],
                                          'has_more': False,
                                          'total_count': 1,
                                          'url': '/v1/subscription_items?subscription=sub_1PVm1CL1MLd6bigCoJNJkhJi'},
                                'latest_invoice': 'in_1PVm1CL1MLd6bigCx2nkQ8lL', 'livemode': False, 'metadata': {
                    'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 343927769'},
                                'next_pending_invoice_item_invoice': None, 'on_behalf_of': None,
                                'pause_collection': None,
                                'payment_settings': {'payment_method_options': None, 'payment_method_types': None,
                                                     'save_default_payment_method': 'off'},
                                'pending_invoice_item_interval': None, 'pending_setup_intent': None,
                                'pending_update': None,
                                'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                         'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                         'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                         'interval': 'month', 'interval_count': 1, 'livemode': False, 'metadata': {},
                                         'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                         'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                         'usage_type': 'licensed'}, 'quantity': 987, 'schedule': None,
                                'start_date': 1719370533, 'status': 'active', 'test_clock': None, 'transfer_data': None,
                                'trial_end': None,
                                'trial_settings': {'end_behavior': {'missing_payment_method': 'create_invoice'}},
                                'trial_start': None}, 'previous_attributes': {'status': 'incomplete'}},
            'livemode': False,
            'pending_webhooks': 1,
            'request': {'id': 'req_37pTMnB2c23SCI', 'idempotency_key': 'e4a69b4e-d993-4a85-9dab-061028dd3245'},
            'type': 'customer.subscription.updated'}


# TODO: make sure to grab actual delete event json from Stripe (this is just copied form update event json)
@pytest.fixture
def subscription_delete_event_dict():
    return {'id': 'evt_1PVm1GL1MLd6bigCoqQjk6zQ', 'object': 'event', 'api_version': '2022-11-15', 'created': 1719370537,
            'data': {'object': {'id': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'object': 'subscription',
                                'application': 'ca_EEtbhRJHFK2etIhjyxcqXqBw3Ck05bKK', 'application_fee_percent': None,
                                'automatic_tax': {'enabled': False, 'liability': None},
                                'billing_cycle_anchor': 1719370533,
                                'billing_cycle_anchor_config': None, 'billing_thresholds': None, 'cancel_at': None,
                                'cancel_at_period_end': False, 'canceled_at': None,
                                'cancellation_details': {'comment': None, 'feedback': None, 'reason': None},
                                'collection_method': 'charge_automatically', 'created': 1719370533, 'currency': 'usd',
                                'current_period_end': 1721962533, 'current_period_start': 1719370533,
                                'customer': 'cus_QMV1TWElciMIsp', 'days_until_due': None,
                                'default_payment_method': 'pm_1PVm1AL1MLd6bigCRlSbSUHf', 'default_source': None,
                                'default_tax_rates': [], 'description': None, 'discount': None, 'discounts': [],
                                'ended_at': None,
                                'invoice_settings': {'account_tax_ids': None, 'issuer': {'type': 'self'}},
                                'items': {'object': 'list', 'data': [
                                    {'id': 'si_QMV1IuZHIUIeZT', 'object': 'subscription_item',
                                     'billing_thresholds': None,
                                     'created': 1719370534, 'discounts': [], 'metadata': {},
                                     'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                              'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                              'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                              'interval': 'month', 'interval_count': 1, 'livemode': False,
                                              'metadata': {},
                                              'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                              'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                              'usage_type': 'licensed'},
                                     'price': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'price',
                                               'active': True,
                                               'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                               'custom_unit_amount': None, 'livemode': False, 'lookup_key': None,
                                               'metadata': {}, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                               'recurring': {'aggregate_usage': None, 'interval': 'month',
                                                             'interval_count': 1, 'meter': None,
                                                             'trial_period_days': None,
                                                             'usage_type': 'licensed'}, 'tax_behavior': 'exclusive',
                                               'tiers_mode': None, 'transform_quantity': None, 'type': 'recurring',
                                               'unit_amount': 100, 'unit_amount_decimal': '100'}, 'quantity': 987,
                                     'subscription': 'sub_1PVm1CL1MLd6bigCoJNJkhJi', 'tax_rates': []}],
                                          'has_more': False,
                                          'total_count': 1,
                                          'url': '/v1/subscription_items?subscription=sub_1PVm1CL1MLd6bigCoJNJkhJi'},
                                'latest_invoice': 'in_1PVm1CL1MLd6bigCx2nkQ8lL', 'livemode': False, 'metadata': {
                    'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 343927769'},
                                'next_pending_invoice_item_invoice': None, 'on_behalf_of': None,
                                'pause_collection': None,
                                'payment_settings': {'payment_method_options': None, 'payment_method_types': None,
                                                     'save_default_payment_method': 'off'},
                                'pending_invoice_item_interval': None, 'pending_setup_intent': None,
                                'pending_update': None,
                                'plan': {'id': 'price_1OxZPCL1MLd6bigCglyGWwz9', 'object': 'plan', 'active': True,
                                         'aggregate_usage': None, 'amount': 100, 'amount_decimal': '100',
                                         'billing_scheme': 'per_unit', 'created': 1711218898, 'currency': 'usd',
                                         'interval': 'month', 'interval_count': 1, 'livemode': False, 'metadata': {},
                                         'meter': None, 'nickname': None, 'product': 'prod_Pn9imCT8L9sSWq',
                                         'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None,
                                         'usage_type': 'licensed'}, 'quantity': 987, 'schedule': None,
                                'start_date': 1719370533, 'status': 'active', 'test_clock': None, 'transfer_data': None,
                                'trial_end': None,
                                'trial_settings': {'end_behavior': {'missing_payment_method': 'create_invoice'}},
                                'trial_start': None}, 'previous_attributes': {'status': 'incomplete'}},
            'livemode': False,
            'pending_webhooks': 1,
            'request': {'id': 'req_37pTMnB2c23SCI', 'idempotency_key': 'e4a69b4e-d993-4a85-9dab-061028dd3245'},
            'type': 'customer.subscription.updated'}
