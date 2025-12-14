from salesforce.salesforce_connection import sf


class SalesforceEmailService:

    def send_email(self, stripe_subscription_id: str, last4: str):
        payload= {
            'stripeSubscriptionId': stripe_subscription_id,
            'last4': last4
        }
        result = sf.apexecute('/Subscription/SendFailedInvoiceEmail', method='POST', data=payload)
        print(result)