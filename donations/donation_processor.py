import datetime
import locale


from donations.donation import Donation
from donors.donor import Donor
from subscriptions.subscription import Subscription


class DonationProcessor:

    #TODO: throw error if donation does not have email/name in Salesforce because I need to be able to connect donation to Contact in Salesforce so that there are not orphan donations
    #TODO: figure out situation below if salesforce id of existing subscription is different than one in event data.  This sometimes happened with ANET where a husband and wife had a subscription together and then one created one by themselves and messed up the sync
    @staticmethod
    def _map_donation(**event_data):
        try:
            data = event_data['data']['object']
            stripe_payment_intent_id = data['id']
            amount = data['amount']
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            formatted_amount = locale.currency(amount / 100, symbol=False)
            stripe_customer_id = data['customer']
            donor_email = Donor.get_email(stripe_customer_id)
            salesforce_id = None
            if donor_email:
                salesforce_id = Donor.exists_by_email(donor_email)

            if not salesforce_id:
                raise Exception(f'Donation event error: Stripe customer {stripe_customer_id} with email {donor_email} does not exist in Salesforce')

            epoch_time_created = data['created']
            closed_date = DonationProcessor._parse_epoch_time(epoch_time_created)
            status = data['status']
            stage_name = DonationProcessor._map_stage_name(status)
            payment_method = data['payment_method_details']
            last_4_digits = DonationProcessor._get_payment_method_last_4(payment_method)

            stripe_invoice_id = data['invoice']
            stripe_subscription_id = None
            if stripe_invoice_id is not None:
                stripe_subscription_id = Donation.get_stripe_subscription_id(stripe_invoice_id)

            salesforce_recurring_donation_id = None
            if stripe_subscription_id is not None:
                salesforce_recurring_donation = Subscription.exists(stripe_subscription_id)
                if salesforce_recurring_donation:
                    salesforce_recurring_donation_id = salesforce_recurring_donation['id']
                    salesforce_id = salesforce_recurring_donation['sf_contact_id']
                else:
                    raise Exception(f'Donation event error: Stripe subscription {stripe_subscription_id} does not exist in Salesforce')


            donation = {'npe01__Contact_Id_for_Role__c': salesforce_id, 'npsp__Primary_Contact__c': salesforce_id,
                        'Amount': formatted_amount,
                        'CloseDate': closed_date, 'Donation_Source__c': 'RF Web-form',
                        'StageName': stage_name, 'Name': f'${formatted_amount} RF Web-form',
                        'npe03__Recurring_Donation__c': salesforce_recurring_donation_id,
                        'Card_Last_4__c': last_4_digits, 'Stripe_Invoice_ID__c': stripe_payment_intent_id,
                        'Stripe_Subscription_ID__c': stripe_subscription_id}
            return donation
        except Exception as error:
            message = f'Error mapping donation due to {error}'
            print(message)
            raise Exception(message)

    @staticmethod
    def _map_refund(**event_data):
        try:
            data = event_data['data']['object']
            stripe_payment_intent_id = data['payment_intent']
            sf_donation_id = Donation.exists(stripe_payment_intent_id)
            donation = {'Id': sf_donation_id, 'StageName': 'Withdrawn'}
            return donation
        except Exception as error:
            print(f'Error mapping refund due to {error}')


    @staticmethod
    def _parse_epoch_time(epoch_time):
        date_time = datetime.datetime.fromtimestamp(epoch_time, datetime.UTC)
        return date_time.isoformat()

    # TODO: might need to change map stage name since status can be required action, etc (but I think stripe would send another webhook event type in this case)
    @staticmethod
    def _map_stage_name(stripe_donation_status):
        print(stripe_donation_status)
        stage_name = 'Closed Won'
        if stripe_donation_status == 'succeeded':
            stage_name = 'Closed Won'
        return stage_name

    @staticmethod
    def _get_payment_method_last_4(stripe_payment_method):
        try:
            #payment_method = stripe.PaymentMethod.retrieve(stripe_payment_method_id)
            last_4_digits = None
            payment_method_type = stripe_payment_method['type']
            if payment_method_type == 'card':
                last_4_digits = stripe_payment_method['card']['last4']
            elif payment_method_type == 'us_bank_account':
                last_4_digits = stripe_payment_method['us_bank_account']['last4']
            else:
                print(f'Payment method type {payment_method_type} is not supported')
            return last_4_digits
        except Exception as e:
            print(e)

    @staticmethod
    def process_create_event(donation_event):
        success = False
        try:
            donation = DonationProcessor._map_donation(**donation_event)
            sf_donation_id = Donation.exists(donation['Stripe_Invoice_ID__c'])
            if not sf_donation_id:
                create_response = Donation.create(**donation)
                if 'success' in create_response:
                    success = create_response['success']
            else:
                print(
                    f'Stripe charge {donation['Stripe_Invoice_ID__c']} already exists in Salesforce. Cannot process create event.')
        except Exception as error:
            print(f'Error in Donation.process_create_event due to: {error}')
        finally:
            return success

    @staticmethod
    def process_update_event(donation_event):
        update_success = False
        try:
            donation = DonationProcessor._map_donation(**donation_event)
            sf_donation_id = Donation.exists(donation['Stripe_Invoice_ID__c'])
            if not sf_donation_id:
                print(
                    f'Stripe charge {donation['Stripe_Invoice_ID__c']} does not exist in Salesforce. Cannot process update event.')
            else:
                response = Donation.update(sf_donation_id, **donation)
                if response == 204:
                    update_success = True
                    print(
                        f'Updated donation {sf_donation_id} successfully in Salesforce.')
        except Exception as error:
            print(f'Error in Donation.process_update_event due to: {error}')
        finally:
            return update_success
