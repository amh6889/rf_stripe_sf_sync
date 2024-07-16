import json

import pytest

@pytest.fixture
def donor_with_no_metadata_address_json():
    return json.dumps({
    "id": "evt_1PEO5DL1MLd6bigCDF2VzSU9",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1715226951,
    "data": {
        "object": {
            "id": "cus_Q4X90EUjCmX1wg",
            "object": "customer",
            "address": None,
            "balance": 0,
            "created": 1715226950,
            "currency": None,
            "default_source": None,
            "delinquent": False,
            "description": "Turd Ferguson",
            "discount": None,
            "email": "turdfergusion_test@gmail.com",
            "invoice_prefix": "D7DBC775",
            "invoice_settings": {
                "custom_fields": None,
                "default_payment_method": None,
                "footer": None,
                "rendering_options": None
            },
            "livemode": False,
            "metadata": {
                "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 338201953"
            },
            "name": None,
            "next_invoice_sequence": 1,
            "phone": None,
            "preferred_locales": [],
            "shipping": None,
            "tax_exempt": "none",
            "test_clock": None
        }
    },
    "livemode": False,
    "pending_webhooks": 0,
    "request": {
        "id": "req_HBIEFtTW7obdZg",
        "idempotency_key": "f50dbd10-e465-4ea7-8127-349017a174cd"
    },
    "type": "customer.created"
})

@pytest.fixture
def donor_with_metadata_address_json():
    return json.dumps({
    "id": "evt_1PEO5DL1MLd6bigCDF2VzSU9",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1715226951,
    "data": {
        "object": {
            "id": "cus_Q4X90EUjCmX1wg",
            "object": "customer",
            "address": None,
            "balance": 0,
            "created": 1715226950,
            "currency": None,
            "default_source": None,
            "delinquent": False,
            "description": "Turd Ferguson",
            "discount": None,
            "email": "turdfergusion_test@gmail.com",
            "invoice_prefix": "D7DBC775",
            "invoice_settings": {
                "custom_fields": None,
                "default_payment_method": None,
                "footer": None,
                "rendering_options": None
            },
            "livemode": False,
            "metadata": {
                "address_city": "Forest",
                "address_country": "United States",
                "address_state": "VA",
                "address_street": "4554 Thomas Jefferson Rd",
                "address_zip": "24551",
                "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 338201953"
            },
            "name": None,
            "next_invoice_sequence": 1,
            "phone": None,
            "preferred_locales": [],
            "shipping": None,
            "tax_exempt": "none",
            "test_clock": None
        }
    },
    "livemode": False,
    "pending_webhooks": 0,
    "request": {
        "id": "req_HBIEFtTW7obdZg",
        "idempotency_key": "f50dbd10-e465-4ea7-8127-349017a174cd"
    },
    "type": "customer.created"
})

@pytest.fixture
def donor_with_address_json():
    return json.dumps({"id": "evt_1OnOgxL1MLd6bigCjQVt4aC3",
                       "data": {
                           "object": {
                               "id": "cus_PcdyPDFvTFM1gP",
                               "name": "Ted Hunt Mendoza",
                               "email": "testemail99@gmail.com",
                               "phone": "+14347280720",
                               "object": "customer",
                               "address": {
                                   "city": "Lynchburg",
                                   "line1": "406 Stonemill Dr",
                                   "line2": "Apt I",
                                   "state": "VA",
                                   "country": "US",
                                   "postal_code": "24502"
                               },
                               "balance": 0,
                               "created": 1708794435,
                               "currency": None,
                               "discount": None,
                               "livemode": False,
                               "metadata": {},
                               "shipping": {
                                   "name": "Stripe Test",
                                   "phone": "+14347280720",
                                   "address": {
                                       "city": "Lynchburg",
                                       "line1": "406 Stonemill Dr",
                                       "line2": "Apt I",
                                       "state": "VA",
                                       "country": "US",
                                       "postal_code": "24502"
                                   }
                               },
                               "delinquent": False,
                               "tax_exempt": "none",
                               "test_clock": None,
                               "description": "test",
                               "default_source": None,
                               "invoice_prefix": "D324F091",
                               "invoice_settings": {
                                   "footer": None,
                                   "custom_fields": None,
                                   "rendering_options": None,
                                   "default_payment_method": None
                               },
                               "preferred_locales": [],
                               "next_invoice_sequence": 1
                           }
                       },
                       "type": "customer.created",
                       "object": "event",
                       "created": 1708794435,
                       "request": {
                           "id": "req_qMdC5zjrtB9Y2a",
                           "idempotency_key": "044342a2-7dbc-4107-93eb-db064bb76ee6"
                       },
                       "livemode": False,
                       "api_version": "2022-11-15",
                       "pending_webhooks": 3
                       })

@pytest.fixture
def donor_that_erred_during_uat():
    return json.dumps({'id': 'evt_1PcrJEL1MLd6bigCdNbs220i', 'object': 'event', 'api_version': '2022-11-15', 'created': 1721059168, 'data': {'object': {'id': 'cus_QToxMZVIxZRAtF', 'object': 'customer', 'address': {'city': 'Alajuela', 'country': 'Costa Rica', 'line1': 'Av. 0AS, Calle 42', 'line2': None, 'postal_code': '20102', 'state': 'Alajuela'}, 'balance': 0, 'created': 1721059167, 'currency': None, 'default_source': None, 'delinquent': False, 'description': 'VISA', 'discount': None, 'email': 'allansr20@gmail.com', 'invoice_prefix': '341086FB', 'invoice_settings': {'custom_fields': None, 'default_payment_method': 'pm_1PcrJCL1MLd6bigCldfpPEmT', 'footer': None, 'rendering_options': None}, 'livemode': False, 'metadata': {'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 346524701', 'address_street': 'Av. 0AS, Calle 42', 'address_country': 'Costa Rica', 'address_state': 'Alajuela', 'address_zip': '20102', 'address_city': 'Alajuela'}, 'name': 'VISA', 'next_invoice_sequence': 1, 'phone': None, 'preferred_locales': [], 'shipping': None, 'tax_exempt': 'none', 'test_clock': None}, 'previous_attributes': {'address': None, 'name': None}}, 'livemode': False, 'pending_webhooks': 1, 'request': {'id': 'req_p3B9ZYNOmcXQcC', 'idempotency_key': '4e0dc179-d7fd-468a-bcf1-4b24df489497'}, 'type': 'customer.updated'})
    _