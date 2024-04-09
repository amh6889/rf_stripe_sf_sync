import mysql.connector

config = {
  'user': 'stripe_svc',
  'password': 'stripe123',
  'host': '127.0.0.1',
  'database': 'stripe',
  'raise_on_warnings': False
}
global db_connection
db_connection = mysql.connector.connect(**config)
print(db_connection.is_connected())


