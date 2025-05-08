from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from .base import BaseModel


def validate_phone_no(value):
    # Basic validation to ensure phone number contains only digits and is of valid length
    if value and not re.match(r'^\+?\d{10,15}$', value):
        raise ValidationError(_('Invalid phone number format. It must contain only digits and be between 10-15 characters long.'))


class User(BaseModel):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField(null=True)
    phone_no = models.CharField(max_length=225, null=True, validators=[validate_phone_no])
    is_teacher = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    user_code = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        # Ensure date_of_birth is in the past
        if self.date_of_birth and self.date_of_birth >= date.today():
            raise ValidationError({
                'date_of_birth': _('Date of birth cannot be in the future.')
            })