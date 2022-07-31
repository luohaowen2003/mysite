from django.urls import path
from . import views
urlpatterns = [
    path('hello', views.index, name='index'),
    path('question/<int:qid>', views.question_detail),
    path('vote', views.vote),
]


