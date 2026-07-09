# documents/models.py

from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)

    file = models.FileField(upload_to="documents/")

    file_type = models.CharField(max_length=20)

    pages = models.IntegerField(null=True, blank=True)

    full_text = models.TextField(blank=True)

    summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# documents/admin.py
from django.contrib import admin

from .models import Document


admin.site.register(Document)
