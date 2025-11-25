import pandas as pd
import os

def read_contacts(csv_path="data/contatos.csv"):
    """
    Lê o arquivo contatos.csv e retorna um DataFrame pandas.
    Força todas as colunas como string para evitar erros.
    """
    try:
        if not os.path.exists(csv_path):
            print(f"[ERRO] Arquivo não encontrado: {csv_path}")
            return pd.DataFrame()

        df = pd.read_csv(csv_path, dtype=str).fillna("")

        # Normalização opcional
        if "numero" in df.columns:
            df["numero"] = df["numero"].astype(str).str.replace(" ", "").str.replace("-", "")

        return df

    except Exception as e:
        print(f"[ERRO] Falha ao ler contatos: {e}")
        return pd.DataFrame()
