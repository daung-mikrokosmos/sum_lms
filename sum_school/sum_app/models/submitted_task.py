from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .user import User
from .task import Task


class SubmittedTask(BaseModel):
    submitted_task_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    checked_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'submitted_tasks'

    def __str__(self):
        return f"{self.student.name} - {self.task.title}"

    def clean(self):
        super().clean()

        # Ensure score is within valid range (0 to max_score of the task)
        if self.score < 0 or self.score > self.task.max_score:
            raise ValidationError({
                'score': _('Score must be between 0 and the max score of the task.')
            })