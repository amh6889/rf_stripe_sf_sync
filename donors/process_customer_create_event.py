import json


def process_customer_create_event(event_data: str) -> None:
    event_data_dict = json.loads(event_data)
    print(event_data_dict)


