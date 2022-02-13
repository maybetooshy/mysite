import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model): ### 여기에는 질문내용과 발행일이 포함됨! id는 명시하지 않아도 장고에서 알아서 만들어줌.
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published') 

    def __str__(self): ### Question.objects.all() 이런걸 실행하면 몇개 생성됐는지만 보여주고 알고싶은건 안보여줌. 이걸 해결하기 위해 str 함수 추가!
        return self.question_text

    def was_published_recently(self): ### 개발자가 원하는 그냥 함수 만들기도 가능
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now ### 최근 기준을 하루로 바꿔줌. 미래로 시간이 넘어가지 않도록!

    was_published_recently.admin_order_field = 'pub_date' ### 정렬을 발행일 기준으로
    was_published_recently.boolean = True ### 아이콘 모양으로
    was_published_recently.short_description = "Published recently?"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self): 
        return self.choice_text