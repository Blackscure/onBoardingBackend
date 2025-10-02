from django.db import models
import uuid
from forms.models import Form

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="submissions")
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class FileUpload(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    field_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
