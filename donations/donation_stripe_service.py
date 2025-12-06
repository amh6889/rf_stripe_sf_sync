from utils.stripe_connection import StripeConnection


class StripeDonationService:
    def __init__(self, connection: StripeConnection):
        self._connection = connection

    def get_stripe_subscription_by_invoice_id(self, invoice_id: str) -> str:
        print(f'Retrieving stripe subscription id for invoice id: {invoice_id}')
        response = self._connection.stripe.Invoice.retrieve(invoice_id)
        print(f'Response from Stripe after retrieving stripe subscription id:\n{response}')
        return response.get('subscription')

    def get_stripe_charge_by_id(self, charge_id: str) -> dict:
        print(f'Retrieving stripe charge id: {charge_id}')
        response = self._connection.stripe.Charge.retrieve(charge_id)
        print(f'Response from Stripe after retrieving stripe charge id:\n{response}')
        return response
