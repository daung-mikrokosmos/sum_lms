from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
import re
from .base import BaseModel


def validate_phone_no(value):
    if value and not re.match(r'^\+?\d{10,15}$', value):
        raise ValidationError(_('Invalid phone number format. It must contain only digits and be between 10-15 characters long.'))


class Admin(BaseModel):
    class AuthorityLevel(models.IntegerChoices):
        SUPER_USER = 1, _('Super User')
        EDITOR = 2, _('Editor')
        MODERATOR = 3, _('Moderator')

    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=225, null=True, validators=[validate_phone_no])
    authority = models.IntegerField(choices=AuthorityLevel.choices, default=AuthorityLevel.MODERATOR)
    admin_code = models.CharField(max_length=50, unique=True, blank=True)
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

    def save(self, *args, **kwargs):
        # Auto-generate admin_code if not set
        if not self.admin_code:
            last_admin = Admin.objects.order_by('-admin_id').first()
            last_number = 0
            if last_admin and last_admin.admin_code and re.match(r'^SUM-A(\d+)$', last_admin.admin_code):
                last_number = int(re.findall(r'\d+', last_admin.admin_code)[0])
            new_number = last_number + 1
            self.admin_code = f"SUM-A{new_number:06d}"
        super().save(*args, **kwargs)
