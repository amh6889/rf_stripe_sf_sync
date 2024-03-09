import utils.database_connection

def get_donor_events():
    query = ("SELECT * FROM stripe.stripe_event where is_synced = 'N' and event_type like '%customer%' order by created_at")
    events = []
    with utils.database_connection.db_connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        for row in cursor:
            print(row)
            events.append(row)
    print((events[0]))
    return events
