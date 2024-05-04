from django.db import models


class ModelProperties(models.Model):
    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(blank=True, auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
