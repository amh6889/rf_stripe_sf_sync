from utils.stripe_connection import StripeConnection


class StripeDonorService:

    def __init__(self):
        self.connection = StripeConnection()

    def get_donor_email(self, stripe_customer_id):
        print(f'Retrieving Stripe customer {stripe_customer_id} info from Stripe...')
        customer = self.connection.stripe.Customer.retrieve(stripe_customer_id)
        return customer.email

    def update(self, customer_id, updates):
        try:
            print(f'Updating Stripe customer {customer_id} in Stripe with data:\n{updates}\n')
            response = self.connection.stripe.Customer.modify(customer_id, **updates)
            print(response)
        except Exception as error:
            print(f'Error updating Stripe customer {customer_id} in Stripe due to {error}')

    def get_donor_address(self, stripe_payment_method_id):
        print(f'Retrieving Stripe address for Stripe payment method id {stripe_payment_method_id}...')
        payment_method = self.connection.stripe.PaymentMethod.retrieve(stripe_payment_method_id)
        address = payment_method.billing_details.address
        return address
