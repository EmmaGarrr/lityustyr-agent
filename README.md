# lityustyr-agent

Step 1 Create Virtual Environment

Open terminal.

python -m venv venv

Activate it.

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
Step 2 Install Packages

Install everything.

pip install django
pip install djangorestframework
pip install python-dotenv
pip install google-genai
pip install pymupdf
pip install python-docx

or install everything together

pip install django djangorestframework python-dotenv google-genai pymupdf python-docx
Step 3 Freeze Requirements
pip freeze > requirements.txt

Now your requirements.txt will contain all installed packages.

Step 4 Create Project
django-admin startproject document_ai .

Notice the dot.

The dot creates project in current folder.

Step 5 Create App
python manage.py startapp documents

Now your folder becomes

document_ai/

documents/

manage.py
Step 6 Open settings.py

Go to

document_ai/settings.py
Step 7 Add Installed Apps

Find

INSTALLED_APPS = [

Replace with

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",

    "documents",
]

Nothing fancy.

Just add DRF and our app.

Step 8 Configure Media

At bottom of settings.py

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

Why?

Because uploaded files should go inside

media/
Step 9 Environment Variables

Create file

.env

Inside

GEMINI_API_KEY=YOUR_API_KEY_HERE

Never hardcode API keys.

Step 10 Read .env

Top of settings.py

from pathlib import Path

Add

import os

from dotenv import load_dotenv

Then after

BASE_DIR = Path(__file__).resolve().parent.parent

Add

load_dotenv(BASE_DIR / ".env")

Now Django can read environment variables.

Step 11 Secret Key (Optional for this assignment)

You can leave Django's default secret key since this is a local test project.

Step 12 Configure URLs

Open

document_ai/urls.py

Replace with

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("documents.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

What this does:

/api/

↓

documents app

Also lets Django serve uploaded files locally.

Step 13 Create URLs for App

Create file

documents/urls.py

Inside

from django.urls import path

urlpatterns = [

]

We'll add APIs later.

Step 14 Run Server
python manage.py migrate

Then

python manage.py runserver

If everything is correct, open

http://127.0.0.1:8000/

You may see Django's default "The install worked successfully!" page or a 404 page because we haven't added any endpoints yet. Either is fine—the important thing is that the server starts without errors.

Why We Chose These Packages
Package	Why we need it
Django	Main backend framework
DRF	Create REST APIs easily
PyMuPDF	Read PDF files and extract text
python-docx	Read DOCX files
google-genai	Call Gemini API
python-dotenv	Read API key from .env

No extra libraries.

No unnecessary complexity.

f the project.
