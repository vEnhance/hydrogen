from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'^active/$', views.ActiveTestView.as_view(), name='active'),
		url(r'^past/$', views.PastTestView.as_view(), name='past'),
		url(r'^start/(?P<test_id>[0-9]+)/$', views.new_key, name='new_key'),
		url(r'^load/(?P<test_id>[0-9]+)/$', views.load_key, name='load_key'),
		url(r'^compete/(?P<sub_id>[\w-]+)/$', views.compete, name='compete'),
		url(r'^scores/(?P<test_id>[0-9]+)/$', views.scoreboard, name='scoreboard'),
		]
