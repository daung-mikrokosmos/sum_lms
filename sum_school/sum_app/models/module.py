from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .program import Program
from .user import User


def validate_positive_credit(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not a valid credit amount. It must be a positive number.'),
            params={'value': value},
        )


class Module(BaseModel):
    module_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    module_code = models.CharField(max_length=50, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    credit = models.SmallIntegerField(validators=[validate_positive_credit])

    class Meta:
        db_table = 'modules'

    def __str__(self):
        return self.name
