from django.contrib import admin
from .models import Question, Choice
# Register your models here.

class ChoiceInline(admin.TabularInline): ### StackedInline, TabularInline 등 여러 형태 있음
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently') ### 데이터 필드에 Question밖에 안보이는걸 보완!

    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        ('Date information',    {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline]

    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice) ### questionadmin에서 choice를 관리할 수 있도록 바꿀거임! inline


