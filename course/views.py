from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import models
from .serializers import LessonSerializer, LessonStatusSerializer, CourseStatSerializer


class LessonAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        course = models.Course.objects.filter(course_access__user=user)
        lessons_access = models.Lesson.objects.filter(course__in=course)
        return models.LessonStatus.objects.filter(
            user=user, lesson__in=lessons_access
        ).select_related('lesson')
    
class LessonDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonStatusSerializer
    queryset = models.LessonStatus.objects.select_related(
        'lesson'
    ).all()

    def get_object(self):
        user = self.request.user
        course_id = self.kwargs.get('course_id')
        lesson_id = self.kwargs.get('lesson_id')

        course = models.Course.objects.filter(pk=course_id, course_access__user=user).first()
        if course:
            lesson = models.Lesson.objects.filter(pk=lesson_id, products=course).first()
            return lesson
        else:
            return None
        

class CourseStatsAPIView(generics.ListAPIView):
    serializer_class = CourseStatSerializer

    def get_queryset(self):
        queryset = models.Course.objects.all()

        for course in queryset:
            watched_lessons_count = models.Access.objects.filter(course_access=course, is_completed=True).count()

            total_watched_time = models.Access.objects.filter(course_access=course, is_completed=True).aggregate(
                total_time=models.Sum('watched_time_seconds')
            )

            enrolled_students_count = models.Access.objects.filter(course=course).count()

            total_users_count = models.User.objects.count()
            course_access_count = models.Access.objects.filter(course_access=course).count()
            purchase_percentage = (course_access_count / total_users_count) * 100 if total_users_count != 0 else 0

            course.watched_lessons_count = watched_lessons_count
            course.total_watched_time = total_watched_time['total_time'] if total_watched_time['total_time'] else 0
            course.enrolled_students_count = enrolled_students_count
            course.purchase_percentage = purchase_percentage