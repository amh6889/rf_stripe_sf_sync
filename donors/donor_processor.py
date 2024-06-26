from donors.donor import Donor
#TODO: create separate app/process/thread that will query Stripe for all customer's that have a null name and update the name with the description field
#TODO: since Form assembly creates a new customer each time a form is submitted I need to have checks in my code to ensure that if I create a donor in Salesforce that it doesnt exist there already (check by email)
class DonorProcessor:

    #TODO: change below method to _map_create_donor_event and make new function to map an update donor event
    @staticmethod
    def _map_donor(**event_data):
        print(event_data)
        data = event_data['data']['object']
        customer_id = data['id']
        full_name = data['name']
        if not full_name:
            full_name = data['description']
        first_name, last_name = DonorProcessor._parse_name(full_name)
        email = data['email']
        phone = data['phone']
        street, city, state, country, postal_code = DonorProcessor.get_donor_address(data)
        donor = {'External_Contact_ID__c': customer_id, 'FirstName': first_name, 'LastName': last_name, 'npe01__HomeEmail__c': email, 'Email': email,
                 'Phone': phone, 'MailingStreet': street, 'MailingState': state,
                 'MailingCity': city, 'MailingCountry': country, 'MailingPostalCode': postal_code, 'npe01__Preferred_Email__c': 'Personal'}
        return donor

    @staticmethod
    def get_donor_address(data):
        street = city = state = country = postal_code = None
        if 'address' in data and data['address']:
            address = data['address']
            if 'city' in address:
                city = address['city']
            if 'state' in address:
                state = address['state']
            if 'line1' in address:
                street = address['line1'] + ' ' + address['line2']
            if 'country' in address:
                country = address['country']
            if 'postal_code' in address:
                postal_code = address['postal_code']
        else:
            metadata = data['metadata']
            if 'address_city' in metadata:
                city = metadata['address_city']
            if 'address_street' in metadata:
                street = metadata['address_street']
            if 'address_state' in metadata:
                state = metadata['address_state']
            if 'address_country' in metadata:
                country = metadata['address_country']
            if 'address_zip' in metadata:
                postal_code = metadata['address_zip']
        return street, city, state, country, postal_code


    @staticmethod
    def process_create_event(event_data):
        success = False
        try:
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
                        print(
                            f'Did not create Stripe customer {donor['External_Contact_ID__c']} successfully in Salesforce due to: {errors}')
            else:
                print(
                    f'Stripe customer {donor['External_Contact_ID__c']} with email {donor['Email']} exists in Salesforce with ID {sf_contact_id}')
        except Exception as error:
            print(f'Error in Donor.process_create_event due to: {error}')
        finally:
            return success


    @staticmethod
    def process_update_event(event_data):
        update_success = False
        try:
            donor = DonorProcessor._map_donor(**event_data)
            sf_contact_id = Donor.exists_by_email(donor['Email'])

            if not sf_contact_id:
                print(
                    f'Stripe customer {donor['External_Contact_ID__c']} with email {donor['Email']} does not exist in Salesforce. Cannot process update event.')
            else:
                response = Donor.update(sf_contact_id, **donor)
                if response == 204:
                    update_success = True
                    print(
                        f'Updated Stripe customer {donor['External_Contact_ID__c']} successfully in Salesforce.')
                else:
                    errors = response['errors']
                    print(
                        f'Did not update Stripe customer {donor['External_Contact_ID__c']} successfully in Salesforce due to {errors}')
        except Exception as error:
            print(f'Error in Donor.process_update_event due to: {error}')
        finally:
            return update_success

    @staticmethod
    def _parse_name(full_name):
        names = full_name.split()
        first_name = names[0]
        del names[0]
        last_name = ' '.join(names)
        return first_name, last_name
