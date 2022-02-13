"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include ### include는 다른 URLconf.들을 참조할 수 있도록 도와줌

urlpatterns = [
    path('polls/', include('polls.urls')), ### 예를들어 127.0.0.13/polls/ 이런게 들어왔으면, 이걸 잘라(parse)서 polls.urls(앱)로 연결해줌 --> path에서 view 내부로 연결. 
                                            ## 그 중 index의 함수를 실행. 이 앱의 실행 내용을 보고 싶으면 http://127.0.0.1:8000/ 뒤에 polls/를 붙여줘야 함~!!
    path('admin/', admin.site.urls),
]
