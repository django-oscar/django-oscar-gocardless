from django.conf import settings
from django.contrib.sites.models import Site
from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.payment.exceptions import RedirectRequired

from oscar_gocardless import facade


class PaymentDetailsView(OscarPaymentDetailsView):

    def handle_payment(self, order_number, total_incl_tax, **kwargs):
        # Determine base URL of current site - you could just set this in a
        # setting
        if settings.DEBUG:
            # Determine the localserver's hostname to use when 
            # in testing mode
            base_url = 'http://%s' % self.request.META['HTTP_HOST']
        else:
            base_url = 'https://%s' % Site.objects.get_current().domain

        # Payment requires a redirect so we raise a RedirectRequired exception
        # and oscar's checkout flow will handle the rest.
        url = facade.BilingFacade(base_url).get_redirect_url(order_number,
                                                             total_incl_tax,
                                                             self.request.user)
        raise RedirectRequired(url)

