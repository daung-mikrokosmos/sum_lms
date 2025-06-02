from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .user import User
from .program import Program


class Registration(BaseModel):
    class PaymentStatus(models.IntegerChoices):
        NOT_PAID = 0, _('Not Paid')
        PAYING = 1, _('Paying')
        PAID = 2, _('Paid')
        SCHOLARED = 3, _('-')

    registration_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    student_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    scholared = models.BooleanField(default=False)
    teacher_flag = models.BooleanField(default=False)
    payment_status = models.IntegerField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_PAID
    )
    is_new = models.BooleanField(default=True)

    class Meta:
        db_table = 'registrations'
        unique_together = ('user', 'program')  # Prevents duplicate registration per user per program

    def __str__(self):
        return f"{self.user.name} - {self.program.name}"

    def clean(self):
        super().clean()
        # Prevent both teacher and scholar flags at the same time
        if self.teacher_flag and self.scholared:
            raise ValidationError({
                'teacher_flag': _('A user cannot be both a teacher and a scholar in the same registration.')
            })

    def save(self, *args, **kwargs):
        if self._state.adding and not self.teacher_flag and not self.student_code:
            # Count existing students in the same program
            existing_count = Registration.objects.filter(
                program=self.program,
                teacher_flag=False
            ).count()
            
            # Add 1 to the count and pad with zeros to 6 digits
            number = existing_count + 1
            padded_number = f"{number:03d}"
            
            # Compose student_code with program_code and padded number
            self.student_code = f"{self.program.program_code}{padded_number}"
            
            # Optional: Check for uniqueness and increment if needed (like in the first example)
            while Registration.objects.filter(student_code=self.student_code).exists():
                number += 1
                padded_number = f"{number:03d}"
                self.student_code = f"{self.program.program_code}{padded_number}"

        super().save(*args, **kwargs)
