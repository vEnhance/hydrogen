from django.contrib import admin

import hydrogen as h # <- are you joking me Yang?
from import_export import resources, widgets, fields
from import_export.admin import ImportExportModelAdmin


class ProblemInline(admin.TabularInline):
	model = h.models.Problem
	fields = ('number', 'test', 'answer', 'weight',)

@admin.register(h.models.Test)
class TestAdmin(admin.ModelAdmin):
	list_display = ('name', 'exam_window_start',
			'exam_window_end', 'active', 'time_limit',
			'team_size', 'publish_problems',
			'max_attempts', 'is_live_grading')
	inlines = (ProblemInline,)
	search_fields = ('name',)
	list_filter = ('active', 'organization',)
	def get_readonly_fields(self, request, obj=None):
		return ['organization',] if not request.user.is_superuser \
				else []

	def has_change_permission(self, request, obj=None):
		if obj is None: return True
		return obj.organization.check_permission(request.user)
	has_view_permission = has_change_permission
	has_add_permission = has_change_permission
	has_delete_permission = has_change_permission

@admin.register(h.models.Problem)
class ProblemAdmin(admin.ModelAdmin):
	list_display = ('test', 'number', 'weight')
	list_filter = ('test', 'test__active',)
	def get_readonly_fields(self, request, obj=None):
		return ['test',] if not request.user.is_superuser \
				else []

	def has_change_permission(self, request, obj=None):
		return request.user.is_superuser
	has_view_permission = has_change_permission
	has_add_permission = has_change_permission
	has_delete_permission = has_change_permission

@admin.register(h.models.SubmissionKey)
class SubmissionKeyAdmin(admin.ModelAdmin):
	list_display = ('id', 'display_name', 'email', 'test', 'start_time',)
	list_filter = ('test', 'test__active',)
	search_fields = ('display_name', 'real_name', 'email')

@admin.register(h.models.Attempt)
class AttemptAdmin(admin.ModelAdmin):
	list_display = ('submission_key', 'student_answer', 'problem', 'time')
	list_filter = ('submission_key__test',)
