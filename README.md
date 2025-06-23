# chatbot_sql

**chatbot_sql** is a terminal-based Python application that translates natural language questions in **Portuguese** into executable **SQLite** queries using a local **LLM (Mistral-7B)** running on CPU. It also includes a utility to populate the database from an Excel (.xlsx) file.

---

## Features

- Converts questions in **Portuguese** to SQL queries using an LLM.
- Extracts database schema automatically and includes it in the prompt.
- Built-in SQL safety checks to block dangerous commands (`DROP`, `DELETE`, etc.).
- Populates an SQLite database from a raw Excel file with realistic fake client data.
- Uses `llama-cpp-python` to run Mistral-7B locally (no GPU required).

---

## Project Structure

```bash
.
├── populate_db.py         # Populate the SQLite DB from Excel
├── text2sql_script.py     # Run chatbot to ask questions
├── database/
│   └── vendas_retail.db   # Generated SQLite database
├── raw_data.xlsx          # Input Excel file with raw sales data
├── models/
│   └── mistral-7b-instruct-v0.1.Q4_K_M.gguf  # LLM model file
└── README.md
