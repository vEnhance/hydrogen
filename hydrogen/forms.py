from django import forms
from . import models

class NewSubmissionKeyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(NewSubmissionKeyForm, self).__init__(*args, **kwargs)
		self.fields['captcha'] = forms.IntegerField(
				required = True,
				min_value = 0,
				max_value = 100000000,
				label = "Sum of first four primes",
				help_text = "Are you human? "
				"If so, please input the sum of the first four prime "
				"numbers as a decimal number.")
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
