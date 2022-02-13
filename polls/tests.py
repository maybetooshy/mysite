from asyncio import queues
from django.test import TestCase 
from django.utils import timezone
from django.urls import reverse
import datetime

from .models import Question

# 테스트 코드!!! 오류를 미리 잡거나 예외처리를 해주는 중요한 코드!!
# 앞 머리를 test로 만들어줘야 좋음

class QuestionModelTests(TestCase): ### 미래 시간으로 생성된 질문에 대한 오류 처리. TestCase를 상속!

    def test_was_published_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_publised_recently(), False) ### 과거에 만들어졌냐? false가 나오길 기대! true라는 결과가 나와서 models 코드 수정! --> test 통과되도록 !

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        
        ###If no questions exist, an appropriate message is displayed.
        ### 테스트 클라이언트가 요청하여 원하는 값이 나오는지 확인하는 것 !!
        
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200) ### 상태코드 같은 값?
        self.assertContains(response, "No polls are available.") ### 포함되어 있음?
        self.assertQuerysetEqual(response.context['latest_question_list'], []) ### 쿼리 셋

    def test_past_question(self):
        create_question(question_text="Past question", days=-30) ### 과거 데이터 하나 만들어서 
        response = self.client.get(reverse('polls:index')) ### 호출

        self.assertQuerysetEqual( ### 데이터가 안나오면 문제가 있음
            response.context['latest_question_list'],
            ['<Question: Past question>'] ### 데이터가 나오는지 확인
        )

    def test_future_question(self):
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(response.context['latest_question_list'], []) ### 미래 데이터를 만들어. 데이터가 나오면 문제가 있는 것

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question", days=-30) ### 과거, 미래 하나씩
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>'] ### 과거 데이터만 나오기를 기대하는 것!
        )

    def test_two_past_question(self):
        create_question(question_text="Past question 1.", days=-30) ### 과거 데이터 두개
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>'] ### 두개 데이터가 나오기를 기대
        )
