from utils.stripe_connection import StripeConnection


def parse_payment_method(subscription):
    payment_method = None
    payment_methods = []
    if subscription.get('default_payment_method'):
        payment_methods.append(subscription['default_payment_method'])
    if subscription.get('default_source'):
        payment_methods.append(subscription['default_source'])
    if subscription.get('latest_invoice'):
        if subscription['latest_invoice']['payment_intent']:
            temp_payment_intent = subscription['latest_invoice']['payment_intent']
            if temp_payment_intent.get('payment_method'):
                payment_methods.append(temp_payment_intent.get('payment_method'))
    if payment_methods:
        any(payment_method := pm for pm in tuple(payment_methods))
    return payment_method


class StripeSubscriptionService:
    def __init__(self, connection: StripeConnection):
        self.connection = connection

    def get_stripe_payment_method(self, stripe_subscription_id):
        print(f'Getting payment method from Stripe for subscription {stripe_subscription_id}')
        subscription = self.connection.stripe.Subscription.retrieve(stripe_subscription_id,
                                                                    expand=['default_payment_method', 'default_source',
                                                                            'latest_invoice.payment_intent.payment_method'])
        payment_method = parse_payment_method(subscription)
        return payment_method

    def get_subscription_schedule(self, stripe_subscription_schedule_id: str) -> dict:
        print(f'Getting subscription schedule {stripe_subscription_schedule_id} from Stripe...')
        subscription_schedule = self.connection.stripe.SubscriptionSchedule.retrieve(stripe_subscription_schedule_id)
        return subscription_schedule
