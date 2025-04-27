from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .user import User
from .program import Program


class Registration(BaseModel):
    registration_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    student_code = models.CharField(max_length=50, unique=True)
    scholared = models.BooleanField(default=False)
    teacher_flag = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'registrations'
        unique_together = ('user', 'program')  # Ensures a user cannot register for the same program twice

    def __str__(self):
        return f"{self.user.name} - {self.program.name}"

    def clean(self):
        super().clean()

        # Ensure that a user is either a teacher or a student, not both
        if self.teacher_flag and self.scholared:
            raise ValidationError({
                'teacher_flag': _('A user cannot be both a teacher and a scholar in the same registration.')
            })