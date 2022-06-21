from django.contrib import admin
from testquiz.models import Quiz,Question,Questions_answered,QuizUser,Answers

# Register your models here.
class AnswersTabularInline(admin.TabularInline):
    model = Answers

class Quiz_admin(admin.ModelAdmin):
    list_display=('id','title','creator','question_point','attempts_quiz','activate')

class Question_admin(admin.ModelAdmin):
    inlines=[AnswersTabularInline]
    list_display=('id','title','number_question','quiz_question',)

class Answers_admin(admin.ModelAdmin):
    list_display=('id','answers_question','answer','is_correct')

class Questions_answered_admin(admin.ModelAdmin):
    list_display=('id','quiz','response_user','question','answer','correct_answer')

class QuizUser_admin(admin.ModelAdmin):
    list_display=('id','competitor','Quiz','total_points','remaining_attempts','finished')



admin.site.register(Quiz,Quiz_admin)
admin.site.register(Question,Question_admin)
admin.site.register(Answers,Answers_admin)
admin.site.register(Questions_answered,Questions_answered_admin)
admin.site.register(QuizUser,QuizUser_admin)
