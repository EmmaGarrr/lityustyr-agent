import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_summary(document_text):
    prompt = f"""
You are an expert document summarizer.

Read the document carefully.

Create:

- A short overview
- Important bullet points
- Important facts
- Important names
- Important dates if available

Keep the summary under 300 words.

Document:

{document_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text



# documents/views.py
from .gemini import generate_summary

document.full_text = text

document.pages = pages

document.save() 

replace with :
document.full_text = text

document.pages = pages

summary = generate_summary(text)

document.summary = summary

document.save()



# recommanded prompt 
You are an expert document analyst.

Read the document carefully.

Write a clear summary using this format.

Overview:
(2-3 sentences)

Key Points:
- point 1
- point 2
- point 3

Important Facts:
- fact 1
- fact 2

Important Dates:
- if any

Important Numbers:
- if any

If a section has no information,
write "Not Available."

Do not make up information.

Only use the provided document.
