from django.views.generic import RedirectView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from oscar_gocardless import facade
from oscar.apps.payment.exceptions import PaymentError
from oscar.apps.checkout.views import OrderPlacementMixin
from oscar.apps.payment.models import SourceType, Source


class ConfirmView(OrderPlacementMixin, View):
    """
    Handle the response from GoCardless
    """
    def get(self, request, *args, **kwargs):
        try:
            facade.confirm(request)
        except PaymentError, e:
            messages.error(self.request, str(e))
            self.restore_frozen_basket()
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        # Fetch submission data out of session
        order_number = self.checkout_session.get_order_number()
        basket = self.get_submitted_basket()
        total_incl_tax, total_excl_tax = self.get_order_totals(basket)

        # Record payment source
        source_type, is_created = SourceType.objects.get_or_create(name='GoCardless')
        source = Source(source_type=source_type,
                        currency='GBP',
                        amount_allocated=total_incl_tax,
                        amount_debited=total_incl_tax)
        self.add_payment_source(source)

        # Place order
        return self.handle_order_placement(order_number,
                                           basket,
                                           total_incl_tax,
                                           total_excl_tax)


class CancelView(RedirectView):

    def get_redirect_url(self, **kwargs):
        messages.error(self.request, "Transaction cancelled")
        return reverse('checkout:payment-details')


