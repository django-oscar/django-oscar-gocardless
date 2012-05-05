from django.core.urlresolvers import reverse
import gocardless
from gocardless.exceptions import SignatureError, ClientError
from oscar.apps.payment.exceptions import PaymentError


class BillingFacade(object):
    # Implemented as a class so that projects can subclass and override methods
    # if the parameters passed to GoCardless need to be customised.

    def __init__(self, base_url):
        self.base_url = base_url

    def get_redirect_url(self, order_number, total_incl_tax, user):
        """
        Return a URL for a new one-off bill transaction
        """
        user_params = None
        if user and user.is_authenticated():
            user_params = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
        return gocardless.client.new_bill_url(
            total_incl_tax,
            self.get_transaction_name(order_number),
            self.get_transaction_description(order_number),
            redirect_uri="%s%s" % (self.base_url, reverse('gocardless-response')),
            cancel_uri="%s%s" % (self.base_url, reverse('gocardless-cancel')),
            state=self.get_transaction_state(order_number),
            user=user_params)

    def get_transaction_name(self, order_number):
        return 'One-off bill for order #%s' % order_number

    def get_transaction_description(self, order_number):
        return ''

    def get_transaction_state(self, order_number):
        return ''


def confirm(request):
    """
    Confirm a transaction with GoCardless
    """
    # Pluck params straight off the request path - if any are missing or have been
    # manipulated, then we'll get a SignatureError
    params = {
        'resource_id': request.GET.get('resource_id', None),
        'resource_type': request.GET.get('resource_type', None),
        'resource_uri': request.GET.get('resource_uri', None),
        'signature': request.GET.get('signature', None),
    }
    state = request.GET.get('state', None)
    if state:
        params['state'] = state
    try:
        gocardless.client.confirm_resource(params)
    except SignatureError:
        raise PaymentError("Invalid signature")
    except ClientError:
        raise PaymentError("An error occurred communicating with payment gateway")
