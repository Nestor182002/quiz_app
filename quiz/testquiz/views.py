from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
'''models'''
from testquiz.models import Quiz,QuizUser,Question,Answers,Questions_answered
'''view'''
from django.views.generic import CreateView,ListView




# Create your views here.
def index_quiz(request):
    if request.method == "GET":
        context ={
            "data": Quiz.objects.all()
        }
        return render(request,'list_and_create/Listquiz.html',context)

def detail_quiz(request,pk):
    if request.method == "GET":
        context ={
            "data": Quiz.objects.filter(pk=pk)
        }
        return render(request,'list_and_create/detailquiz.html',context)

class Create_Quiz(CreateView):
    model=Quiz
    template_name = 'list_and_create/createquiz.html'
    fields =['title','question_point','attempts_quiz']
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

# pause for now
def CreateQuestions_Answers(request,pk):
    context ={}
    if request.method == "GET":
        context["data"] = "hola"
        return render(request,'create_question_answer/question_answers.html',context)
    if request.method == "POST":
        return render(request,'create_question_answer/question_answers.html')



'''verify if user exist in the quiz or not and create'''
def Verify_Quiz(request,pk):
    if request.user.is_authenticated:
        quiz=Quiz.objects.get(pk=pk)
        if request.method == 'GET':
            Quizuser=QuizUser.objects.filter(competitor=request.user,Quiz=pk).exists()
            if Quizuser == False:
                return render(request,'validate/validate_user.html')
            else:
                return redirect( reverse('play',args=(quiz.id,)))

        if request.method == 'POST':
            quiz_attemps=quiz.attempts_quiz
            response=request.POST.get('response')
            if response == 'yes':
                QuizUser.objects.create(competitor=request.user,Quiz=quiz,remaining_attempts=quiz_attemps)
                return redirect(reverse('play',args=(quiz.id,)))
            else:
                return redirect(reverse('detailquiz',args=(quiz.id,)))
    else:
        return render(request,'validate/validate_user.html')


class List_quiz(ListView):
    model=Quiz
    template_name = 'quiz/quiz.html'
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        Quizuser=QuizUser.objects.filter(competitor=self.request.user,Quiz=pk).exists()
        if Quizuser:
            return Quiz.objects.filter(pk=pk)
    
    def dispatch(self, request, *args, **kwargs):
        User=request.user
        pk = self.kwargs['pk']

        if User.is_authenticated == False:
            return render(request,'validate/validate_user.html')

        if Question.objects.filter(quiz_question=pk,).count() == Questions_answered.objects.filter(quiz=pk,response_user=User).count():
            return redirect(reverse('positions',args=(pk,)))

        try:
            result_ok=QuizUser.objects.get(competitor=User,Quiz=pk)

            if result_ok.finished == True:
                return redirect(reverse('positions',args=(pk,)))
            elif result_ok.remaining_attempts == 0:
                return redirect(reverse('positions',args=(pk,)))

        except QuizUser.DoesNotExist:
            return redirect(reverse('detailquiz',args=(pk,)))


        return super().dispatch(request, *args, **kwargs)


# validate data 
def results_quiz(request,pk):
    # verify number of questions answered
    user=request.user
    len_answer_correct=0
    ans_not_found=0
    quiz=Quiz.objects.get(pk=pk)
    question=Question.objects.filter(quiz_question=pk)
    for correct in question:
            len_answer_correct=len_answer_correct+1
    
    if request.method == 'POST' :
        request=request.POST
        data=dict(request.lists())
        data.pop('csrfmiddlewaretoken')

        '''I check the len of data and verify the len of the questions answered and Add'''
        list_question=question.values_list('id',flat=True)
        list_response=Questions_answered.objects.filter(question__in=list_question)
        len_data=len(data)+len(list_response)

        # verify number of questions answered
        if len_data == len_answer_correct:

            # verify if exists the answer
            for ans in data.values():      
                try:
                    list_to_str=''.join(ans)
                    str_to_int=int(list_to_str)
                    Answers.objects.get(pk=str_to_int)
                except Answers.DoesNotExist:
                    ans_not_found=ans_not_found+1
            if ans_not_found >= 1:
                return JsonResponse({'error':'an error occurred','status':'error'})

            else:
                # save answers
                for ans in data.values(): 
                    is_correct=False
                    list_to_strs=''.join(ans)
                    str_to_ints=int(list_to_strs)
                    answer=Answers.objects.get(pk=str_to_ints)    
                    # correct answer
                    if answer.is_correct == True:
                        is_correct=True
                    else:
                        is_correct=False  

                    exist=Questions_answered.objects.filter(question=answer.answers_question).exists()
                    if exist == False:
                        Questions_answered.objects.get_or_create(quiz=quiz,
                        response_user=user,
                        question=answer.answers_question,
                        answer=answer,
                        correct_answer=is_correct
                        ) 

                # finish and assign point
                total_correct=Questions_answered.objects.filter(
                        response_user=user,
                        quiz=quiz,
                        correct_answer=True  
                    ).count()
                user_finish_total=QuizUser.objects.get(competitor=user,Quiz=quiz)
                total_point=total_correct*quiz.question_point
                if user_finish_total.remaining_attempts >= 1:
                    user_finish_total.remaining_attempts=user_finish_total.remaining_attempts -1
                    user_finish_total.finished=True
                    user_finish_total.total_points=total_point
                    user_finish_total.save()
                else:
                    user_finish_total.finished=True
                    user_finish_total.total_points=total_point
                    user_finish_total.save()
                    
                return JsonResponse({'gg':'gg'})


        else:
            return JsonResponse({'error':'answer all the questions','status':'error'})


class positions_table(ListView):
    model=QuizUser
    template_name = 'quiz/resultquiz.html'
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return QuizUser.objects.filter(Quiz=pk,finished=True)



