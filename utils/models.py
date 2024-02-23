from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusType(models.TextChoices):
    seen = 'Просмотрено'
    not_seen = 'Не просмотрено'


