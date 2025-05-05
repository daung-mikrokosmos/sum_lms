from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .module import Module
from .file import File


def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not a positive number'),
            params={'value': value},
        )

class Task(BaseModel):
    class TaskType(models.IntegerChoices):
        ASSIGNMENT = 1, _('Assignment')
        QUIZ = 2, _('Quiz')
        PROJECT = 3, _('Project')
        EXAM = 4, _('Exam')

    task_id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    type = models.IntegerField(choices=TaskType.choices)
    max_score = models.IntegerField(default=100, validators=[validate_positive])
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'tasks'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': _('End date cannot be before start date')
            })
