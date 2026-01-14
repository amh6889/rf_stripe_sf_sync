import json

import pytest
from mock.mock import MagicMock


@pytest.fixture
def mocked_donor_mapper(donor_with_no_metadata_address_dict):
    mapped_donor = {'FirstName': 'Bill', 'LastName': 'Nye', 'npe01__HomeEmail__c': 'bill_nye_test@gmail.com',
                    'Email': 'bill_nye_test@gmail.com', 'MailingStreet': '901 Alum Springs Rd', 'MailingCity': 'Forest',
                    'MailingState': 'VA', 'MailingPostalCode': '24551', 'MailingCountry': None, 'Phone': None,
                    'npe01__Preferred_Email__c': 'Personal', 'External_Contact_ID__c': '12345',
                    'HasOptedOutOfEmail': True, 'DoNotMail__c': True}
    mocked_mapper = MagicMock()
    mocked_mapper.map_donor_create_event.return_value = mapped_donor
    return mocked_mapper


@pytest.fixture
def mocked_stripe_donor_service():
    mocked_stripe_donor_service = MagicMock()
    mocked_stripe_donor_service.update.return_value = {'success': True}
    return mocked_stripe_donor_service


@pytest.fixture
def mocked_salesforce_donor_service():
    mocked_salesforce_donor_service = MagicMock()
    mocked_salesforce_donor_service.get_contact_id.return_value = '12345'
    return mocked_salesforce_donor_service


@pytest.fixture
def donor_with_no_metadata_address_dict():
    return {"id": "evt_1PEO5DL1MLd6bigCDF2VzSU9",
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
            }


@pytest.fixture
def donor_with_metadata_address_dict():
    return {
        'id': 'evt_1PEO5DL1MLd6bigCDF2VzSU9',
        'object': 'event',
        'api_version': '2022-11-15',
        'created': 1715226951,
        'data': {
            'object': {
                'id': 'cus_Q4X90EUjCmX1wg',
                'object': 'customer',
                'address': None,
                'balance': 0,
                'created': 1715226950,
                'currency': None,
                'default_source': None,
                'delinquent': False,
                'description': 'Turd Ferguson',
                'discount': None,
                'email': 'turdfergusion_test@gmail.com',
                'invoice_prefix': 'D7DBC775',
                'invoice_settings': {
                    'custom_fields': None,
                    'default_payment_method': None,
                    'footer': None,
                    'rendering_options': None
                },
                'livemode': False,
                'metadata': {
                    'address_city': 'Forest',
                    'address_country': 'United States',
                    'address_state': 'VA',
                    'address_street': '4554 Thomas Jefferson Rd',
                    'address_zip': '24551',
                    'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 338201953'
                },
                'name': None,
                'next_invoice_sequence': 1,
                'phone': None,
                'preferred_locales': [],
                'shipping': None,
                'tax_exempt': 'none',
                'test_clock': None
            }
        },
        'livemode': False,
        'pending_webhooks': 0,
        'request': {
            'id': 'req_HBIEFtTW7obdZg',
            'idempotency_key': 'f50dbd10-e465-4ea7-8127-349017a174cd'
        },
        'type': 'customer.created'
    }


@pytest.fixture
def donor_with_address_dict():
    return {'id': 'evt_1OnOgxL1MLd6bigCjQVt4aC3',
            'data': {
                'object': {
                    'id': 'cus_PcdyPDFvTFM1gP',
                    'name': 'Ted Hunt Mendoza',
                    'email': 'testemail99@gmail.com',
                    'phone': '+14347280720',
                    'object': 'customer',
                    'address': {
                        'city': 'Lynchburg',
                        'line1': '406 Stonemill Dr',
                        'line2': 'Apt I',
                        'state': 'VA',
                        'country': 'US',
                        'postal_code': '24502'
                    },
                    'balance': 0,
                    'created': 1708794435,
                    'currency': None,
                    'discount': None,
                    'livemode': False,
                    'metadata': {},
                    'shipping': {
                        'name': 'Stripe Test',
                        'phone': '+14347280720',
                        'address': {
                            'city': 'Lynchburg',
                            'line1': '406 Stonemill Dr',
                            'line2': 'Apt I',
                            'state': 'VA',
                            'country': 'US',
                            'postal_code': '24502'
                        }
                    },
                    'delinquent': False,
                    'tax_exempt': 'none',
                    'test_clock': None,
                    'description': 'test',
                    'default_source': None,
                    'invoice_prefix': 'D324F091',
                    'invoice_settings': {
                        'footer': None,
                        'custom_fields': None,
                        'rendering_options': None,
                        'default_payment_method': None
                    },
                    'preferred_locales': [],
                    'next_invoice_sequence': 1
                }
            },
            'type': 'customer.created',
            'object': 'event',
            'created': 1708794435,
            'request': {
                'id': 'req_qMdC5zjrtB9Y2a',
                'idempotency_key': '044342a2-7dbc-4107-93eb-db064bb76ee6'
            },
            'livemode': False,
            'api_version': '2022-11-15',
            'pending_webhooks': 3
            }


