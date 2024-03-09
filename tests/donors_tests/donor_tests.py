from donors.donor import Donor


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
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail99@gmail.com',
             'Email': 'testemail99@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
    response = Donor.create(**donor)
    assert response.get('success') is True
    assert type(response) is dict


def test_create_donor_errors():
    donor = {'FirstName': 'Melinda', 'LastName': 'Trump', 'ANET_Donor__c': True,
             'npe01__Preferred_Email__c': 'Personal', 'npe01__HomeEmail__c': 'testemail@gmail.com',
             'Email': 'testemail@gmail.com',
             'npe01__PreferredPhone__c': 'Home', 'Created_by_Anet_Sync__c': True}
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
    assert response is None
