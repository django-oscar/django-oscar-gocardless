from django.conf.urls.defaults import *

from oscar_gocardless import views


urlpatterns = patterns('',
    url(r'^redirect/', views.RedirectView.as_view(), name='gocardless-redirect'),
    url(r'^confirm/', views.ConfirmView.as_view(), name='gocardless-response'),
    url(r'^cancel/', views.CancelView.as_view(), name='gocardless-cancel'),
)
