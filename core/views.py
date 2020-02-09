from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from . import models
import hydrogen.models

# Create your views here.

class OrganizationDetailView(DetailView):
	model = models.Organization
	def get_context_data(self, **kwargs):
		context = super(OrganizationDetailView, self).get_context_data(**kwargs)
		context['num_active'] = hydrogen.models.Test.objects\
				.filter(organization=self.object,visible=True).count()
		return context
class OrganizationListView(ListView):
	model = models.Organization
	def get_queryset(self):
		return models.Organization.objects.filter(visible=True)
