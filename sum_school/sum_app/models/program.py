from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel


def validate_positive_fees(value):
    if value is not None and value < 0:
        raise ValidationError(
            _('%(value)s is not a valid fee amount. It must be a non-negative number.'),
            params={'value': value},
        )


class Program(BaseModel):
    program_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    program_code = models.CharField(max_length=255, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    fees = models.IntegerField(null=True, validators=[validate_positive_fees])

    class Meta:
        db_table = 'programs'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.end_date < self.start_date:
            raise ValidationError({
                'end_date': _('End date cannot be before start date.')
            })

    def get_duration_days(self):
        return (self.end_date - self.start_date).days