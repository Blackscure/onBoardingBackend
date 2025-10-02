from django.db import models
import uuid
from django.conf import settings


class Form(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="forms"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    FIELD_TYPES = [
        ("text", "Text"),
        ("textarea", "Paragraph Text"),
        ("number", "Number"),
        ("decimal", "Decimal / Currency"), 
        ("date", "Date"),
        ("time", "Time"),
        ("datetime", "Date & Time"),
        ("email", "Email"),
        ("phone", "Phone Number"),
        ("url", "URL / Website"),
        ("password", "Password"),
        ("dropdown", "Dropdown"),
        ("radio", "Radio Buttons"),
        ("checkbox", "Checkbox"),
        ("checkbox_group", "Checkbox Group"),
        ("file", "File Upload"),
        ("image", "Image Upload"),
        ("signature", "Signature / Drawing Pad"),
        ("boolean", "Yes/No Toggle or Switch"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)
    options = models.JSONField(blank=True, null=True)
    validation_rules = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.label} ({self.type})"
