from salesforce.salesforce_connection import get_salesforce_session


def test_salesforce_connection():
    session_id = get_salesforce_session()
    assert session_id is not None