@pytest.fixture
def donor_with_address_line2_missing():
    return {'id': 'evt_1PcrJEL1MLd6bigCdNbs220i',
            'object': 'event', 'api_version': '2022-11-15', 'created': 1721059168,
            'data':
                {'object':
                     {'id': 'cus_QToxMZVIxZRAtF', 'object': 'customer',
                      'address': {'city': 'Alajuela', 'country': 'Costa Rica', 'line1': 'Av. 0AS, Calle 42',
                                  'line2': None, 'postal_code': '20102', 'state': 'Alajuela'},
                      'balance': 0, 'created': 1721059167, 'currency': None, 'default_source': None,
                      'delinquent': False,
                      'description': 'VISA', 'discount': None, 'email': 'allansr20@gmail.com',
                      'invoice_prefix': '341086FB',
                      'invoice_settings': {'custom_fields': None,
                                           'default_payment_method': 'pm_1PcrJCL1MLd6bigCldfpPEmT',
                                           'footer': None, 'rendering_options': None}, 'livemode': False,
                      'metadata': {
                          'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 346524701',
                          'address_street': 'Av. 0AS, Calle 42', 'address_country': 'Costa Rica',
                          'address_state': 'Alajuela', 'address_zip': '20102', 'address_city': 'Alajuela'},
                      'name': 'VISA', 'next_invoice_sequence': 1,
                      'phone': None, 'preferred_locales': [], 'shipping': None, 'tax_exempt': 'none',
                      'test_clock': None},
                 'previous_attributes': {'address': None, 'name': None}}, 'livemode': False,
            'pending_webhooks': 1,
            'request': {'id': 'req_p3B9ZYNOmcXQcC',
                        'idempotency_key': '4e0dc179-d7fd-468a-bcf1-4b24df489497'},
            'type': 'customer.updated'}


@pytest.fixture
def donor_with_metadata_name():
    return {'id': 'evt_1PcrJEL1MLd6bigCdNbs220i', 'object': 'event', 'api_version': '2022-11-15', 'created': 1721059168,
            'data': {'object':
                         {'id': 'cus_QToxMZVIxZRAtF', 'object': 'customer',
                          'address': {'city': 'Alajuela', 'country': 'Costa Rica',
                                      'line1': 'Av. 0AS, Calle 42',
                                      'line2': None, 'postal_code': '20102', 'state': 'Alajuela'},
                          'balance': 0, 'created': 1721059167, 'currency': None, 'default_source': None,
                          'delinquent': False,
                          'description': 'VISA', 'discount': None, 'email': 'allansr20@gmail.com',
                          'invoice_prefix': '341086FB',
                          'invoice_settings': {'custom_fields': None,
                                               'default_payment_method': 'pm_1PcrJCL1MLd6bigCldfpPEmT',
                                               'footer': None, 'rendering_options': None}, 'livemode': False,
                          'metadata': {
                              'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / '
                                            'Resp. 346524701',
                              'address_street': 'Av. 0AS, Calle 42', 'address_country': 'Costa Rica',
                              'address_state': 'Alajuela', 'address_zip': '20102',
                              'address_city': 'Alajuela',
                              'first_name': 'Allan', 'last_name': 'Sanchez'},
                          'name': None, 'next_invoice_sequence': 1,
                          'phone': None, 'preferred_locales': [], 'shipping': None, 'tax_exempt': 'none',
                          'test_clock': None},
                     'previous_attributes': {'address': None, 'name': None}}, 'livemode': False,
            'pending_webhooks': 1,
            'request': {'id': 'req_p3B9ZYNOmcXQcC',
                        'idempotency_key': '4e0dc179-d7fd-468a-bcf1-4b24df489497'},
            'type': 'customer.updated'}


