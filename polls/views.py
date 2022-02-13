from urllib import response
from django.utils import timezone
from django.shortcuts import get_object_or_404, render ### 코드 양을 줄일 수 있음. 정형화 된 코드를 간단한 함수를 제공.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice

# Create your views here.
### view에서는 request를 인자로 받고, httpresponse를 리턴함. 
### 클라이언트로부터 request를 받아, response를 해준다!

### view는 기능담당, template은 비주얼담당
### template은 polls/templates/polls/index.html처럼 다른 앱의 템플릿과 구분을 할 수 있게 만들어야 함. polls/templates는 안돼.
### 장고는 이름이 일치하는 첫번째 템플릿을 선택함. 만약 같은 템플릿 이름이 다른 app에 있으면 꼬일 수 있음!!! 
### 그래서 앱 이름으로 된 디렉토리에 템플릿을 넣어 이름공간으로 나누는 방법 사용!

def index(request):
    # 1
    # return HttpResponse("Hello, World.")

    # 2
    # latest_question_list = Question.objects.order_by('-pub_date')[:5] ### 출판 일자로 정렬해 5개까지만 가져와서 정렬하겠다!
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # 3
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html') ### template을 load해서 response해줌!
    # context = {
    #     'latest_question_list': latest_question_list, ### context를 통해서 템플릿에 데이터를 전달해줌. 템플릿의 latest~~~를 여기의 latest~~~로 전달해줌
    # }
    # return HttpResponse(template.render(context, request))

    # 4
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    context = {
        'latest_question_list': latest_question_list, ### context를 통해서 템플릿에 데이터를 전달해줌. 템플릿의 latest~~~를 여기의 latest~~~로 전달해줌
    }
    return render(request, 'polls/index.html', context)

### 제너릭(클래스) 뷰를 써보자!

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list' ### 컨텍스트에 넘겨주는 이름이 모델 이름과 다르면, 이걸 다시 정해주고 필요한 데이터를 get_quaryset 함수로 다시 정해주면 됨. 

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now() ### __lte: less than equal. 여러가지 다른 옵션도 있음. __gt: greater than
        ).order_by('-pub_date')[:5]

# def detail(request, question_id):
#     # 1
#     # return HttpResponse("You're looking at  question %s." % question_id)

#     # 2
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question}) ### http 404로 render처럼 간단하게 처리할 수 있음

#     # 3
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question':question})

class DetailView(generic.DeleteView): ### 제너릭에서는 데이터 이름, 해당 템플릿에서 사용할 데이터 모델만 명시해주면 됨!!
    model = Question
    template_name = 'polls/detail.html'

# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question}) ### question 번호 조회 후 result 결과 페이지 보여줌. 이때 question 데이터가 같이 넘어가

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'    

def vote(request, question_id): ### question id를 넘겨받아. 
    # return HttpResponse("You're voting on question %s." % question_id)

    ### get 방식과 post 방식? get은 조회용, post는 데이터 생성/변경?
    if request.method == 'GET':
        pass ### 방식에 따라 처리 다르게!
    elif request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id) ### question id를 조회해 
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice']) ### 이 q에 대해 외래 키를 갖는 선택지를 가져와. 선택지 중 pk값이 템플릿에서 넘겨받은 값을 조회! 그건 (detail.html)input의 name!!
        except (KeyError, Choice.DoesNotExist): ### 넘어온 데이터가 없을때
            return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."  ### 질문과 에러메세지 --> detail.html의 맨 위쪽 error message
            })
        else: 
            selected_choice.votes += 1
            selected_choice.save()

            return HttpResponseRedirect(reverse('polls:results', args=(question_id,))) ### responseredirect는 post와 세트!! post로 view가 호출된 경우 리다이렉트를 해준다!
                                                                                        ### result url로 리다이렉트 해줌. --> 결과 페이지 보여주기!
                                                                                        ### reverse: url을 하드코딩 하지 않기 위해 app name:url name 사용