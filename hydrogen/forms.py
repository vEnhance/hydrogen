from django import forms
from . import models
import datetime

TEAM_REAL_NAME_PROMPT = """Student1 Name (graduating %d)
Student2 Name (graduating %d)
... etc ...
""" %(datetime.datetime.now().year+1, datetime.datetime.now().year+3)

TEAM_REAL_NAME_HELP = """Enter the real names of all students
taking this exam, one per line.
For each student, write their graduation year from high school
in parentheses immediately afterwards.
You can enter 9999 as the year if the student is unofficial."""


class NewSubmissionKeyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		test = kwargs.pop('test')
		super(NewSubmissionKeyForm, self).__init__(*args, **kwargs)
		self.fields['captcha'] = forms.IntegerField(
				required = True,
				min_value = 0,
				max_value = 100000000,
				label = "Sum of first four primes",
				help_text = "Are you human? "
				"If so, please input the sum of the first four prime "
				"numbers as a decimal number.")

		if test.is_indiv:
			self.fields['display_name'].label = "Your name"
			self.fields['display_name'].help_text = "Enter your real name."
			self.fields['real_name'] = forms.IntegerField(
					label = "Graduation year",
					help_text = "Enter your graduation year " \
					"or 9999 if you are participating unofficially."
					)
		else:
			self.fields['display_name'].label = "Team name"
			self.fields['display_name'].help_text = "Enter a team name."
			self.fields['real_name'].initial = TEAM_REAL_NAME_PROMPT
			self.fields['real_name'].help_text = TEAM_REAL_NAME_HELP


	def clean(self):
		super(NewSubmissionKeyForm, self).clean()
		seventeen = self.cleaned_data['captcha']
		if seventeen != 17:
			raise forms.ValidationError("You failed the CAPTCHA. "
					"try entering the seventh prime instead.")
		return self.cleaned_data

	class Meta:
		model = models.SubmissionKey
		fields = ('display_name', 'real_name', 'email', )

class NewAttemptForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		test = kwargs.pop('test')
		super(NewAttemptForm, self).__init__(*args,**kwargs)
		self.fields['problem'].queryset = models.Problem.objects.filter(test=test)

	class Meta:
		model = models.Attempt
		fields = ('problem', 'student_answer',)

class InputAnswerForm(forms.Form):
	answer = forms.IntegerField(label="", required=False)