@pytest.fixture
def donor_with_metadata_opt_out():
    return {
        'id': 'evt_1PdlYsL1MLd6bigCYMOA3AWK',
        'object': 'event',
        'api_version': '2022-11-15',
        'created': 1721275402,
        'data': {
            'object': {
                'id': 'cus_QUl5PhyHKkQnDC',
                'object': 'customer',
                'address': None,
                'balance': 0,
                'created': 1721275402,
                'currency': None,
                'default_source': None,
                'delinquent': False,
                'description': 'bill nye',
                'discount': None,
                'email': 'bill_nye_test@gmail.com',
                'invoice_prefix': 'FC900036',
                'invoice_settings': {
                    'custom_fields': None,
                    'default_payment_method': None,
                    'footer': None,
                    'rendering_options': None
                },
                'livemode': False,
                'metadata': {
                    'address_city': 'Forest',
                    'address_state': 'VA',
                    'address_street': '901 Alum Springs Rd',
                    'address_zip': '24551',
                    'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 346959583',
                    'first_name': 'Bill',
                    'last_name': 'Nye',
                    'opt_out': '3',
                    'receipt': 'Email + Mail'
                },
                'name': None,
                'next_invoice_sequence': 1,
                'phone': None,
                'preferred_locales': [],
                'shipping': None,
                'tax_exempt': 'none',
                'test_clock': None
            }
        },
        'livemode': False,
        'pending_webhooks': 0,
        'request': {
            'id': 'req_VZQppRgbx88RxI',
            'idempotency_key': '249f4f31-5632-448c-bd9e-7fd9279ae4d3'
        },
        'type': 'customer.created'
    }


@pytest.fixture
def donor_with_metadata_receipt():
    return {
        'id': 'evt_1PdlYsL1MLd6bigCYMOA3AWK',
        'object': 'event',
        'api_version': '2022-11-15',
        'created': 1721275402,
        'data': {
            'object': {
                'id': 'cus_QUl5PhyHKkQnDC',
                'object': 'customer',
                'address': None,
                'balance': 0,
                'created': 1721275402,
                'currency': None,
                'default_source': None,
                'delinquent': False,
                'description': 'bill nye',
                'discount': None,
                'email': 'bill_nye_test@gmail.com',
                'invoice_prefix': 'FC900036',
                'invoice_settings': {
                    'custom_fields': None,
                    'default_payment_method': None,
                    'footer': None,
                    'rendering_options': None
                },
                'livemode': False,
                'metadata': {
                    'address_city': 'Forest',
                    'address_state': 'VA',
                    'address_street': '901 Alum Springs Rd',
                    'address_zip': '24551',
                    'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 346959583',
                    'first_name': 'Bill',
                    'last_name': 'Nye',
                    'receipt': 'Email + Mail'
                },
                'name': None,
                'next_invoice_sequence': 1,
                'phone': None,
                'preferred_locales': [],
                'shipping': None,
                'tax_exempt': 'none',
                'test_clock': None
            }
        },
        'livemode': False,
        'pending_webhooks': 0,
        'request': {
            'id': 'req_VZQppRgbx88RxI',
            'idempotency_key': '249f4f31-5632-448c-bd9e-7fd9279ae4d3'
        },
        'type': 'customer.created'
    }


