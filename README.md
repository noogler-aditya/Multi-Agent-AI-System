# 🧠 Multi-Agent AI System for Input Classification & Routing

This project is a **multi-agent AI pipeline** designed to classify inputs (PDF, JSON, Email), detect their intent (e.g., Invoice, Complaint), and route them to specialized agents. The system maintains a **shared memory** for traceability and enables seamless processing across agents.
---

## 🚀 Features

- Accepts input in **PDF**, **JSON**, and **Email (text)** formats.
- Detects **input type** and **user intent** (Invoice, RFQ, Complaint, Regulation, etc.).
- Routes input to a specific **agent** for processing.
- Maintains a **shared memory** with extracted data and thread tracking.
- Modular design with extensibility for new formats/intents.

---

## 🧱 System Architecture

```mermaid
flowchart TD
    A[User Input: PDF, JSON, Email] --> B[Classifier Agent]
    B --> C1[Detect Format]
    B --> C2[Detect Intent]
    B --> C3[Log to Shared Memory]
    C1 --> D1{Format Type}
    C2 --> D2{Intent Type}

    D1 -->|PDF| PDF_Agent[PDF Agent (Optional)]
    D1 -->|JSON| JSON_Agent[JSON Agent]
    D1 -->|Email| Email_Agent[Email Agent]

    D2 -->|Invoice| Process_Invoice[Process Invoice]
    D2 -->|RFQ| Process_RFQ[Process RFQ]
    D2 -->|Complaint| Process_Complaint[Process Complaint]

    JSON_Agent --> M[Shared Memory Module]
    Email_Agent --> M
    PDF_Agent --> M
    Process_Invoice --> M
    Process_RFQ --> M
    Process_Complaint --> M

```

---

## 🧠 Agents Overview

### 1. 🔍 Classifier Agent
- **Input**: Raw file, JSON, or email content.
- **Output**:
  - Detects `Format` (PDF / JSON / Email)
  - Detects `Intent` (Invoice, Complaint, RFQ, etc.)
  - Routes to appropriate downstream agent
- **Logs**: Format and Intent to Shared Memory

### 2. 🗞 JSON Agent
- **Input**: JSON-formatted payloads
- **Function**:
  - Parses structured data
  - Converts to target schema
  - Flags anomalies or missing fields
- **Logs**: Validated/processed data to Shared Memory

### 3. ✉️ Email Agent
- **Input**: Plain-text email content
- **Function**:
  - Extracts sender name, urgency, and intent
  - Formats output for CRM-style systems
- **Logs**: Extracted metadata to Shared Memory

---

## 🧠 Shared Memory Module

A lightweight context store available across agents.

- **Can be backed by**: SQLite (preferred), Redis, or in-memory store
- **Stores**:
  - `source`, `file type`, `timestamp`
  - Extracted fields
  - Conversation or thread ID

---

## 🧪 Sample Flow

```text
User sends email:
-----------------------
From: ceo@company.com
Subject: Request for Quotation
Body: Please send us a quote for 500 units of ...



Classifier Agent:
→ Detected Format: Email
→ Detected Intent: RFQ
→ Routed to: Email Agent



Email Agent:
→ Extracted: sender=ceo@company.com, intent=RFQ, urgency=Medium
→ Formatted output for CRM



Shared Memory:
→ Logged: source=Email, type=RFQ, sender=ceo@company.com, timestamp=2025-05-30
```

---

## 📁 Folder Structure

```
multi-agent-system/
├── agents/
│   ├── classifier_agent.py
│   ├── json_agent.py
│   └── email_agent.py
├── memory/
│   └── shared_memory.py (SQLite-backed)
├── utils/
│   └── format_detector.py
├── tests/
│   └── sample_inputs/
│       ├── invoice.json
│       ├── sample_email.txt
│       └── sample_invoice.pdf
├── main.py
├── requirements.txt
└── README.md
```

---

## 📸 Sample Logs (SQLite Memory)

| ID | Source | Type  | Intent | Timestamp           | Extracted Fields                  |
|----|--------|-------|--------|---------------------|-----------------------------------|
| 1  | Email  | RFQ   | Medium | 2025-05-30 12:21:54 | sender=ceo@company.com, item=500u |
| 2  | JSON   | Invoice | High | 2025-05-30 12:22:10 | invoice_no=1234, total=$1200      |

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **LLMs**: Gemini AI
- **Memory Backend**: SQLite
- **Utilities**: `pdfminer`, `email`, `json`, `sqlite3`

---

## 🔧 Setup Instructions

```bash
# Clone repo
git clone https://github.com/yourname/multi-agent-system.git
cd multi-agent-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the system
python main.py sample_inputs/complaint_email.txt
```

---

## 📌 Future Improvements

- PDF Agent support with OCR and field extraction
- Web dashboard for memory visualization
- Redis-based scalable memory module
- Add multilingual support

---
