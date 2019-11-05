from django.contrib import admin

# Register your models here.

import hydrogen as h
# ^ are you joking me Yang?
from import_export import resources, widgets, fields
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ProblemInline(admin.TabularInline):
	model = h.models.Problem
	fields = ('number', 'test', 'answer', 'weight',)

@admin.register(h.models.Test)
class TestAdmin(admin.ModelAdmin):
	list_display = ('name', 'exam_window_start', 'exam_window_end', 'active', 'time_limit', 'publish_problems', 'max_attempts')
	inlines = (ProblemInline,)
	search_fields = ('name',)
	list_filter = ('active',)

@admin.register(h.models.Problem)
class ProblemAdmin(admin.ModelAdmin):
	list_display = ('test', 'number', 'answer', 'weight')
	list_filter = ('test', 'test__active',)

@admin.register(h.models.SubmissionKey)
class SubmissionKeyAdmin(admin.ModelAdmin):
	list_display = ('id', 'display_name', 'real_name', 'email', 'test', 'end_time',)
	list_filter = ('test',)
	search_fields = ('display_name', 'real_name', 'email')

@admin.register(h.models.Attempt)
class AttemptAdmin(admin.ModelAdmin):
	list_display = ('submission_key', 'student_answer', 'problem', 'time')
	list_filter = ('submission_key__test',)
