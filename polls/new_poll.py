from django import forms
from django.contrib import admin
from .models import Question,Choice

class PostQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)
        
class PostChoices(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)
    