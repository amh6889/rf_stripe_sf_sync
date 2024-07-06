from utils.filter_string import filter_string


def test_filter_string():
    email = 'test--^12345@gmail.com'
    filtered_email = filter_string(email)
    assert filtered_email == ''