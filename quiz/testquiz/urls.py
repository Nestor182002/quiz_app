from django.urls import path

from testquiz.views import index_quiz,Create_Quiz,detail_quiz,CreateQuestions_Answers,Verify_Quiz,List_quiz,results_quiz,positions_table

urlpatterns = [
    path('',index_quiz,name='list_quiz'),
    path('<int:pk>/',detail_quiz,name='detailquiz'),
    #it not in use
    path('quiz/create/',Create_Quiz.as_view(),name='create_quiz'),
    path('question/answer/<int:pk>/',CreateQuestions_Answers,name='create_question_answer'),


    # play quiz
    path('validate/<int:pk>/',Verify_Quiz,name='validate'),
    path('play/<int:pk>/',List_quiz.as_view(),name='play'),
    path('results/<int:pk>/',results_quiz,name='results'),

    path('positions/<int:pk>/',positions_table.as_view(),name='positions')

]
