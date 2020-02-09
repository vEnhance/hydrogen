from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from . import models

# Create your views here.

class OrganizationDetailView(DetailView):
	model = models.Organization
class OrganizationListView(ListView):
	model = models.Organization
	def get_queryset(self):
		return models.Organization.objects.filter(visible=True)
