# src/core/utils/utils.py
import os
import random
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes")
PROFILE_PATH = os.getenv("PROFILE_PATH", "")
MIN_DELAY = float(os.getenv("MIN_DELAY", 2))
MAX_DELAY = float(os.getenv("MAX_DELAY", 5))

def human_delay():
    """Delay aleatório entre MIN_DELAY e MAX_DELAY (simula usuário humano)."""
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    time.sleep(delay)
    return delay

def log_sent(nome, telefone, status, detail=""):
    """Log simples para acompanhar envios (pode ser substituído por loguru)."""
    ts = __import__("datetime").datetime.now().isoformat()
    print(f"[{ts}] {nome} | {telefone} | {status} | {detail}")
