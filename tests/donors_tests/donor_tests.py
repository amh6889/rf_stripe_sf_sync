import json

from donors.donor import Donor
from donors.donor_processor import DonorProcessor


def test_donor_does_not_exist():
    email = 'sometestemail@gmail.com'
    exists = Donor.exists(email)
    assert exists is None


def test_donor_exist():
    email = 'acat@tx.rr.com'
    donor = Donor.exists(email)
    assert donor is not None


def test_create_donor_succeeds():
    donor = {'FirstName': 'Melinda', 'LastName': 'Trump', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail9998@gmail.com',
             'Email': 'testemail9998@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True,
             "MailingStreet": "5668 Lilac Blossom Lane", "MailingCity": "San Jose", "MailingState": "CA",
             "MailingCountry": "United States",
             "MailingPostalCode": "95124"}
    response = Donor.create(**donor)
    assert response.get('success') is True


def test_create_donor_errors():
    donor = {'FirstName': 'Melinda', 'LastName': 'Trump', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail9999@gmail.com',
             'Email': 'testemail9999@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True,
             "MailingStreet": "5668 Lilac Blossom Lane", "MailingCity": "San Jose", "MailingState": "CA",
             "MailingCountry": "United States",
             "MailingPostalCode": "95124"}
    response = Donor.create(**donor)
    assert response.get('success') is False


def test_update_donor_succeeds():
    donor = {'FirstName': 'Ted', 'LastName': 'Turner', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail99@gmail.com',
             'Email': 'testemail99@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
    sf_contact_id = '003Ox00000Acq6HIAR'
    response = Donor.update(sf_contact_id, **donor)
    assert response is 204


def test_update_donor_errors():
    donor = {'FirstName': 'Ted', 'LastName': 'Turner', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail99@gmail.com',
             'Email': 'testemail99@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
    sf_contact_id = '003Ox00000Acq6HIAX'
    response = Donor.update(sf_contact_id, **donor)
    assert response is not 204


def test_donor_processor_maps_works():
    donor_event = """
  {"id": "evt_1OnOgxL1MLd6bigCjQVt4aC3",
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
      "currency": null,
      "discount": null,
      "livemode": false,
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
      "delinquent": false,
      "tax_exempt": "none",
      "test_clock": null,
      "description": "test",
      "default_source": null,
      "invoice_prefix": "D324F091",
      "invoice_settings": {
        "footer": null,
        "custom_fields": null,
        "rendering_options": null,
        "default_payment_method": null
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
  "livemode": false,
  "api_version": "2022-11-15",
  "pending_webhooks": 3
}
"""
    donor = json.loads(donor_event)
    mapped_donor = DonorProcessor._map_donor(**donor)
    assert mapped_donor['FirstName'] == 'Ted'
    assert mapped_donor['LastName'] == 'Hunt Mendoza'
    assert mapped_donor['npe01__HomeEmail__c'] == 'testemail99@gmail.com'
    assert mapped_donor['Email'] == 'testemail99@gmail.com'
    assert mapped_donor['MailingStreet'] == '406 Stonemill Dr Apt I'
    assert mapped_donor['MailingCity'] == 'Lynchburg'
    assert mapped_donor['MailingState'] == 'VA'
    assert mapped_donor['MailingPostalCode'] == '24502'
    assert mapped_donor['MailingCountry'] == 'US'
    assert mapped_donor['Phone'] == '+14347280720'
    assert mapped_donor['npe01__Preferred_Email__c'] == 'Personal'
    assert mapped_donor['External_Contact_ID__c'] == 'cus_PcdyPDFvTFM1gP'


def test_parse_name_two_names_works():
    full_name = 'Billy Bob'
    first_name, last_name = DonorProcessor._parse_name(full_name)
    print(first_name)
    assert first_name == 'Billy'
    assert last_name == 'Bob'


def test_parse_name_three_names_works():
    full_name = 'Billy Bob Thumb'
    first_name, last_name = DonorProcessor._parse_name(full_name)
    assert first_name == 'Billy'
    assert last_name == 'Bob Thumb'


def test_parse_name_four_names_works():
    full_name = 'Wing Pong Robert Luk'
    first_name, last_name = DonorProcessor._parse_name(full_name)
    assert first_name == 'Wing'
    assert last_name == 'Pong Robert Luk'

def test_get_email_works():
    stripe_customer_id = 'cus_PjBU4vGjx2wr3I'
    email = Donor.get_email(stripe_customer_id)
    assert email is not None
    assert email == 'thisisatestemailhomey@gmail.com'