import pandas as pd
import sqlite3
from sqlalchemy import (
    create_engine,
    inspect,
)
from llama_cpp import Llama
from translate import Translator

db_path = "database/vendas_retail.db"


def write_prompt_description():
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    description = "[INST]"
    description += "\nYou are an expert in writing SQL queries for SQLite databases."
    description += "\nBelow is the schema of the database:"

    inspector = inspect(engine)
    for table in inspector.get_table_names():
        columns_info = [(col["name"], col["type"]) for col in inspector.get_columns(table)]

        table_description = f"Table {table}:\n"

        table_description += "\n".join([f"{name}: {col_type}" for name, col_type in columns_info])
        description += "\n\n" + table_description

    description+="\n\nYour task:"
    description+="\nWrite a single valid SQLite query that answers the following question:\n\n$$\n"
    description+="\nInstructions:"
    description+="\n- Use JOINs where needed, explicitly referencing table and column names."
    description+="\n- Always use the correct table for each field based on the schema above."
    description+="\n- Prefer names (e.g. product name, client name) instead of IDs in the output when applicable."
    description+="\n- Use full SQL syntax."
    description+="\n- Return only the SQLite query enclosed in triple backticks (```)."
    description+="\n- DO NOT return anything else — no comments, no explanations."
    description+="\n- The field sales.date is stored as TEXT in format d/m/Y H:M"
    description+="\n[/INST]"

    return description


def ask_llm(question, debug=False):
    # model_path = "models/mistral-7b-instruct-v0.2.Q4_K_S.gguf"
    model_path = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    # model_path = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    # model_path = "models/mistral-7b-instruct-v0.1.Q5_K_M.gguf"
    # model_path = "models/mistral-7b-instruct-v0.2.Q5_K_M.gguf"
    # model_path = "models/mistral-7b-instruct-v0.2.Q6_K.gguf"
    # model_path = "models/deepseek-coder-6.7b-instruct.Q5_K_M.gguf"
    # model_path = "models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf"
    # model_path = "models/devstralQ4_0.gguf"

    llm = Llama(
        model_path=model_path,
        n_ctx=32768,
        verbose=False,
        use_mlock=True,
        embedding=False,
    )
    if debug:
        print("-------------LLM INFO-----------------")
        print(type(llm))
        print(llm)
        print("----------------------------------------")


    translator= Translator(to_lang="en", from_lang="pt")
    translation = translator.translate(question)

    if debug:
        print("-------------Translator-----------------")
        print(question)
        print(translation)
        print("----------------------------------------")

    prompt = write_prompt_description().replace("$$", translation)

    if debug:
        print("------------Prompt-----------")
        print(prompt)
        print("----------------------------")

    output = llm(prompt, max_tokens=256, stop=["</s>"])

    if debug:
        print("----------------LLM Output--------------")
        print(output)
        print("----------------------------------------")
    return output["choices"][0]["text"]


def is_query_safe(sql):
    proibidos = ["DROP", "DELETE", "UPDATE", "INSERT"]
    return not any(palavra in sql.upper() for palavra in proibidos)


def execute_query(sql, debug=False):
    text = sql
    substring = "```"
    occurrences = []
    start_index = 0
    while True:
        index = text.find(substring, start_index)
        if index == -1:
            break
        occurrences.append(index)
        start_index = index + 1
    if len(occurrences) < 2:
        return None
    
    if text.find('sql') != -1:
        occurrences[0] += 4
    
    sql=sql[occurrences[0]+3:occurrences[1]]
        
    if debug:
        print("-------Query executada-------")
        print(sql)
        print("--------------------------")

    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        print("Erro ao executar SQL:", e)
        return None


def main():
    debug=False
    print("Pergunte algo sobre as vendas (ou 'sair' para encerrar):")

    while True:
        pergunta = input("\nSua pergunta: ").strip()
        if pergunta.lower() in ["sair", "exit", "quit"]:
            break

        sql = ask_llm(pergunta, debug)

        if not sql:
            print("Não foi possível gerar uma consulta SQL.")
            continue
        
        
        print("-------Query gerada-------")
        print(sql)
        print("--------------------------")

        if not is_query_safe(sql):
            print("Query bloqueada por segurança.")
            continue

        resultado = execute_query(sql, debug)
        if resultado is not None:
            print("\nResultado:")
            print(resultado)
        else:
            print("Falha ao executar a query.")

if __name__ == "__main__":
    main()
