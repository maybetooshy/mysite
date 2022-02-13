from django.urls import path

from . import views

### 클라이언트가 polls라고 호출하면, view -> index 호출됨.
### id로 5를 전달해줫으면, view -> detail을 호출함. 

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    # path('', views.index, name='index'),    
    path('', views.IndexView.as_view(), name='index'), ### 제너릭 형태에서는 미리 저장된 as_view 함수로 호출해 view를 호출함. pk만 명시해주면 됨. 
                                                       ### pk는 DB 내의 하나의 열, 하나의 데이터를 구분할 수 있는 값

    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'), ### 장고에서 지원하는 url 패턴을 명시해줘야 함. view에 있는 파라미터 중 question_id와 일치해야 함. 그 함수에 인자로 사용됨.
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]