from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .module import Module


class Class(BaseModel):
    class_id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    canceled = models.BooleanField(default=False)

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.end_time < self.start_time:
            raise ValidationError({
                'end_time': _('End time cannot be before start time')
            })
