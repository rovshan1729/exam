from django.db import models
from django.contrib.auth.models import User
from utils.models import BaseModel, StatusType

class Course(BaseModel):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    watched_lessons_count = models.IntegerField(default=0)
    total_watched_time = models.IntegerField(default=0)
    enrolled_students_count = models.IntegerField(default=0)
    purchase_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return self.title
    

class Access(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='course_access'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course_access'
    )

    is_completed = models.BooleanField(default=False)
    

class Lesson(BaseModel):
    title = models.CharField(max_length=128)
    video_url = models.URLField()
    duration_seconds = models.IntegerField(default=0)

    courses = models.ManyToManyField(Course, related_name='lessons')

    def __str__(self):
        return self.title


class LessonStatus(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_lesson_status')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_status')

    watched_time = models.PositiveIntegerField(default=0) 
    last_viewed_date = models.DateTimeField(blank=True, null=True) 

    status = models.CharField(max_length=256, choices=StatusType.choices, default=StatusType.not_seen)


    def save(self, *args, **kwargs):
        if self.lesson.duration * 0.8 >= self.watched_time:
            self.status = StatusType.seen
        else:
            self.status = StatusType.not_seen
        super().save(*args, **kwargs)


    def __str__(self):
        return self.lesson.title
