from django.contrib import admin

from . import models

# Register your models here.

@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
	list_display = ('name', 'group', 'visible', 'short_description',)
	search_fields = ('name', 'short_description', 'verbose_description')

	def has_change_permission(self, request, obj=None):
		if obj is None: return True
		return obj.check_permission(request.user)
	has_view_permission = has_change_permission

