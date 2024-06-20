from utils import slack_notifier


def test_send_message():
    message = "Hello World!"
    success = slack_notifier.send_message(message)
    assert success is True
