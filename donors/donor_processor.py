from donors.donor import Donor


class DonorProcessor:

    @staticmethod
    def _map_donor(**event_data):
        print(event_data)
        data = event_data['data']['object']
        full_name = data['name']
        first_name, last_name = DonorProcessor._parse_name(full_name)
        customer_id = data['id']
        email = data['email']
        phone = data['phone']
        city = data['address']['city']
        street = data['address']['line1'] + ' ' + data['address']['line2']
        state = data['address']['state']
        country = data['address']['country']
        postal_code = data['address']['postal_code']
        donor = {'External_Contact_ID__c': customer_id, 'FirstName': first_name, 'LastName': last_name, 'npe01__HomeEmail__c': email, 'Email': email,
                 'Phone': phone, 'MailingStreet': street.rstrip(), 'MailingState': state,
                 'MailingCity': city, 'MailingCountry': country, 'MailingPostalCode': postal_code, 'npe01__Preferred_Email__c': 'Personal'}
        return donor

    @staticmethod
    def process_create_event(event_data):
        donor = DonorProcessor._map_donor(event_data)
        Donor.create(**donor)

    @staticmethod
    def process_update_event(event):
        pass

    @staticmethod
    def _parse_name(full_name):
        names = full_name.split()
        first_name = names[0]
        del names[0]
        last_name = ' '.join(names)
        return first_name, last_name
