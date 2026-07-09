import fitz
from docx import Document


def extract_pdf_text(file_path):
    """
    Read a PDF file and return:

    text
    page count
    """

    pdf = fitz.open(file_path)

    text = ""

    for page in pdf:
        text += page.get_text()

    total_pages = len(pdf)

    pdf.close()

    return text, total_pages




def extract_docx_text(file_path):
    """
    Read a DOCX file and return:

    text
    page count
    """

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text, None


import os


def extract_document(file_path):
    """
    Detect file type and call
    the correct extraction function.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    if extension == ".docx":
        return extract_docx_text(file_path)

    raise ValueError("Unsupported file type.")



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
                {"error": "Only PDF and DOCX files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = os.path.splitext(uploaded_file.name)[0]

        document = Document.objects.create(
            title=title,
            file=uploaded_file,
            file_type=extension.replace(".", ""),
        )

        file_path = document.file.path

        text, pages = extract_document(file_path)

        document.full_text = text

        document.pages = pages

        document.save()

        serializer = DocumentSerializer(document)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )






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
        extra_kwargs = {
            "full_text": {"write_only": True},
        }
