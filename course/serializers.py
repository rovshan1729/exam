from rest_framework import serializers
from . import models


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = (
            'id',
            'title',
            'video_url',
            'products',
            'created_at'
            'updated_at'
        )


class LessonStatusSerializer(serializers.ModelSerializer):
    lesson = serializers.StringRelatedField(source='title', read_only=True)

    class Meta:
        model = models.LessonStatus
        fields = (
            'id',
            'user',
            'lesson',
            'watched_time',
            'last_viewed_date',
            'status',
            'created_at'
            'updated_at'
        )


class CourseStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = (
            'id',
            'title',
            'watched_lessons_count',
            'total_watched_time',
            'enrolled_students_count',
            'purchase_percentage',
            'created_at',
            'updated_at',
        )


