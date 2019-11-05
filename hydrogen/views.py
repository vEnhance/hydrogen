from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.urls import reverse
from .forms import NewSubmissionKeyForm, NewAttemptForm
from . import models
from datetime import timedelta
from django.views import generic
from django.contrib import messages
from django.forms.models import model_to_dict
from django.utils import timezone
import collections
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import F, Sum, Case, When

# Create your views here.

# In sessions data, we'll store a
# dict of test ID -> submission key for user
def get_sub_key(request, test_id):
	if not "hydrogen_session_keys" in request.session:
		request.session["hydrogen_session_keys"] = {}
	sub_id = request.session["hydrogen_session_keys"].get(test_id)
	if sub_id is not None:
		return models.SubmissionKey.objects.filter(id=sub_id).first()
	else:
		return None

def set_sub_key(request, test_id, sub_id):
	old_id = get_sub_key(request, test_id)
	if old_id != sub_id:
		request.session["hydrogen_session_keys"][test_id] = sub_id
		request.session.modified = True

def index(request):
	return render(request, 'hydrogen/index.html', {})

class ActiveTestView(generic.ListView):
	model = models.Test
	queryset = models.Test.objects\
			.filter(active=True).order_by('exam_window_start')
	def get_context_data(self, **kwargs):
		context = super(ActiveTestView, self).get_context_data(**kwargs)
		context['list_title'] = "Active Tests"
		return context

class PastTestView(generic.ListView):
	model = models.Test
	queryset = models.Test.objects\
			.filter(active=False).order_by('exam_window_start')
	def get_context_data(self, **kwargs):
		context = super(PastTestView, self).get_context_data(**kwargs)
		context['list_title'] = "Past Tests"
		return context

def new_key(request, test_id):
	test = get_object_or_404(models.Test, pk = test_id)
	prev_sub_key = get_sub_key(request, test_id)
	if prev_sub_key is not None:
		return HttpResponseRedirect(
				reverse("compete", args=(prev_sub_key.id,)))

	if test.window_has_past:
		messages.warning(request, "Sorry, the window has passed, "
				"no new submissions are allowed.")
		form = None
	elif test.window_not_started:
		messages.warning(request, "Sorry, the test has not started yet.")
		form = None
	elif not test.active:
		messages.warning(request, "Sorry, the test is not accepting submissions now.")
		form = None
	elif request.method == "POST":
		assert test.accepting_submissions
		form = NewSubmissionKeyForm(request.POST)
		if form.is_valid():
			new_sub_key = form.save(commit=False)
			new_sub_key.test = test
			new_sub_key.end_time = timezone.now() + \
					timedelta(minutes=test.time_limit)
			new_sub_key.save()
			set_sub_key(request, test_id, str(new_sub_key.id))
			return HttpResponseRedirect(
					reverse("compete", args=(new_sub_key.id,)))
	else:
		form = NewSubmissionKeyForm()
	context = {'form' : form, 'test' : test}
	return render(request, "hydrogen/new_key.html", context)

def load_key(request, test_id):
	sub_key = get_sub_key(request, test_id)
	if sub_key is not None:
		return HttpResponseRedirect(
				reverse("compete", args=(sub_key.id,)))
	else:
		return HttpResponseRedirect(
				reverse("new_key", args=(test_id,)))

def grade(request, sub_key, attempt, past_attempts):
	attempt.submission_key = sub_key
	problem = attempt.problem
	true_answer = problem.answer
	student_answer = attempt.student_answer
	already_solved = [d['problem__number'] for d in past_attempts
			if d['student_answer'] == d['problem__answer']]

	# Check time limit
	if timezone.now() > sub_key.end_time:
		messages.error(request, "Sorry, time has expired.")
		return None

	# Check not already answered correctly
	if problem.number in already_solved:
		messages.error(request, "You already solved %s correctly." %problem)
		return None

	# Check the problem is in the right test
	# (only if malicious input or serious bug)
	if not problem.test == sub_key.test:
		messages.error(request, "nani the fuck?") # ragequit
		return None

	# Check attempt limit
	num_attempts = len([d for d in past_attempts \
			if d['problem__number'] == problem.number])
	attempts_left = problem.test.max_attempts - num_attempts
	if attempts_left <= 0:
		messages.error(request, "No attempts remaining for %s." % problem)
		return None

	# Now check answer
	if student_answer == true_answer:
		messages.success(request,
				'Correct answer %d submitted for %s.'
				%(student_answer, problem))
		sub_key.save()
	else:
		attempts_left -= 1
		messages.warning(request,
				'Incorrect answer %d submitted for %s. '
				'%d attempts remaining.'
				%(student_answer, problem, attempts_left))
	# Student allowed to submit, so save to database
	attempt.save()
	return attempt


def compete(request, sub_id):
	sub_key = get_object_or_404(models.SubmissionKey, pk = sub_id)
	test = sub_key.test

	past_attempts = list(models.Attempt.objects.filter(submission_key = sub_key)\
			.order_by('time').values('student_answer',
				'problem__number', 'problem__answer', 'time'))

	if request.method == "POST":
		form = NewAttemptForm(request.POST, test = test)
		if form.is_valid():
			# Create object, get relevant grading data
			attempt = form.save(commit=False)
			attempt = grade(request, sub_key, attempt, past_attempts)
			if attempt is not None:
				d = {
						'problem__number' : attempt.problem.number,
						'problem__answer' : attempt.problem.answer,
						'time' : attempt.time,
						'student_answer': attempt.student_answer,
						}
				past_attempts.append(d) # add to log
				reset_form = attempt.correct # reset form iff correct
			else: reset_form = False # attempt rejected, allow correction
		else: reset_form = False # invalid form, allow correction
	else: reset_form = True # no form, reset form

	if reset_form: form = NewAttemptForm(test = test)

	# generate history dictionary; this is a dictionary of the form
	# n -> { answer, weight, correct, attempts }{
	# where attempts is a dictionary provided by values
	history = collections.OrderedDict()
	for p in models.Problem.objects.filter(test = test).values('number', 'answer', 'weight'):
		history[p['number']] = {
				'answer' : p['answer'],
				'weight' : p['weight'],
				'solved' : False, # set to True later
				'attempts' : []
				}
	for d in past_attempts:
		n = d.pop('problem__number')
		h = history[n]
		h['attempts'].append(d) # add attempt to log
		if d['student_answer'] == h['answer']:
			h['solved'] = True # there was a submission with this correct
	score = sum(h['weight'] for h in history.values() if h['solved'])

	context = {
			'sub_key' : sub_key,
			'test' : test,
			'form' : form,
			'score' : score,
			'history' : history,
			}
	return render(request, "hydrogen/compete.html", context)


@staff_member_required
def scoreboard(request, test_id):
	test = models.Test.objects.get(id = test_id)

	# oh boy I love querysets
	submissions = models.SubmissionKey.objects\
			.filter(test = test)\
			.annotate(total_score = Sum(Case(
				When(
					attempt__problem__answer
						= F('attempt__student_answer'),
					then = F('attempt__problem__weight')),
				default = 0)))\
			.order_by('-total_score')\
			.values('total_score', 'display_name', 'id')

	context = {
			'submissions' : submissions,
			'test' : test,
			}
	return render(request, "hydrogen/scoreboard.html", context)
