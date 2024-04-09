class DonationProcessor:

    @staticmethod
    def _map_donation(**event_data):
        print(event_data)
        data = event_data['data']['object']
        full_name = data['name']
        customer_id = data['id']
        email = data['email']
        phone = data['phone']
        city = data['address']['city']
        street = data['address']['line1'] + ' ' + data['address']['line2']
        state = data['address']['state']
        country = data['address']['country']
        postal_code = data['address']['postal_code']
        donation = {'External_Contact_ID__c': customer_id, 'FirstName': first_name, 'LastName': last_name,
                    'npe01__HomeEmail__c': email, 'Email': email,
                    'Phone': phone, 'MailingStreet': street.rstrip(), 'MailingState': state,
                    'MailingCity': city, 'MailingCountry': country, 'MailingPostalCode': postal_code,
                    'npe01__Preferred_Email__c': 'Personal'}
        return donation
