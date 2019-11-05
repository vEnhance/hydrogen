from django.conf.urls import url
from . import views

from django.http import HttpResponseRedirect

def hydrogen_temp_redirect(request):
    return HttpResponseRedirect("/hydrogen")

urlpatterns = [
	url(r'^$', hydrogen_temp_redirect),
]

