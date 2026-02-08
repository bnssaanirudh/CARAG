
---

# 📘 CARAG: Corrective Agentic Retrieval-Augmented Generation

**CARAG** is a full-stack, cloud-native AI information retrieval platform that bridges **static document-grounded knowledge** and **real-time web intelligence**.
Developed as a course project for **M.Tech. CSI3001 – Cloud Computing Methodologies** at **Vellore Institute of Technology (VIT)**, CARAG upgrades traditional *naive RAG* systems into an **agentic, decision-making retrieval architecture**.

---

## 🚀 Overview

Conventional Retrieval-Augmented Generation (RAG) systems rely solely on static, pre-indexed documents. When user queries fall outside this closed domain, such systems either hallucinate answers or fail silently.

**CARAG** addresses this limitation using an **Agentic Router** — a lightweight LLM-based controller that analyzes user intent *before retrieval* and dynamically selects the optimal information source:

* **Private PDFs** for document-centric, factual queries
* **Live Web Search** for ambiguous, open-domain, or time-sensitive queries

This hybrid approach significantly improves **answer faithfulness**, **coverage**, and **user trust**.

---

## ✨ Key Features

* **Agentic Decision-Making**
  Intelligent routing between private document retrieval and live web search, reducing closed-domain failure modes.

* **Cloud-Native Persistence**
  Secure, multi-session conversational history stored in **Google Cloud Firestore**.

* **Secure Authentication**
  User authentication and session management via **Firebase Authentication** (Email/Password).

* **High-Speed Inference**
  Near-real-time responses powered by the **Groq API** (Llama 3.3 70B / Llama 3 8B).

* **Source Transparency**
  Clickable citations and context snippets for verifiable, trustworthy responses.

---

## 🛠️ Technical Stack

| Layer             | Technology                                      |
| ----------------- | ----------------------------------------------- |
| **Frontend**      | Streamlit                                       |
| **Backend**       | Python 3.11+, LangChain                         |
| **LLM Inference** | Groq API (Llama 3.3 70B / Llama 3 8B)           |
| **Vector Store**  | FAISS                                           |
| **Web Search**    | Tavily API                                      |
| **Cloud & Auth**  | Google Cloud Firestore, Firebase Authentication |
| **Embeddings**    | Sentence-Transformers (`all-MiniLM-L6-v2`)      |

---

## 📐 System Architecture

CARAG follows a **three-tier architecture**:

1. **Frontend Layer**

   * Streamlit UI for authentication, PDF uploads, and real-time chat.

2. **Backend Logic Layer**

   * **Agentic Router** determines the optimal retrieval path.
   * **Ingestion Pipeline** chunks PDFs, generates embeddings, and indexes them in FAISS.

3. **Cloud Persistence Layer**

   * Firebase handles authentication and session metadata.
   * Firestore stores conversation history and user state.

---

## 📊 Performance Metrics

Empirical evaluation under moderate load shows:

* **Average Query Response Time:** ~2.9 seconds
* **PDF Ingestion Time:** ~4.5 seconds (50-page document)
* **Routing & Retrieval Accuracy:** 92%
* **Response Faithfulness:** 90% (measured using RAGAS metrics)

---

## 📁 Repository Structure

```text
CARAG/
├── app.py                     # Streamlit frontend
├── agent/
│   ├── router.py               # Agentic routing logic
│   └── prompts.py              # Routing & generation prompts
├── ingestion/
│   ├── pdf_loader.py           # PDF parsing & chunking
│   └── embedder.py             # Embedding generation
├── retrieval/
│   ├── faiss_store.py          # Vector search logic
│   └── web_search.py           # Tavily search wrapper
├── cloud/
│   ├── firestore.py            # Firestore persistence
│   └── auth.py                 # Firebase authentication
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/CARAG.git
cd CARAG
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file using the template below:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
```

> ⚠️ Never commit `.env` files to version control.

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

Open your browser and navigate to:

```
http://localhost:8501
```

---

## 🧪 Usage Workflow

1. Sign up / log in using Firebase Authentication
2. Upload one or more PDFs
3. Ask questions via the chat interface
4. CARAG automatically:

   * Routes the query (PDF vs Web)
   * Retrieves relevant context
   * Generates a grounded response with citations

---

**Contributors:**

* **B. Agasthya Anirudh** (23MID0054)

---

## 🔮 Future Roadmap

* **Post-Retrieval Self-Correction**
  Add a verifier agent to evaluate retrieved chunks *before* final generation.

* **Persistent Vector Databases**
  Replace in-memory FAISS with Pinecone or Weaviate for large-scale, multi-document retrieval.

* **Hybrid Search**
  Combine dense semantic search with sparse BM25 for higher precision.

---

## 📜 License

This project is released for **academic and educational use**.
For commercial usage, please contact the authors.

---
