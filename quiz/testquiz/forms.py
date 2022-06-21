from django import forms
'''models'''
from testquiz.models import Quiz
 

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "creator",
            "question_point",
            "attempts_quiz"
        ]