from event_processor.event_processor import EventProcessor

if __name__ == '__main__':
    events = EventProcessor.get_events()

    EventProcessor.process_events(events)

