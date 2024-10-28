
from django.urls import path, include
from . import views


urlpatterns = [
        path('words/', views.WordsAPIView.as_view()),
        path('words/<int:id>/', views.WordAPIView.as_view()),
        path('practice/spelling/', views.SpellingAPIView.as_view()),
        path('practice/normal/', views.PracticeAPIView.as_view())
]
