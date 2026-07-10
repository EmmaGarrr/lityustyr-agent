I looked through your architecture. The good news is that **you do NOT need to rewrite your project**. Your code is already well separated into services, so only the AI layer needs to change.

## What needs to change

Currently your project uses **Gemini** for two things:

1. **LLM**

   * Summarization
   * Question Answering

2. **Embeddings**

   * Creating vectors for FAISS
   * Similarity search

These are the only Gemini dependencies in your project. 

---

# Files you need to modify

## 1. requirements.txt

Remove:

```txt
langchain-google-genai
google-generativeai
```

Add:

```txt
groq
langchain-huggingface
sentence-transformers
```

Install:

```bash
pip install groq langchain-huggingface sentence-transformers
```

---

## 2. settings.py

Replace

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

with

```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
```

and in `.env`

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

---

## 3. SummaryService

Currently it contains

```python
ChatGoogleGenerativeAI
```

Replace it with

```python
from groq import Groq
```

This service alone handles all document summarization. 

---

## 4. QAService

Same thing.

Instead of

```python
ChatGoogleGenerativeAI
```

use

```python
Groq()
```

Only the request call changes.

Everything else stays exactly the same.

---

## 5. VectorStoreService

This is the **only place that needs a bigger change.**

Currently you have

```python
GoogleGenerativeAIEmbeddings
```

Replace it with

```python
from langchain_huggingface import HuggingFaceEmbeddings
```

and

```python
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

Everything else (FAISS, similarity search, saving/loading vectors) stays exactly the same. 

---

# What DOES NOT change

These parts remain unchanged:

* ✅ Upload API
* ✅ Models
* ✅ Serializers
* ✅ Views
* ✅ FAISS
* ✅ Chunking
* ✅ Document extraction
* ✅ Cache
* ✅ Chat history
* ✅ Database

---

# Your project architecture after migration

```
Upload
      │
      ▼
Extract Text
      │
      ▼
Chunk
      │
      ▼
SentenceTransformer Embeddings
      │
      ▼
FAISS
      │
      ▼
Question
      │
      ▼
Retrieve Chunks
      │
      ▼
Groq Llama 3.3
      │
      ▼
Answer
```

---

# Estimated work

| File               | Time     |
| ------------------ | -------- |
| requirements.txt   | 2 min    |
| settings.py        | 1 min    |
| SummaryService     | 10 min   |
| QAService          | 10 min   |
| VectorStoreService | 5–10 min |

**Total:** about **30 minutes**.

## My recommendation

Because your code is already modular, **don't patch the existing Gemini classes**. Instead:

* Create `apps/document/ai/groq_service.py` (LLM wrapper).
* Create `apps/document/ai/embedding_service.py` (Hugging Face embeddings).
* Update `SummaryService`, `QAService`, and `VectorStoreService` to use those wrappers.

This keeps the rest of your project unchanged and makes it easy to switch providers again in the future.

Given the architecture you've shared, I can provide a **complete migration** with production-ready code for all affected files, rather than just snippets, so you can replace them directly.



