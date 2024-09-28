from utils.filter_string import filter_string


def test_filter_string_with_invalid_characters():
    email = 'test--^12345@gmail.com'
    filtered_email = filter_string(email)
    assert filtered_email == 'test12345@gmail.com'

def test_filter_string_with_no_invalid_characters():
    email = 'testscenario1@gmail.com'
    filtered_email = filter_string(email)
    assert filtered_email == 'testscenario1@gmail.com'