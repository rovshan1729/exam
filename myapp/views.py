from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Product, Lesson, LessonView
from .serializers import LessonViewSerializer

class LessonListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonViewSerializer

    def get_queryset(self):
        user = self.request.user
        products = Product.objects.filter(access__user=user)
        lessons = Lesson.objects.filter(product__in=products)
        return LessonView.objects.filter(user=user, lesson__in=lessons)

class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonViewSerializer
    queryset = LessonView.objects.all()

    def get_object(self):
        user = self.request.user
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(pk=product_id, access__user=user)
            lessons = product.lesson_set.all()
            return LessonView.objects.filter(user=user, lesson__in=lessons)
        except Product.DoesNotExist:
            return Response({"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN)
