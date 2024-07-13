import traceback

from donors.donor import Donor


# TODO: create separate app/process/thread that will query Stripe for all customer's that have a null name and update the name with the description field
# TODO: since Form assembly creates a new customer each time a form is submitted I need to have checks in my code to ensure that if I create a donor in Salesforce that it doesnt exist there already (check by email)
class DonorProcessor:

    # TODO: change below method to _map_create_donor_event and make new function to map an update donor event
    @staticmethod
    def _map_donor(**event_data):
        print(event_data)
        data = event_data['data']['object']
        customer_id = data['id']
        full_name = data['name']
        updates = {}
        # TODO: instead of making another process to update name in Stripe I say just do it in this process to update it.  So create new function that will update Stripe with name
        if not full_name:
            full_name = data['description']
            updates['name'] = full_name

        first_name, last_name = DonorProcessor._parse_name(full_name)

        email = data['email']
        phone = data['phone']
        address = data['address']
        donor_address = DonorProcessor.get_donor_address(data)
        if not address:
            updates['address'] = donor_address

        if updates:
            Donor.update_stripe_customer(customer_id, updates)

        donor = {'External_Contact_ID__c': customer_id, 'FirstName': first_name, 'LastName': last_name,
                 'npe01__HomeEmail__c': email, 'Email': email, 'Phone': phone, 'MailingStreet': donor_address['line1'],
                 'MailingState': donor_address['state'], 'MailingCity': donor_address['city'],
                 'MailingCountry': donor_address['country'], 'MailingPostalCode': donor_address['postal_code'],
                 'npe01__Preferred_Email__c': 'Personal', 'Stripe_Donor__c': True}
        return donor

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
            if 'line2' in address:
                donor_address['line1'] = donor_address['line1'] + ' ' + address['line2']
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
        donor = DonorProcessor._map_donor(**event_data)
        sf_contact_id = Donor.exists_by_email(donor['Email'])
        if not sf_contact_id:
            print(
                f'Creating Stripe customer {donor['External_Contact_ID__c']} with email {donor['Email']} in Salesforce')
            create_response = Donor.create(**donor)
            if 'success' in create_response:
                success = create_response['success']
                if success:
                    salesforce_id = create_response['id']
                    print(
                        f'Created Stripe customer {donor['External_Contact_ID__c']} successfully in Salesforce with ID {salesforce_id}')
                else:
                    errors = create_response['errors']
                    error_message = f'Did not create Stripe customer {donor['External_Contact_ID__c']} successfully in Salesforce due to: {errors}'
                    raise Exception(error_message)
        else:
            error_message = f'Stripe customer {donor['External_Contact_ID__c']} with email {donor['Email']} already exists in Salesforce with ID {sf_contact_id}'
            raise Exception(error_message)

    @staticmethod
    def process_update_event(event_data):
        donor = DonorProcessor._map_donor(**event_data)
        sf_contact_id = Donor.exists_by_email(donor['Email'])

        if not sf_contact_id:
            error_message = f'Stripe customer {donor['External_Contact_ID__c']} with email {donor['Email']} does not exist in Salesforce. Cannot process update event.'
            print(error_message)
            raise Exception(error_message)
        else:
            response = Donor.update(sf_contact_id, **donor)
            if response != 204:
                errors = response['errors']
                error_message = f'Did not update Stripe customer {donor['External_Contact_ID__c']} successfully in Salesforce due to {errors}'
                print(error_message)
                raise Exception(error_message)

            print(f'Updated Stripe customer {donor['External_Contact_ID__c']} successfully in Salesforce.')

    @staticmethod
    def _parse_name(full_name):
        names = full_name.split()
        first_name = names[0]
        del names[0]
        last_name = ' '.join(names)
        return first_name, last_name
