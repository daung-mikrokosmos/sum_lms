from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
import re
from .base import BaseModel


def validate_phone_no(value):
    # Basic validation to ensure phone number contains only digits and is of valid length
    if value and not re.match(r'^\+?\d{10,15}$', value):
        raise ValidationError(_('Invalid phone number format. It must contain only digits and be between 10-15 characters long.'))


class Admin(BaseModel):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=225, null=True, validators=[validate_phone_no])
    authority = models.IntegerField(default=1)
    admin_code = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'admins'

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def clean(self):
        super().clean()
