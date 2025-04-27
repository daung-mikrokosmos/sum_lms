from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .program import Program
from .user import User


class Leave(BaseModel):
    leave_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approve_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'leaves'

    def __str__(self):
        return f"{self.user.name} - {self.start_date}"

    def clean(self):
        super().clean()
        if self.end_date < self.start_date:
            raise ValidationError({
                'end_date': _('End date cannot be before start date')
            })