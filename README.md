# 📈 AI Financial Analyst — RAG System

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-1C3C3C)](https://python.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?logo=openai&logoColor=white)](https://openai.com/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-5A45FF)](https://www.trychroma.com/)


An intelligent Retrieval-Augmented Generation (RAG) application for querying company documents using natural language. The system extracts PDF text, creates overlapping chunks, generates semantic embeddings, stores them in ChromaDB, retrieves relevant context for a question, and uses GPT-4o to generate a concise, grounded answer with document/page references.

A core design principle is **evidence-first answering**: when the uploaded document does not contain the requested information, the system should explicitly say that the information is unavailable instead of inventing a financial figure.

---

## 📚 Table of Contents

- [Project Overview](#-project-overview)
- [Source Document](#-source-document)
- [Assignment Alignment](#-assignment-alignment)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Chunking Strategy](#-chunking-strategy)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [RAG Workflow](#-rag-workflow)
- [Evaluation Questions and Results](#-evaluation-questions-and-results)
- [Screenshots](#-screenshots)
- [Limitations and Lessons Learned](#-limitations-and-lessons-learned)
- [Demo Video](#-demo-video)
- [Submission Checklist](#-submission-checklist)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

The **AI Financial Analyst** is a document-question-answering system built using the Retrieval-Augmented Generation pattern.

The application is intended to help an analyst quickly find information inside lengthy company reports without manually searching every page.

### High-level workflow

```text
PDF Document
     │
     ▼
Text Extraction
     │
     ▼
Recursive Chunking
     │
     ▼
OpenAI Embeddings
     │
     ▼
Persistent ChromaDB
     │
     ▼
User Question
     │
     ▼
Semantic Retrieval
     │
     ▼
GPT-4o
     │
     ▼
Grounded Answer + Source
```

The system combines retrieval and generation so that the language model receives relevant document context before producing an answer.

---

## 🏢 Source Document

### Company

**Meridian Components Pvt. Ltd.**

The supplied document identifies Meridian Components as an automotive electronic control unit and wiring-harness company, with its registered office in Chakan Industrial Area, Pune and plants in Chakan and Hosur.


### Important source-scope note

The supplied PDF is a **Supply Chain Performance Review**, not a conventional quarterly financial-results statement. Therefore, some standard financial questions in the assignment cannot be answered from this document.

The RAG system should **not hallucinate** values for revenue, net profit, operating margin, or dividends when those figures are absent. Instead, it should report that the information is not available in the uploaded document.

---



## ✨ Key Features

### 📄 PDF Document Ingestion

Users can upload one or more PDF documents through the Streamlit interface.

### 🧩 Intelligent Chunking

Extracted PDF text is divided into overlapping chunks so that related information remains available during retrieval.

### 🧠 Semantic Search

The application uses OpenAI embeddings and ChromaDB to find document passages that are semantically relevant to the user's question.

### 🤖 GPT-4o Question Answering

Retrieved passages are supplied to GPT-4o as context for generating a concise response.

### 📌 Source References

Answers can be accompanied by the originating document and page number, allowing users to verify the information against the original report.

### 🛑 Hallucination Prevention

The application is designed to refuse unsupported questions instead of creating unsupported financial information.

### 💾 Persistent Vector Store

ChromaDB is stored locally so indexed document data can persist across application restarts.

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │     PDF Documents    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   pypdf Extraction   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Recursive Splitter   │
                         │ 1000 chars           │
                         │ 150 char overlap     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ OpenAI Embeddings    │
                         │ text-embedding-3-    │
                         │ small                │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Persistent ChromaDB  │
                         └──────────┬───────────┘
                                    │
                         User      │
                         Question  ▼
                         ┌──────────────────────┐
                         │ Similarity Retrieval │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       GPT-4o         │
                         │ Grounded Prompt      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Answer + References  │
                         └──────────────────────┘
```

---

## 💻 Tech Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| RAG orchestration | LangChain |
| PDF processing | `pypdf` |
| Text splitting | Recursive character splitter |
| Embedding model | OpenAI `text-embedding-3-small` |
| Language model | OpenAI GPT-4o |
| Vector database | ChromaDB |
| Environment management | `python-dotenv` |

---

## ✂️ Chunking Strategy

The project uses:

```text
Chunk size:    1,000 characters
Chunk overlap:   150 characters
Method:        Recursive character splitting
```

### Why this configuration?

A 1,000-character chunk keeps related financial and operational information together while remaining small enough for focused semantic retrieval.

The 150-character overlap helps preserve context when a sentence, figure, or explanation crosses a chunk boundary.

Both values fall within the assignment's specified ranges.

---

## 📁 Project Structure

```text
RAG-Project/
│
├── data/
│   └── Meridian_Q1_FY2025-26.pdf
│
├── chroma_db/
│   └── ...                       # Persistent vector store
│
├── assets/
│   ├── upload.png
│   ├── indexing.png
│   ├── answer.png
│   └── refusal.png
│
├── app.py                        # Streamlit application
├── ingest.py                     # PDF ingestion and indexing
├── rag.py                        # Retrieval and answer generation
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── .gitignore                    # Git exclusions
└── README.md                     # Project documentation
```


---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/askikumari8-web/RAG-Project.git
cd RAG-Project
```

### 2. Create a Virtual Environment

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### `.env.example`

Commit only the template:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### `.gitignore`

Make sure the real secret and generated vector database are excluded:

```gitignore
.env
venv/
__pycache__/
*.pyc
chroma_db/
```

**Never commit your real OpenAI API key to GitHub.**

---

## ▶️ Usage

Start the Streamlit application:

```bash
streamlit run app.py
```

### 1. Upload Documents

Upload the quarterly/company PDF through the document uploader.

### 2. Index the Documents

Click:

```text
Index Documents
```

The application should process the PDF, create chunks, generate embeddings, and store them in ChromaDB.

### 3. Ask a Question

Example:

```text
What were the major supply-chain risks carried into Q2?
```

### 4. Review the Answer

The application should display:

- A concise answer
- Relevant source document
- Page number(s)
- Supporting context where applicable

---

## 🔄 RAG Workflow

### Step 1 — Read

`pypdf` extracts text from the uploaded PDF.

### Step 2 — Chunk

The text is divided into 1,000-character chunks with 150 characters of overlap.

### Step 3 — Embed

Each chunk is transformed into an embedding using:

```text
text-embedding-3-small
```

### Step 4 — Store

Embeddings and document metadata are persisted in ChromaDB.

### Step 5 — Retrieve

The user's question is embedded and the most relevant chunks are retrieved.

### Step 6 — Generate

The retrieved context is passed to GPT-4o.

### Step 7 — Cite

The response identifies the source PDF and page number.

### Step 8 — Refuse When Necessary

If the retrieved context does not contain the requested information, the system should respond that the information is not available in the uploaded documents.

---

# 🧪 Evaluation Questions and Results

The following evaluation uses the **Meridian Components Pvt. Ltd. — Supply Chain Performance Review, Q1 FY 2025-26** supplied for this project.

---


### 1. What was the total procurement spend in the most recent quarter loaded?

- **Answer:** Total procurement spend in Q1 FY 2025-26 stood at **₹81.6 crore** across the six primary suppliers, against a planned budget of ₹79.4 crore.

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Page 1)

### 2. Compare the spend across all suppliers. Which supplier had the highest spend?

- **Answer:** The supplier spend breakdown for Q1 is:
  1. **Shenzhen Rui Electronics:** ₹21.9 crore (Highest)

  2. **Trident Circuit Boards:** ₹17.3 crore

  3. **Baltic Wire GmbH:** ₹15.2 crore

  4. **Nexa Polymers Ltd:** ₹12.4 crore

  5. **Kaveri Metals Pvt Ltd:** ₹8.7 crore

  6. **Sunrise Connectors:** ₹6.1 crore

     **Shenzhen Rui Electronics** had the highest spend at ₹21.9 crore.

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Page 1)

### 3. How did on-time delivery and incoming quality compare with their quarterly targets?

- **Answer:** On-time delivery averaged **88.4%** against a target of **95%**. Incoming quality deteriorated to **480 defects per million (PPM)** against a target of **250 PPM**.

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Page 1)

### 4. What did management say about the demand outlook and the June forecast miss?

- **Answer:** Management noted that Q1 was difficult for inbound supply. The forecast accuracy had a mean absolute percentage error of 23% against a 15% target, driven by an unannounced two-week shutdown at a major customer's Pune assembly plant in June (actual ECU demand dropped to 131,000 units vs. a 162,000 unit forecast).

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Pages 1, 3)

### 5. Which supplier had the highest defect rate, and what corrective actions were triggered?

- **Answer:** **Kaveri Metals Pvt Ltd** had the highest defect rate at **1,150 PPM** due to burr formation on stamped contacts. Under Policy Clause 6.3, Kaveri bore the cost of rework (standard rate ₹120/unit) and was placed under 100% incoming inspection dock containment.

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Pages 1–2), `Meridian_Procurement_Policy_Handbook_v4.2.pdf` (Page 2)

### 6. What was the freight spend variance, and why did the budget overrun happen?

- **Answer:** Inbound freight spend was **₹6.42 crore** against a budget of **₹5.10 crore** (a 25.9% overrun). This was caused by 9 emergency air shipments from Shenzhen taken in May and June at ₹11,20,000 per shipment to avert production line stoppages.

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Page 2)

### 7. Which policy penalty clause applies to Shenzhen Rui Electronics for delivery failure?

- **Answer:** Shenzhen Rui recorded on-time delivery of 79.5% in Q1 and 83.2% in Q4 (two consecutive quarters below 85%). This triggers **Clause 6.2**, resulting in a debit note equal to **2% of the quarterly invoice value** and requiring a formal improvement plan within 15 working days.

- **Source:** `Meridian_Procurement_Policy_Handbook_v4.2.pdf` (Page 2), `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf`(Page 1)

### 8. What are the key supply chain risks carried into Q2?

- **Answer:** The 5 key risks cited are:
  1. **Single-source dependency** on Shenzhen Rui Electronics for microcontrollers.

  2. **Port congestion and customs delays** at Nhava Sheva adding \~2.9 days per ocean lane.

  3. **Copper price escalation** (+14% YoY) prompting price increase requests from Baltic Wire.

  4. **Regulatory BIS certification** changes taking effect in October 2025.

  5. **Customer concentration**, with top 3 customers accounting for 71% of revenue.

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Page 3)

### 9. Give me a three-line summary of Q1 supply chain performance for executive leadership.

- **Answer:**
  - Q1 procurement spend closed at ₹81.6 crore, with on-time delivery underperforming at 88.4% and defect rates rising to 480 PPM.

  - Production recorded 41 downtime hours costing ₹1.9 crore, driven primarily by microcontroller supply shortages from Shenzhen Rui Electronics.

  - Total inventory rose to ₹68.4 crore due to emergency buffer building, with qualification of Anh Long Semiconductors (Vietnam) underway to establish dual sourcing.

- **Source:** `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf` (Pages 1–3)

### 10. Trap Question: What was the CEO's personal stock holding in Meridian Components in 2015?

- **Answer:** **The requested information is not available in the uploaded documents.**

- **Source:** *None (System prompt honest refusal enforced)*

---

# 📊 Key Facts Extracted from the PDF

| Metric | Q1 FY 2025-26 |
|---|---:|
| Procurement spend | ₹81.6 crore |
| Planned procurement spend | ₹79.4 crore |
| On-time delivery | 88.4% |
| On-time delivery target | 95% |
| Incoming defects | 480 PPM |
| Incoming defect target | 250 PPM |
| Line stoppages | 7 |
| Production downtime | 41 hours |
| Estimated lost output | ₹1.9 crore |
| Inventory value at 30 Jun 2025 | ₹68.4 crore |
| Inventory value at 31 Mar 2025 | ₹61.2 crore |
| Inventory turns | 6.8 |
| Inventory turns target | 8.0 |
| Inbound freight spend | ₹6.42 crore |
| Freight budget | ₹5.10 crore |
| Freight overrun | 25.9% |
| Forecast MAPE | 23% |
| Forecast MAPE target | 15% |
| Customer concentration | Top 3 customers = 71% of quarterly revenue |



---

# ⚠️ Limitations and Lessons Learned

### 1. The supplied PDF is not a conventional financial statement

The document is a **Supply Chain Performance Review**, so standard financial metrics such as net profit, operating margin, and dividend information are absent.

This is an important RAG test: the application must distinguish between information that exists in the document and information that does not.

### 2. PDF table extraction

Financial and operational tables can lose their visual row/column relationships when converted to plain text. Retrieval quality should therefore be tested against table-heavy questions.

### 3. Retrieval quality matters

A poor answer can originate from retrieving the wrong chunks rather than from the LLM itself. When debugging, inspect the retrieved context before changing the generation prompt.

### 4. Important figures should be manually verified

At least three important figures should be checked against the original PDF before submission. Recommended examples:

- ₹81.6 crore procurement spend
- 88.4% on-time delivery
- ₹1.9 crore estimated lost output

### 5. Avoid unnecessary re-indexing

Repeatedly embedding the same PDF during development can increase API usage. Use the persistent ChromaDB store once the document has been indexed successfully.

### 6. Avoid hallucination

The most important lesson from the evaluation is that a RAG system should not manufacture an answer simply because the user asks a financial question.

---

# 🎥 Demo Video

**Demo link:** `[Insert Loom / Google Drive / YouTube link]`

___

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes:

```bash
git commit -m "Add AmazingFeature"
```

4. Push the branch:

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request.

Keep contributions focused on improving document retrieval, grounded answering, usability, and source traceability.

---

# 📜 License

No explicit license has been provided for this project.

If this repository will be distributed publicly, add an appropriate `LICENSE` file and update this section.

---

# 🔗 Repository

**GitHub:** https://github.com/askikumari8-web/RAG-Project

---

## 🌟 Final Summary

The **AI Financial Analyst** demonstrates a complete RAG pipeline for company-document analysis:

```text
PDF
 ↓
Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Retrieval
 ↓
GPT-4o
 ↓
Grounded Answer
 ↓
Source Reference
```

The project emphasizes **accuracy, traceability, and honest refusal**. When the source document contains the answer, the system should retrieve and cite the relevant evidence. When the source does not contain the answer, the system should clearly state that the information is unavailable rather than hallucinating a financial value.

---

<p align="center">
  Built with Python · LangChain · ChromaDB · Streamlit · OpenAI GPT-4o
</p>
