from django.urls import path
from .views import LessonListView, LessonDetailView

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:product_id>/', LessonDetailView.as_view(), name='lesson-detail'),
]
