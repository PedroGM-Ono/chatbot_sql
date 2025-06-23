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
├── text2sql_script.py     # Run chatbot to ask questions
├── database/
│   └── vendas_retail.db   # Generated SQLite database
│   └── populate_db.py     # Populate the SQLite DB from Excel
│   └── raw_data.xlsx          # Input Excel file with raw sales data
├── requirements.txt       # Python requirements for the project
├── models/                # LLM model file
│   └──# Put the models files here
└── README.md

```


## Instructions
1. Create and activate a Python env
```bash
    python3 -m venv .venv
    source .venv/bin/activate
```
2. Install the dependencies
```bash
  pip install -r requirements.txt
```
3. Download the LLM you would like to use on the 'models/' folder
```bash
wget  "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
```
4. Run the populate database script to generate the db file:
```bash
python database/populate
```




