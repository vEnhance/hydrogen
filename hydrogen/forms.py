from django import forms
from . import models

class NewSubmissionKeyForm(forms.ModelForm):
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
