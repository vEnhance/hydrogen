from django.conf.urls import url
from . import views
from django.shortcuts import redirect

def active_redirect(request):
	return redirect('active')

urlpatterns = [
	url(r'^$', active_redirect, name='hydrogen-index'),
	url(r'^active/$', views.ActiveTestView.as_view(), name='active'),
	url(r'^past/$', views.PastTestView.as_view(), name='past'),
	url(r'^start/(?P<test_id>[0-9]+)/$', views.new_key, name='new_key'),
	url(r'^load/(?P<test_id>[0-9]+)/$', views.load_key, name='load_key'),
	url(r'^compete/(?P<sub_id>[\w-]+)/$', views.compete, name='compete'),
	url(r'^scoreboard/(?P<test_id>[0-9]+)/$', views.scoreboard, name='scoreboard'),
	url(r'^csv-scores/(?P<test_id>[0-9]+)/$', views.csv_scores, name='csv-scores'),
	url(r'^namechange/(?P<pk>[\w-]+)/$', views.UpdateKey.as_view(), name='update_key')
]
