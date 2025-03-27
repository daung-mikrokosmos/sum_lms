from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .user import User
from .module_class import Class


class RoleCall(BaseModel):
    rolecall_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'rolecalls'
        unique_together = ('user', 'class_field')  # Ensures a user cannot have duplicate attendance records for the same class

    def __str__(self):
        return f"{self.user.name} - {self.class_field.title}"

    def clean(self):
        super().clean()

        # Ensure the user is not already marked for this class
        if RoleCall.objects.filter(user=self.user, class_field=self.class_field).exists():
            raise ValidationError({
                'user': _('This user has already been marked for this class.')
            })
