from django.conf.urls import url
from . import views

from django.http import HttpResponseRedirect

urlpatterns = [
	url(r'^$', views.OrganizationListView.as_view(),
		name='org-index'),
	url(r'^(?P<slug>[\w-]+)/$', views.OrganizationDetailView.as_view(),
		name='org-view'),
]

