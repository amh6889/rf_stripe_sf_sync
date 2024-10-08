import time
import traceback

from donors.donor import Donor


class DonorProcessor:

    # TODO: change below method to _map_create_donor_event and make new function to map an update donor event
    @staticmethod
    def _map_donor_update_event(**event_data):
        print(event_data)
        data = event_data['data']['object']
        customer_id = data.get('id')
        full_name = data.get('name')
        updates = {}

        if not full_name:
            donor_names = DonorProcessor.get_donor_name(data)
            first_name = donor_names['first_name']
            last_name = donor_names['last_name']
            updates['name'] = first_name + ' ' + last_name
        else:
            first_name, last_name = DonorProcessor._parse_name(full_name)

        address = data['address']
        donor_address = DonorProcessor.get_donor_address(data)
        if not address:
            updates['address'] = donor_address

        if updates:
            Donor.update_stripe_customer(customer_id, updates)

        donor = {'FirstName': first_name, 'LastName': last_name, 'npe01__HomeEmail__c': data.get('email'),
                 'Email': data.get('email'), 'Phone': data.get('phone'), 'MailingStreet': donor_address['line1'],
                 'MailingState': donor_address.get('state'), 'MailingCity': donor_address.get('city'),
                 'MailingCountry': donor_address.get('country'), 'MailingPostalCode': donor_address.get('postal_code')}
        filtered_donor = DonorProcessor._filter_donor(donor)
        return filtered_donor

    @staticmethod
    def _filter_donor(donor):
        filtered_donor = {k: v for k, v in donor.items() if v is not None}
        return filtered_donor

    @staticmethod
    def _map_donor_create_event(**event_data):
        data = event_data['data']['object']
        customer_id = data.get('id')
        full_name = data.get('name')
        updates = {}

        if not full_name:
            donor_names = DonorProcessor.get_donor_name(data)
            first_name = donor_names['first_name']
            last_name = donor_names['last_name']
            updates['name'] = first_name + ' ' + last_name
        else:
            first_name, last_name = DonorProcessor._parse_name(full_name)

        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        donor_address = DonorProcessor.get_donor_address(data)
        opt_out = DonorProcessor.get_donor_opt_out(data)
        receipt_preference = DonorProcessor.get_donor_receipt_preference(data)
        if not address:
            updates['address'] = donor_address

        if updates:
            Donor.update_stripe_customer(customer_id, updates)

        donor = {'FirstName': first_name, 'LastName': last_name,
                 'npe01__HomeEmail__c': email, 'Email': email, 'Phone': phone, 'MailingStreet': donor_address['line1'],
                 'MailingState': donor_address.get('state'), 'MailingCity': donor_address.get('city'),
                 'MailingCountry': donor_address.get('country'), 'MailingPostalCode': donor_address.get('postal_code'),
                 'npe01__Preferred_Email__c': 'Personal', 'Stripe_Donor__c': True,
                 'ReceiptDelivery__c': receipt_preference,
                 'HasOptedOutOfEmail': opt_out.get('email_opt_out'), 'DoNotMail__c': opt_out.get('mail_opt_out')}
        return donor

    @staticmethod
    def get_donor_name(data):
        donor_name = {'first_name': None, 'last_name': None}
        if data['metadata']:
            if 'first_name' in data['metadata'] and data['metadata']['first_name']:
                donor_name['first_name'] = data['metadata']['first_name']

            if 'last_name' in data['metadata'] and data['metadata']['last_name']:
                donor_name['last_name'] = data['metadata']['last_name']

        if not donor_name['first_name'] and not donor_name['last_name']:
            full_name = data['description']
            first_name, last_name = DonorProcessor._parse_name(full_name)
            donor_name['first_name'] = first_name
            donor_name['last_name'] = last_name
        return donor_name

    @staticmethod
    def get_donor_opt_out(data):
        opt_out = {'email_opt_out': False, 'mail_opt_out': False}
        if data['metadata']:
            if 'opt_out' in data['metadata'] and data['metadata']['opt_out']:
                opt_out_number = data['metadata']['opt_out']
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

    @staticmethod
    def get_donor_receipt_preference(data):
        default_receipt_preference = 'Email'
        receipt_preference = data['metadata']['receipt'] if data['metadata'] and 'receipt' in data[
            'metadata'] else default_receipt_preference
        return receipt_preference

    @staticmethod
    def get_donor_address(data):
        donor_address = {'city': None, 'state': None, 'line1': None, 'country': None, 'postal_code': None}
        if 'address' in data and data['address']:
            address = data['address']
            if 'city' in address:
                donor_address['city'] = address['city']
            if 'state' in address:
                donor_address['state'] = address['state']
            if 'line1' in address:
                donor_address['line1'] = address['line1']
            if 'line2' in address and address['line2']:
                donor_address = donor_address['line1'] + ' ' + address['line2']
            if 'country' in address:
                donor_address['country'] = address['country']
            if 'postal_code' in address:
                donor_address['postal_code'] = address['postal_code']
        else:
            metadata = data['metadata']
            if 'address_city' in metadata:
                donor_address['city'] = metadata['address_city']
            if 'address_street' in metadata:
                donor_address['line1'] = metadata['address_street']
            if 'address_state' in metadata:
                donor_address['state'] = metadata['address_state']
            if 'address_country' in metadata:
                donor_address['country'] = metadata['address_country']
            if 'address_zip' in metadata:
                donor_address['postal_code'] = metadata['address_zip']
        return donor_address

    @staticmethod
    def process_create_event(event_data):
        donor = DonorProcessor._map_donor_create_event(**event_data)
        email = donor.get('Email')
        if email is None:
            raise Exception('Donor email is null.  Cannot process donor create event further.')

        sf_contact_id = Donor.exists_by_email(email)
        if not sf_contact_id:
            print(
                f'Creating Stripe customer {donor.get('FirstName')} {donor.get('LastName')} with email {email} in Salesforce')
            create_response = Donor.create(**donor)
            if 'success' in create_response:
                success = create_response.get('success')
                if success:
                    salesforce_id = create_response.get('id')
                    print(
                        f'Created Stripe customer with email {email} successfully in Salesforce with ID {salesforce_id}')
                else:
                    errors = create_response.get('errors')
                    error_message = f'Did not create Stripe customer with {email} successfully in Salesforce due to: {errors}'
                    raise Exception(error_message)
        else:
            error_message = f'Stripe customer with email {email} already exists in Salesforce with ID {sf_contact_id}. Cannot process donor create event further.'
            raise Exception(error_message)

    @staticmethod
    def process_update_event(event_data):
        donor = DonorProcessor._map_donor_update_event(**event_data)
        email = donor.get('Email')
        if email is None:
            raise Exception('Donor email is null.  Cannot process donor update event further.')
        sf_contact_id = Donor.exists_by_email(email)

        if not sf_contact_id:
            error_message = f'Stripe customer with email {email} does not exist in Salesforce. Cannot process donor update event further.'
            print(error_message)
            time.sleep(30)
            raise Exception(error_message)
        else:
            response = Donor.update(sf_contact_id, **donor)
            if response != 204:
                errors = response.get('errors')
                error_message = f'Did not update Stripe customer with email {email} and Salesforce Contact ID {sf_contact_id} successfully in Salesforce due to {errors}'
                print(error_message)
                raise Exception(error_message)

            print(f'Updated Stripe customer with email {email} and Salesforce Contact ID {sf_contact_id} successfully in Salesforce.')

    @staticmethod
    def _parse_name(full_name):
        names = full_name.split()
        first_name = names[0]
        del names[0]
        last_name = ' '.join(names) if names else 'N/A'
        return first_name, last_name