@pytest.fixture
def donor_update_error_3_12_25():
    return {
        'id': 'evt_1R1oL1L1MLd6bigCUBGKkaca',
        'object': 'event',
        'api_version': '2022-11-15',
        'created': 1741782283,
        'data': {
            'object':
                {'id': 'cus_RvfgDCi6Rjqhdq',
                 'object': 'customer',
                 'address': None,
                 'balance': 0,
                 'created': 1741782282,
                 'currency': None,
                 'default_source': None,
                 'delinquent': False,
                  'description': 'Matthew D Mahar',
                 'discount': None,
                 'email': 'savedsynner@gmail.com',
                  'invoice_prefix': 'DEE3D8A5',
                 'invoice_settings':
                     {
                        'custom_fields': None,
                        'default_payment_method': 'pm_1R1oKzL1MLd6bigCymTqlErd',
                        'footer': None,
                       ' rendering_options': None
                     },
                 'livemode': True,
                  'metadata':
                     {
                        'last_name': 'Mahar',
                        'address_street': '4201 Ware Neck Dr',
                        'receipt': 'Email',
                        'first_name': 'Matthew',
                        'address_country': 'United States',
                        'address_state': 'VA',
                        'created_by': 'FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 372170210',
                        'address_zip': '23456', 'address_city': 'Virginia Beach'
                     },
                 'name': None,
                 'next_invoice_sequence': 1,
                 'phone': None, 'preferred_locales': [],
                 'shipping': None,
                'tax_exempt': 'none', 'test_clock': None},
                 'previous_attributes': {'invoice_settings': {'default_payment_method': None}}}, 'livemode': True,
        'pending_webhooks': 1,
        'request': {'id': 'req_pD12zy59OhDs4e', 'idempotency_key': '86c41d96-44b4-41e0-9e99-b0c60e47775f'},
        'type': 'customer.updated'}

@pytest.fixture
def donor_no_last_name():
    return {
    "id": "evt_1SR7BgL1MLd6bigCG5D379o9",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1762589276,
    "data": {
        "object": {
            "id": "cus_TNsxY7VBzTW7JX",
            "object": "customer",
            "address": None,
            "balance": 0,
            "created": 1762589276,
            "currency": None,
            "default_source": None,
            "delinquent": False,
            "description": "Hayden Frizzell",
            "discount": None,
            "email": "logicalbiblestudy@gmail.com",
            "invoice_prefix": "6TBW3XP0",
            "invoice_settings": {
                "custom_fields": None,
                "default_payment_method": None,
                "footer": None,
                "rendering_options": None,
            },
            "livemode": True,
            "metadata": {
                "opt_out": "2",
                "address_street": "7 Vickers Street",
                "address_country": "Australia",
                "first_name": "Logical Bible Study",
                "address_state": "Victoria",
                "receipt": "Email",
                "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 390040058",
                "address_zip": "3631",
                "address_city": "Kialla",
            },
            "name": None,
            "next_invoice_sequence": 1,
            "phone": None,
            "preferred_locales": [],
            "shipping": None,
            "tax_exempt": "none",
            "test_clock": None,
        }
    },
    "livemode": True,
    "pending_webhooks": 1,
    "request": {
        "id": "req_Ntvp8TpBx2skYZ",
        "idempotency_key": "d176624d-3657-4dad-b474-128802d142d3",
    },
    "type": "customer.created",
}



@pytest.fixture
def json_10_26_25_error():
    return {
    "id": "evt_1SMWFGL1MLd6bigCRjpuN7Gw",
    "object": "event",
    "api_version": "2022-11-15",
    "created": 1761493957,
    "data": {
        "object": {
            "id": "cus_TJ8WFWUi0mIQm4",
            "object": "customer",
            "address": None,
            "balance": 0,
            "created": 1761493956,
            "currency": None,
            "default_source": None,
            "delinquent": False,
            "description": "Aaron N Miller",
            "discount": None,
            "email": "aaronneilmiller80@gmail.com",
            "invoice_prefix": "M7DMKGGA",
            "invoice_settings": {
                "custom_fields": None,
                "default_payment_method": "pm_1SMWFDL1MLd6bigC3wnshzPE",
                "footer": None,
                "rendering_options": None,
            },
            "livemode": True,
            "metadata": {
                "address_street": "234 Brookfield Rd",
                "receipt": "Email",
                "first_name": "Aaron",
                "address_state": "OH",
                "address_country": "United States",
                "created_by": "FormAssembly - Stripe - Reference: Form 5120065 / Conn. 762535 / Resp. 389163993",
                "address_zip": "44012",
                "address_city": "Avon Lake",
                "last_name": "Miller",
            },
            "name": None,
            "next_invoice_sequence": 1,
            "phone": None,
            "preferred_locales": [],
            "shipping": None,
            "tax_exempt": "none",
            "test_clock": None,
        },
        "previous_attributes": {"invoice_settings": {"default_payment_method": None}},
    },
    "livemode": True,
    "pending_webhooks": 1,
    "request": {
        "id": "req_iEr35xQKg46WFU",
        "idempotency_key": "19329c45-2494-4efd-a2d7-6617ab1d6c0b",
    },
    "type": "customer.updated",
}

