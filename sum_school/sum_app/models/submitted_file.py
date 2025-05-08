from django.db import models
from .base import BaseModel
from .file import File
from .submitted_task import SubmittedTask

class SubmittedFile(BaseModel):
    submitted_file_id = models.AutoField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    submitted_task = models.ForeignKey(SubmittedTask, on_delete=models.CASCADE)

    class Meta:
        db_table = 'submitted_files'

    def __str__(self):
        return f"{self.submitted_task.student.name} - {self.file.original_name}"