from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} has access to {self.product.name}"


class Lesson(models.Model):
    products = models.ManyToManyField(Product)
    name = models.CharField(max_length=200)
    video_url = models.URLField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name

class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_time = models.PositiveIntegerField(default=0) 
    last_viewed_date = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=False)  

    def save(self, *args, **kwargs):
        if (self.watched_time / self.lesson.duration) * 100 >= 80:
            self.status = True
        else:
            self.status = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.name}"
