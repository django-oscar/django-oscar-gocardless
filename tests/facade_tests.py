from django.test import TestCase

from oscar_gocardless import facade


class BillingFacadeTests(TestCase):

    def test_for_smoke(self):
        base_url = 'http://localhost:8000'
        f = facade.BillingFacade(base_url)
