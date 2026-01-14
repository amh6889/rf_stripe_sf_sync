


def get_donor_opt_out(data):
    opt_out = {'email_opt_out': False, 'mail_opt_out': False}
    if metadata := data.get('metadata'):
        if opt_out_number := metadata.get('opt_out'):
            match opt_out_number:
                case '1':
                    opt_out['email_opt_out'] = True
                case '2':
                    opt_out['mail_opt_out'] = True
                case '3':
                    opt_out['email_opt_out'] = True
                    opt_out['mail_opt_out'] = True
                case _:
                    print(f'Unknown donor opt out number: {opt_out_number}')
    return opt_out


def get_donor_receipt_preference(data):
    default_receipt_preference = 'Email'
    receipt_preference = data['metadata']['receipt'] if data['metadata'] and 'receipt' in data[
        'metadata'] else default_receipt_preference
    return receipt_preference


def get_donor_address(data):
    donor_address = {'city': None, 'state': None, 'line1': None, 'country': None, 'postal_code': None}
    if address := data.get('address'):
        donor_address['city'] = address.get('city')
        donor_address['state'] = address.get('state')
        donor_address['line1'] = address.get('line1')
        if 'line2' in address and address['line2']:
            donor_address['line1'] = donor_address.get('line1') + ' ' + address.get('line2')
        donor_address['country'] = address.get('country')
        donor_address['postal_code'] = address.get('postal_code')
    elif metadata := data.get('metadata'):
        donor_address['city'] = metadata.get('address_city')
        donor_address['line1'] = metadata.get('address_street')
        donor_address['state'] = metadata.get('address_state')
        donor_address['country'] = metadata.get('address_country')
        donor_address['postal_code'] = metadata.get('address_zip')
    return donor_address


def get_first_and_last_name(full_name):
    names = full_name.split()
    first_name = names[0]
    del names[0]
    last_name = ' '.join(names) if names else 'N/A'
    return first_name, last_name


def get_donor_name(data):
    donor_name = {'first_name': None, 'last_name': None}
    if metadata := data.get('metadata'):
        donor_name['first_name'] = metadata.get('first_name')
        donor_name['last_name'] = metadata.get('last_name')
    if donor_name['first_name'] and not donor_name.get('last_name'):
        full_name = data.get('description')
        first_name, last_name = get_first_and_last_name(full_name)
        donor_name['first_name'] = first_name
        donor_name['last_name'] = last_name
    if not donor_name['first_name'] and not donor_name['last_name']:
        full_name = data.get('description')
        first_name, last_name = get_first_and_last_name(full_name)
        donor_name['first_name'] = first_name
        donor_name['last_name'] = last_name
    return donor_name


def filter_donor(donor):
    filtered_donor = {k: v for k, v in donor.items() if v is not None}
    return filtered_donor


class DonorMapper:

    def map_create_event(self, event_data):
        data = event_data['data']['object']
        full_name = data.get('name')
        updates = {}

        if not full_name:
            donor_names = get_donor_name(data)
            first_name = donor_names.get('first_name')
            last_name = donor_names.get('last_name')
            updates['name'] = first_name + ' ' + last_name
        else:
            first_name, last_name = get_first_and_last_name(full_name)

        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        donor_address = get_donor_address(data)
        opt_out = get_donor_opt_out(data)
        receipt_preference = get_donor_receipt_preference(data)
        if not address:
            updates['address'] = donor_address

        if updates:
            updates['id'] = data.get('id')

        donor = {'FirstName': first_name,
                 'LastName': last_name,
                 'npe01__HomeEmail__c': email,
                 'Email': email,
                 'Phone': phone,
                 'MailingStreet': donor_address.get('line1'),
                 'MailingState': donor_address.get('state'),
                 'MailingCity': donor_address.get('city'),
                 'MailingCountry': donor_address.get('country'),
                 'MailingPostalCode': donor_address.get('postal_code'),
                 'npe01__Preferred_Email__c': 'Personal',
                 'Stripe_Donor__c': True,
                 'ReceiptDelivery__c': receipt_preference,
                 'HasOptedOutOfEmail': opt_out.get('email_opt_out'),
                 'DoNotMail__c': opt_out.get('mail_opt_out'),
                 'stripe_updates': updates}
        return donor

    def map_update_event(self, event_data):
        data = event_data['data']['object']
        full_name = data.get('name')
        stripe_updates = {}
        if not full_name:
            donor_names = get_donor_name(data)
            first_name = donor_names.get('first_name')
            last_name = donor_names.get('last_name')
            stripe_updates['name'] = first_name + ' ' + last_name
        else:
            first_name, last_name = get_first_and_last_name(full_name)

        donor_address = get_donor_address(data)
        address = data.get('address')
        if not address:
            stripe_updates['address'] = donor_address

        if stripe_updates:
            stripe_updates['id'] = data.get('id')

        donor = {'FirstName': first_name,
                 'LastName': last_name,
                 'npe01__HomeEmail__c': data.get('email'),
                 'Stripe_Donor__c': True,
                 'Email': data.get('email'),
                 'Phone': data.get('phone'),
                 'MailingStreet': donor_address.get('line1'),
                 'MailingState': donor_address.get('state'),
                 'MailingCity': donor_address.get('city'),
                 'MailingCountry': donor_address.get('country'),
                 'MailingPostalCode': donor_address.get('postal_code'),
                 'stripe_updates': stripe_updates
                 }
        filtered_donor = filter_donor(donor)
        return filtered_donor


