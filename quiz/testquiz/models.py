from django.db import models
'''model'''
from django.contrib.auth.models import User

class Quiz(models.Model):
    title=models.CharField(max_length=50)
    creator=models.ForeignKey(User,related_name='quiz_creator',on_delete=models.CASCADE)
    question_point=models.PositiveIntegerField(default=1)
    attempts_quiz=models.PositiveIntegerField(default=1)
    activate=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    '''delete questions answered'''
    def question_list(self):
        # I remove questions you answered
        response=list(Questions_answered.objects.filter(quiz=self.pk).values_list('question',flat=True))
        return self.quiz_question.all().exclude(pk__in=response)

class Question(models.Model):
    quiz_question=models.ForeignKey(Quiz,related_name='quiz_question',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    number_question=models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    def answers_list(self):
        return self.options.all()

class Answers(models.Model):
    answers_question=models.ForeignKey(Question,related_name='options',on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return self.answer

class Questions_answered(models.Model):
    quiz=models.ForeignKey(Quiz,related_name='quiz_attempts',on_delete=models.CASCADE)
    response_user=models.ForeignKey(User,related_name='response_user',on_delete=models.CASCADE)
    question=models.ForeignKey(Question,related_name='response_question',on_delete=models.CASCADE)
    answer=models.ForeignKey(Answers,related_name='response_answers',on_delete=models.CASCADE)
    correct_answer=models.BooleanField()

    def __str__(self):
        return str(self.quiz)

class QuizUser(models.Model):
    competitor=models.ForeignKey(User,related_name='competitor',on_delete=models.CASCADE)
    Quiz=models.ForeignKey(Quiz,related_name='quiz_user',on_delete=models.CASCADE)
    total_points=models.PositiveIntegerField(default=0)
    remaining_attempts=models.PositiveIntegerField(default=0)
    finished=models.BooleanField(default=False)

    def __str__(self):
        return str(self.competitor)
        
    class Meta:
        ordering = ('total_points', )
