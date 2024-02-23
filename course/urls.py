from django.urls import path
from .views import LessonAPIView, LessonDetailAPIView, CourseStatsAPIView

urlpatterns = [
    path('lesson/', LessonAPIView.as_view()),
    path('course/<int:product_id>/lessons/<int:lesson_id>/', LessonDetailAPIView.as_view()),
    path('course-stats/', CourseStatsAPIView.as_view()),
]
