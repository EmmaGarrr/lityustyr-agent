def ask_from_summary(summary, question):

    prompt = f"""
You are an AI assistant.

Answer ONLY from the summary below.

If the answer is not present,

reply exactly:

I could not find the answer in the document summary.

Summary:

{summary}

Question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text



def ask_from_document(full_text, question):

    MAX_CHARACTERS = 80000

    if len(full_text) > MAX_CHARACTERS:
        full_text = full_text[:MAX_CHARACTERS]

    prompt = f"""
You are an AI assistant.

Answer ONLY using the document below.

Do not invent information.

If the answer is not available,

reply exactly:

I could not find the answer in the document.

Document:

{full_text}

Question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


# documents/views.py
from .gemini import (
    ask_from_document,
    ask_from_summary,
)


class AskSummaryView(APIView):

    def post(self, request, pk):

        question = request.data.get("question")

        if not question:
            return Response(
                {
                    "error": "Question is required."
                },
                status=400,
            )

        try:
            document = Document.objects.get(pk=pk)

        except Document.DoesNotExist:
            return Response(
                {
                    "error": "Document not found."
                },
                status=404,
            )

        answer = ask_from_summary(
            document.summary,
            question,
        )

        return Response(
            {
                "question": question,
                "answer": answer,
            }
        )




# full

class AskDocumentView(APIView):

    def post(self, request, pk):

        question = request.data.get("question")

        if not question:
            return Response(
                {
                    "error": "Question is required."
                },
                status=400,
            )

        try:
            document = Document.objects.get(pk=pk)

        except Document.DoesNotExist:
            return Response(
                {
                    "error": "Document not found."
                },
                status=404,
            )

        answer = ask_from_document(
            document.full_text,
            question,
        )

        return Response(
            {
                "question": question,
                "answer": answer,
            }
        )



# updated urls :
from django.urls import path

from .views import (
    AskDocumentView,
    AskSummaryView,
    DocumentDetailView,
    DocumentView,  # if you combined GET/POST as discussed
)

urlpatterns = [
    path(
        "documents/",
        DocumentView.as_view(),
        name="documents",
    ),

    path(
        "documents/<int:pk>/",
        DocumentDetailView.as_view(),
        name="document-detail",
    ),

    path(
        "documents/<int:pk>/ask-summary/",
        AskSummaryView.as_view(),
        name="ask-summary",
    ),

    path(
        "documents/<int:pk>/ask-document/",
        AskDocumentView.as_view(),
        name="ask-document",
    ),
]
