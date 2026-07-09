# documents/serializers.py

from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document

        fields = "__all__"

        read_only_fields = (
            "id",
            "pages",
            "full_text",
            "summary",
            "created_at",
        )


# documents/views.py

import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentSerializer


class DocumentUploadView(APIView):

    def post(self, request):
        uploaded_file = request.FILES.get("file")

        if uploaded_file is None:
            return Response(
                {"error": "Please upload a file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        extension = os.path.splitext(uploaded_file.name)[1].lower()

        if extension not in [".pdf", ".docx"]:
            return Response(
                {
                    "error": "Only PDF and DOCX files are allowed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = os.path.splitext(uploaded_file.name)[0]

        document = Document.objects.create(
            title=title,
            file=uploaded_file,
            file_type=extension.replace(".", ""),
        )
from django.urls import path

from .views import DocumentUploadView


urlpatterns = [
    path(
        "documents/",
        DocumentUploadView.as_view(),
        name="document-upload",
    ),
]
        serializer = DocumentSerializer(document)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


# documents/urls.py
