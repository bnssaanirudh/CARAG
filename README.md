# CARAG: Corrective Agentic Retrieval-Augmented Generation

**CARAG** is a full-stack, cloud-native Al information retrieval platform designed to bridge the gap between static document-grounded knowledge and real-time web intelligence. Developed as a course project for M.Tech. CSI3001 – Cloud Computing Methodologies at **Vellore Institute of Technology (VIT)**, this system transforms traditional "naive" RAG architectures into an active, decision-making agent.

---

## 🚀 Overview

Standard Retrieval-Augmented Generation (RAG) systems often fail when a user's query falls outside their static, indexed content, leading to "hallucinations" or empty responses.

**CARAG** solves this by implementing an **Agentic Router**. This lightweight LLM analyzes user intent before retrieval and dynamically selects the best tool:

* 
**PDF Tool:** For deep, document-centric queries using a local FAISS vector store.


* 
**Web Tool:** For general, ambiguous, or time-sensitive questions using the Tavily Search API.



---

## ✨ Key Features

* 
**Agentic Decision-Making:** Uses a routing layer to choose between private documents and the live web, reducing closed-domain failure modes.


* 
**Cloud Persistence:** Integrated with **Google Cloud Firestore** to provide secure, multi-session conversational history and user-specific continuity.


* 
**Secure Authentication:** User sessions are managed via **Firebase Authentication** (Email/Password).


* 
**High-Speed Inference:** Leverages the **Groq API** (Llama 3.3 70B) for near-instant generative synthesis.


* 
**Source Transparency:** Returns clickable citations and context snippets to ensure verifiability and trust.



---

## 🛠️ Technical Stack

| Component | Technology |
| --- | --- |
| **Frontend** | Streamlit 

 |
| **Backend** | Python 3.11+, LangChain (logic) 

 |
| **AI Inference** | Groq API (Llama 3.3 70B / Llama 3 8B) 

 |
| **Vector Database** | FAISS (Facebook AI Similarity Search) 

 |
| **Web Search** | Tavily API 

 |
| **Cloud/DB** | Google Cloud Firestore & Firebase Auth 

 |
| **Embeddings** | Sentence-Transformers (`all-MiniLM-L6-v2`) 

 |

---

## 📐 System Architecture

The system follows a three-tier model:

1. 
**Frontend Layer:** Streamlit interface for PDF uploads and real-time chat.


2. 
**Backend Logic:** An "Agentic Router" interprets the query, while the Ingestion Module processes PDFs into semantic chunks and embeddings.


3. 
**Cloud Persistence Layer:** Firebase manages authentication and stores the interaction history metadata.



---

## 📈 Performance Metrics

Based on system testing, CARAG maintains high efficiency even under moderate load:

* Avg. Query Response Time: ~2.9 seconds.


* 
**Document Processing:** ~4.5 seconds for a 50-page PDF.


* 
**Context Relevance:** 92% accuracy in routing and retrieval.


* 
**Response Faithfulness:** 90% (measured via RAGAS metrics).



---

## 🧑‍💻 The Team


* B. Agasthya Anirudh

---

## 🔮 Future Roadmap

* 
**Post-Retrieval Evaluator:** Moving from pre-retrieval routing to a full self-corrective loop that scores retrieved chunks before deciding to hit the web.


* 
**Persistent Vector Storage:** Migrating from in-memory FAISS to persistent databases like Pinecone or Weaviate for long-term multi-document libraries.


* 
**Hybrid Search:** Fusing semantic vector search with keyword-based BM25 for better precision.



Would you like me to generate a step-by-step setup guide for the API configurations mentioned in the Appendix?
