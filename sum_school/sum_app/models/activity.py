from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .module import Module
from django.utils import timezone


class Activity(BaseModel):
    class ActivityType(models.IntegerChoices):
        PRESENTATION = 1, _('Presentation')
        DEBATE = 2, _('Debate')

    activity_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(unique=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    type = models.IntegerField(choices=ActivityType.choices)
    schedule = models.DateField()

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return self.title

    @property
    def is_due(self):
        return self.schedule < timezone.localdate()