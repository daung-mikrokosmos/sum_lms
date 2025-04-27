from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True