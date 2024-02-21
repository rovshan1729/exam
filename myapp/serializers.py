from rest_framework import serializers
from .models import Lesson, LessonView

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'video_url',
            'duration',
        )

class LessonViewSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = LessonView
        fields = (
            'lesson',
            'watched_time',
            'status',
            'last_viewed_date',
        )
