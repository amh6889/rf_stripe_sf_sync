import json

import pytest

@pytest.fixture
def successful_one_time_donation_dict():
    return {
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
}

@pytest.fixture
def refunded_donation_dict():
    return {
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
}


@pytest.fixture
def successful_subscription_donation_dict():
    return {
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

@pytest.fixture
def donation_failure_event():
    return {
    "id": "evt_1SVaKML1MLd6bigCOWOTj00x",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1763654601,
    "data": {
        "object": {
            "id": "in_1SNxNOL1MLd6bigCOUnMhSMn",
            "object": "invoice",
            "account_country": "US",
            "account_name": "Reasonable Faith, Inc.",
            "account_tax_ids": None,
            "amount_due": 10000,
            "amount_overpaid": 0,
            "amount_paid": 0,
            "amount_remaining": 10000,
            "amount_shipping": 0,
            "application": "ca_EEtbpNfCXuyxRLnevQm4k27P4HUXWUWm",
            "application_fee_amount": None,
            "attempt_count": 5,
            "attempted": True,
            "auto_advance": True,
            "automatic_tax": {
                "disabled_reason": None,
                "enabled": False,
                "liability": None,
                "provider": None,
                "status": None
            },
            "automatically_finalizes_at": None,
            "billing_reason": "subscription_cycle",
            "charge": "ch_3SNyJfL1MLd6bigC1yQKCTZu",
            "collection_method": "charge_automatically",
            "created": 1761836578,
            "currency": "usd",
            "custom_fields": None,
            "customer": "cus_SPJ4p8ZaFZsNNT",
            "customer_address": {
                "city": "PORTERVILLE",
                "country": "United States",
                "line1": "265 N. G Street, Porterville CA, United States",
                "line2": None,
                "postal_code": "93257-3409",
                "state": "ca"
            },
            "customer_email": "jabenas@hotmail.com",
            "customer_name": "John Benas",
            "customer_phone": None,
            "customer_shipping": None,
            "customer_tax_exempt": "none",
            "customer_tax_ids": [],
            "default_payment_method": None,
            "default_source": None,
            "default_tax_rates": [],
            "description": None,
            "discount": None,
            "discounts": [],
            "due_date": None,
            "effective_at": 1761840190,
            "ending_balance": 0,
            "footer": None,
            "from_invoice": None,
            "hosted_invoice_url": "https://invoice.stripe.com/i/acct_1KjcUQL1MLd6bigC/live_YWNjdF8xS2pjVVFMMU1MZDZiaWdDLF9US2NjaEh6V1ZCT3Z0UmZlMWcwaXFsYlNVdmRTMmJtLDE1NDE5NTQwMg0200nBatHBjo?s=ap",
            "invoice_pdf": "https://pay.stripe.com/invoice/acct_1KjcUQL1MLd6bigC/live_YWNjdF8xS2pjVVFMMU1MZDZiaWdDLF9US2NjaEh6V1ZCT3Z0UmZlMWcwaXFsYlNVdmRTMmJtLDE1NDE5NTQwMg0200nBatHBjo/pdf?s=ap",
            "issuer": {
                "type": "self"
            },
            "last_finalization_error": None,
            "latest_revision": None,
            "lines": {
                "object": "list",
                "data": [
                    {
                        "id": "il_1SNxNOL1MLd6bigC9g5Miy1W",
                        "object": "line_item",
                        "amount": 10000,
                        "amount_excluding_tax": 10000,
                        "currency": "usd",
                        "description": "1 × spring_campaign_2025 (at $100.00 / month)",
                        "discount_amounts": [],
                        "discountable": True,
                        "discounts": [],
                        "invoice": "in_1SNxNOL1MLd6bigCOUnMhSMn",
                        "livemode": True,
                        "metadata": {
                            "campaign_code": "C0425",
                            "created_by": "FormAssembly - Stripe Connector - Reference: Form 5172191 / Conn. 827226 / Resp. 378661360"
                        },
                        "parent": {
                            "invoice_item_details": None,
                            "subscription_item_details": {
                                "invoice_item": None,
                                "proration": False,
                                "proration_details": {
                                    "credited_items": None
                                },
                                "subscription": "sub_1RUUSDL1MLd6bigCzQ7YGYM9",
                                "subscription_item": "si_SPJ44WNNASl3gU"
                            },
                            "type": "subscription_item_details"
                        },
                        "period": {
                            "end": 1764514961,
                            "start": 1761836561
                        },
                        "plan": {
                            "id": "price_1R4YqtL1MLd6bigCwuZll9ef",
                            "object": "plan",
                            "active": True,
                            "aggregate_usage": None,
                            "amount": 10000,
                            "amount_decimal": "10000",
                            "billing_scheme": "per_unit",
                            "created": 1742437739,
                            "currency": "usd",
                            "interval": "month",
                            "interval_count": 1,
                            "livemode": True,
                            "metadata": {},
                            "meter": None,
                            "nickname": None,
                            "product": "prod_RyVsi7nNSt1mqK",
                            "tiers_mode": None,
                            "transform_usage": None,
                            "trial_period_days": None,
                            "usage_type": "licensed"
                        },
                        "pretax_credit_amounts": [],
                        "price": {
                            "id": "price_1R4YqtL1MLd6bigCwuZll9ef",
                            "object": "price",
                            "active": True,
                            "billing_scheme": "per_unit",
                            "created": 1742437739,
                            "currency": "usd",
                            "custom_unit_amount": None,
                            "livemode": True,
                            "lookup_key": None,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_RyVsi7nNSt1mqK",
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
                            "unit_amount": 10000,
                            "unit_amount_decimal": "10000"
                        },
                        "pricing": {
                            "price_details": {
                                "price": "price_1R4YqtL1MLd6bigCwuZll9ef",
                                "product": "prod_RyVsi7nNSt1mqK"
                            },
                            "type": "price_details",
                            "unit_amount_decimal": "10000"
                        },
                        "proration": False,
                        "proration_details": {
                            "credited_items": None
                        },
                        "quantity": 1,
                        "subscription": "sub_1RUUSDL1MLd6bigCzQ7YGYM9",
                        "subscription_item": "si_SPJ44WNNASl3gU",
                        "tax_amounts": [],
                        "tax_rates": [],
                        "taxes": [],
                        "type": "subscription",
                        "unit_amount_excluding_tax": "10000"
                    }
                ],
                "has_more": False,
                "total_count": 1,
                "url": "/v1/invoices/in_1SNxNOL1MLd6bigCOUnMhSMn/lines"
            },
            "livemode": True,
            "metadata": {},
            "next_payment_attempt": None,
            "number": "YTZ7MANF-0006",
            "on_behalf_of": None,
            "paid": False,
            "paid_out_of_band": False,
            "parent": {
                "quote_details": None,
                "subscription_details": {
                    "metadata": {
                        "campaign_code": "C0425",
                        "created_by": "FormAssembly - Stripe Connector - Reference: Form 5172191 / Conn. 827226 / Resp. 378661360"
                    },
                    "subscription": "sub_1RUUSDL1MLd6bigCzQ7YGYM9"
                },
                "type": "subscription_details"
            },
            "payment_intent": "pi_3SNyJfL1MLd6bigC1RYuT4XV",
            "payment_settings": {
                "default_mandate": None,
                "payment_method_options": None,
                "payment_method_types": None
            },
            "period_end": 1761836561,
            "period_start": 1759244561,
            "post_payment_credit_notes_amount": 0,
            "pre_payment_credit_notes_amount": 0,
            "quote": None,
            "receipt_number": None,
            "rendering": None,
            "rendering_options": None,
            "shipping_cost": None,
            "shipping_details": None,
            "starting_balance": 0,
            "statement_descriptor": None,
            "status": "open",
            "status_transitions": {
                "finalized_at": 1761840190,
                "marked_uncollectible_at": None,
                "paid_at": None,
                "voided_at": None
            },
            "subscription": "sub_1RUUSDL1MLd6bigCzQ7YGYM9",
            "subscription_details": {
                "metadata": {
                    "campaign_code": "C0425",
                    "created_by": "FormAssembly - Stripe Connector - Reference: Form 5172191 / Conn. 827226 / Resp. 378661360"
                }
            },
            "subtotal": 10000,
            "subtotal_excluding_tax": 10000,
            "tax": None,
            "test_clock": None,
            "total": 10000,
            "total_discount_amounts": [],
            "total_excluding_tax": 10000,
            "total_pretax_credit_amounts": [],
            "total_tax_amounts": [],
            "total_taxes": [],
            "transfer_data": None,
            "webhooks_delivered_at": 1761836578
        }
    },
    "livemode": True,
    "pending_webhooks": 0,
    "request": {
        "id": None,
        "idempotency_key": None
    },
    "type": "invoice.payment_failed"
}