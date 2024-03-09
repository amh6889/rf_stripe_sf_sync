from donors.process_customer_create_event import process_customer_create_event


def test_process_customer_create_event():
    event = {'event_type': 'customer.created',
             'event_data': '{"id": "evt_1OnOgxL1MLd6bigCjQVt4aC3", "data": {"object": {"id": "cus_PcdyPDFvTFM1gP", '
                           '"name": "Stripe Test", "email": "testemail@gmail.com", "phone": "+14347280720", '
                           '"object": "customer", "address": {"city": "Lynchburg", "line1": "406 Stonemill Dr", '
                           '"line2": "Apt I", "state": "VA", "country": "US", "postal_code": "24502"}, "balance": 0, '
                           '"created": 1708794435, "currency": null, "discount": null, "livemode": false, "metadata": '
                           '{}, "shipping": {"name": "Stripe Test", "phone": "+14347280720", "address": {"city": '
                           '"Lynchburg", "line1": "406 Stonemill Dr", "line2": "Apt I", "state": "VA", "country": '
                           '"US", "postal_code": "24502"}}, "delinquent": false, "tax_exempt": "none", "test_clock": '
                           'null, "description": "test", "default_source": null, "invoice_prefix": "D324F091", '
                           '"invoice_settings": {"footer": null, "custom_fields": null, "rendering_options": null, '
                           '"default_payment_method": null}, "preferred_locales": [], "next_invoice_sequence": 1}}, '
                           '"type": "customer.created", "object": "event", "created": 1708794435, "request": {"id": '
                           '"req_qMdC5zjrtB9Y2a", "idempotency_key": "044342a2-7dbc-4107-93eb-db064bb76ee6"}, '
                           '"livemode": false, "api_version": "2022-11-15", "pending_webhooks": 3}'}
    event_data = event['event_data']
    process_customer_create_event(event_data)
