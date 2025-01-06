from donors.salesforce_donor_service import SalesforceDonorService


def test_exist_by_email_works_when_email_does_not_exist():
    # arrange
    donor = SalesforceDonorService()
    # act
    exists = donor.get_contact_id('amh6889@gmail.com')
    # assert
    assert exists is None


def test_reserved_characters_email_exists():
    # arrange
    donor = SalesforceDonorService()
    email = 'ade-rogers-wright@hotmail.co.uk'
    # act
    contact_id = donor.get_contact_id(email)
    # assert
    assert contact_id is not None
    assert contact_id == '0030b00002TWpQwAAL'


def test_reserved_characters_email_does_not_exist():
    # arrange
    donor = SalesforceDonorService()
    email = 'ade-^?|"\'rogers-wright@hotmail.co.uk'
    # act
    contact_id = donor.get_contact_id(email)
    # assert
    assert contact_id is None


def test_update_donor_errors():
    # arrange
    donor = SalesforceDonorService()
    donor_data = {'FirstName': 'Ted', 'LastName': 'Turner', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail99@gmail.com',
             'Email': 'testemail99@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
    sf_contact_id = '003Ox00000Acq6HIAX'
    # act
    response = donor.update(sf_contact_id, **donor_data)
    print(response)
    # assert
    assert response is not 204

def test_update_donor_succeeds():
    # arrange
    donor = SalesforceDonorService()
    donor_data = {'FirstName': 'Ted', 'LastName': 'Turner', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail99@gmail.com',
             'Email': 'testemail99@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
    sf_contact_id = '003Ox00000Acq6HIAR'
    response = donor.update(sf_contact_id, **donor_data)
    assert response is 204

def test_create_donor_errors():
    # arrange
    donor = SalesforceDonorService()
    donor_data = {'FirstName': 'Melinda', 'LastName': 'Trump', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail9999@gmail.com',
             'Email': 'testemail9999@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True,
             "MailingStreet": "5668 Lilac Blossom Lane", "MailingCity": "San Jose", "MailingState": "CA",
             "MailingCountry": "United States",
             "MailingPostalCode": "95124"}
    response = donor.create(**donor_data)
    assert response.get('success') is False

def test_create_donor_succeeds():
    # arrange
    donor = SalesforceDonorService()
    donor_data = {'FirstName': 'Melinda', 'LastName': 'Trump', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail9998@gmail.com',
             'Email': 'testemail9998@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True,
             "MailingStreet": "5668 Lilac Blossom Lane", "MailingCity": "San Jose", "MailingState": "CA",
             "MailingCountry": "United States",
             "MailingPostalCode": "95124"}
    response = donor.create(**donor_data)
    assert response.get('success') is True

def test_donor_does_not_exist():
    # arrange
    donor = SalesforceDonorService()
    email = 'sometestemail@gmail.com'
    # act
    exists = donor.get_contact_id(email)
    # assert
    assert exists is None


def test_donor_exist():
    # arrange
    donor = SalesforceDonorService()
    email = 'do_test@gmail.com'
    # act
    donor = donor.get_contact_id(email)
    # assert
    assert donor is not None
