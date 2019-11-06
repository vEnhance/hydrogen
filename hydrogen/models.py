from django.db import models
from django.contrib.auth import models as auth
import core
from django.urls import reverse

import uuid
from django.utils import timezone

# Create your models here.

class Test(models.Model):
	name = models.CharField(max_length=80,
			help_text = "Name of test", unique=True)
	description = models.TextField(default='',
			help_text = "Description of the test (shown on listing).")
	problems_url = models.CharField(max_length=150,
			help_text = "The URL to the problems file or page")
	organization = models.ForeignKey(core.models.Organization,
			on_delete = models.CASCADE,
			help_text = "The organization running this contest.")

	exam_window_start = models.DateTimeField(
			help_text = "Earliest you can start the test")
	exam_window_end = models.DateTimeField(
			help_text = "Latest you can start the test")
	active = models.BooleanField(default=False,
			help_text = "Is the contest currently active?")
	time_limit = models.PositiveIntegerField(blank=True, null=True,
			help_text = "How long is the contest in minutes? "
			"Leave blank for no time limit at all.")
	team_size = models.PositiveIntegerField(default = 1,
			help_text = "Number of students per team; "
			"use 1 for individual.")

	publish_problems = models.BooleanField(default=False,
			help_text = "Show the problems URL to the public "
			"at the start of the exam.")
	max_attempts = models.PositiveIntegerField(default = 0,
			help_text = "Number of available attempts "
					"on each problem on the test for live-grading. "
					"Set to zero if you don't want live-grading.")

	@property
	def is_indiv(self):
		return (self.team_size == 1)
	@property
	def is_live_grading(self):
		return (self.max_attempts != 0)
	@property
	def window_has_past(self):
		return timezone.now() > self.exam_window_end
	@property
	def window_not_started(self):
		return timezone.now() < self.exam_window_start
	@property
	def accepting_submissions(self):
		return (not self.window_has_past) \
				and (not self.window_not_started) \
				and self.active

	def __str__(self):
		return self.name

class SubmissionKey(models.Model):
	id = models.UUIDField(primary_key=True,
			default=uuid.uuid4, editable=False)
	display_name = models.CharField(max_length=80,
			help_text = "The displayed name of the student "
			"or team taking the contest, "
			"e.g. \"MIT Beavers\", \"Yang the Sheep\". "
			"For individual students this can be the same "
			"as the real name.")
	real_name = models.TextField(max_length=240,
			verbose_name = "Real name(s) of participant(s)",
			help_text = "Real name(s) of participants(s), one per line.")
	email = models.EmailField(max_length=80,
			help_text = "Email used to contact participant(s) "
			"if necessary.")
	test = models.ForeignKey(Test,
			on_delete=models.CASCADE,
			help_text = "Test that the submission is for.")
	end_time = models.DateTimeField(
			help_text = "Latest you can submit answers. "
			"Set automatically by server.")
	def __str__(self):
		return self.display_name + " vs " + str(self.test)
	def get_absolute_url(self):
		return reverse("compete", args=(self.id,))

class Problem(models.Model):
	test = models.ForeignKey(Test,
			on_delete=models.CASCADE,
			help_text = "The test that the problem is on")
	number = models.PositiveIntegerField(
			help_text = "The problem number on the test")
	answer = models.IntegerField(
			help_text = "The answer to the problem")
	weight = models.IntegerField(default = 1,
			help_text = "The weight of the problem")

	def __str__(self):
		return self.test.name + " #" + str(self.number)
	class Meta:
		unique_together = ('test', 'number',)
		ordering = ('test', 'number',)

class Attempt(models.Model):
	submission_key = models.ForeignKey(SubmissionKey,
			on_delete = models.CASCADE,
			help_text = "Which session is this attempt a part of?")
	student_answer = models.IntegerField(
			help_text = "The answer the student is inputting")
	problem = models.ForeignKey(Problem,
			on_delete = models.CASCADE,
			help_text = "The problem the attempt is for")
	time = models.DateTimeField(auto_now_add = True,
			help_text = "The time the attempt was made")
	@property
	def correct(self):
		return self.student_answer == self.problem.answer
