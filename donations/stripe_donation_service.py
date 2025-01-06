from utils.stripe_connection import StripeConnection


class StripeDonationService:
    def __init__(self, connection: StripeConnection):
        self._connection = connection

    def get_stripe_subscription_by_invoice_id(self, invoice_id: str):
        print(f'Retrieving stripe subscription id for invoice id: {invoice_id}')
        response = self._connection.stripe.Invoice.retrieve(invoice_id)
        print(f'Response from Stripe after retrieving stripe subscription id:\n{response}')
        return response.get('subscription')
