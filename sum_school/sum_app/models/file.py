from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel


def validate_file_size(value):
    if value is not None and value <= 0:
        raise ValidationError(
            _('%(value)s is not a valid file size. It must be a positive number.'),
            params={'value': value},
        )

class File(BaseModel):
    file_id = models.AutoField(primary_key=True)
    original_name = models.CharField(max_length=225)
    type = models.IntegerField()
    size = models.IntegerField(null=True, validators=[validate_file_size])
    url = models.CharField(max_length=225)

    class Meta:
        db_table = 'files'

    def __str__(self):
        return self.original_name