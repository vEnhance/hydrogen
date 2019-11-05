from django.contrib import admin

from . import models

# Register your models here.

@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('name', 'group', 'description',)
	search_fields = ('name', 'description',)
