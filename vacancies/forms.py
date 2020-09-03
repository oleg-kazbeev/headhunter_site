from django import forms

from .models import Feedback, Vacancy


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description')
