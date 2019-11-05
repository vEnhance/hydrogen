from django.db import models
from django.contrib.auth import models as auth

# Create your models here.

class Organization(models.Model):
	"""A major organization like HMMT or Online Math Open"""
	name = models.CharField(max_length=80, unique=True,
			help_text = "The name of the organization")
	group = models.ForeignKey(auth.Group,
			on_delete = models.CASCADE,
			help_text = "The group for users who want to modify")

	description = models.TextField(default='',
			help_text = "A description about the contest.")
