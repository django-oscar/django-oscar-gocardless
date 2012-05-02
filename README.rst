===================================
GoCardLess package for django-oscar
===================================

This is a work in progress - not ready for production yet.  It also depends on
the forthcoming version of oscar (0.2) which hasn't been released yet.  

Overview
========

GoCardless_ provide payments straight from customer's bank accounts using the
Direct Debit system.  A typical integration involves redirecting the user to
GoCardless' site where they enter their bank account details and confirm the
transaction.  

This library provides integration between GoCardless and `django-oscar`_.

.. _GoCardless: https://gocardless.com/
.. _`django-oscar`: https://github.com/tangentlabs/django-oscar

Installation
============

You need to make sure your redirect URI and cancel URIs are set up within your
GoCardless dashboard.  Only the scheme and domain need to match so you can just
put your site URL in there.

Limitations
===========

* Only the 'one-off bill' transaction has been implemented so far. 
* Webhook handling isn't implemented yet.
* Refunds aren't possible through the GoCardless API at the moment.  These
  should be handled either through BACS transfers or a cheque payment.

Contribute
==========

Create a virtualenv, clone repo and install dependencies::

    mkvirtualenv oscar-gocardless
    git clone git://github.com/tangentlabs/django-oscar-gocardless.git
    cd django-oscar-gocardless
    python setup.py develop
    pip install -r requirements.txt

Set up a sandbox site to play with::

    cd sandbox
    ./manage.py syncdb --noinput
    ./manage.py migrate
    ./manage.py oscar_import_catalogue data/books-catalogue.csv

You can test the end-to-end process by adding an item to your basket and then
proceeding through checkout.  After the preview page, you'll be redirected to
the GoCardless 'sandbox' site where you can use the following account details to
complete an order:

    Account number -  55779911
    Sort code - 200000
