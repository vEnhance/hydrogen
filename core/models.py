from django.db import models
from django.contrib.auth import models as auth

from django.urls import reverse

# Create your models here.

class Organization(models.Model):
	"""A major organization like HMMT or Online Math Open"""
	name = models.CharField(max_length=80, unique=True,
			help_text = "The name of the organization")
	group = models.ForeignKey(auth.Group,
			on_delete = models.CASCADE,
			help_text = "The group for users who are run this.")
	slug = models.SlugField("A slug for the URL for the about page.",
			unique = True)

	short_description = models.TextField(default='',
			help_text = "A short description about the contest. "
			"HTML OK.")
	verbose_description = models.TextField(default='',
			help_text = "A page-long description about the contest. "
			"HTML OK.")
	external_url = models.CharField(max_length=80, default='',
			blank=True, help_text="A website to link to.")
	
	def get_absolute_url(self):
		return reverse("org-view", args=(self.slug,))

	def __str__(self):
		return self.name

	def check_permission(self, user):
		if user.is_superuser: return True
		if not user.is_staff: return False
		return user.groups.filter(name=self.group).exists()
