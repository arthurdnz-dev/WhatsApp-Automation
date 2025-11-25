# src/core/sender.py
import time
import urllib.parse
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# IMPORT CORRIGIDO: utils está em src/core/utils/utils.py na sua estrutura atual
from src.core.utils.utils import human_delay, DRY_RUN, PROFILE_PATH, log_sent

def init_driver(profile_path: str = None, headless: bool = False):
    """
    Inicializa o ChromeDriver e retorna o objeto driver.
    profile_path: caminho para o perfil do Chrome (mantém sessão logada).
    """
    options = Options()
    if profile_path:
        options.add_argument(f"--user-data-dir={profile_path}")
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def open_chat(driver, numero: str, mensagem: str):
    """
    Abre a conversa para o número com a mensagem pré-preenchida.
    """
    msg_encoded = urllib.parse.quote(mensagem)
    url = f"https://web.whatsapp.com/send?phone={numero}&text={msg_encoded}"
    driver.get(url)
    time.sleep(6)  # ajuste se sua conexão for lenta

def send_text(driver, nome: str, numero: str, mensagem: str):
    """
    Envia a mensagem de texto usando a caixa editável do WhatsApp Web.
    Retorna (True, "") se ok, ou (False, detalhe) se erro.
    """
    try:
        # tenta primeiro um seletor genérico para a caixa de mensagem
        box = driver.find_element(By.XPATH, '//div[@contenteditable="true" and not(@data-testid)]')
    except Exception:
        try:
            box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab]')
        except Exception as e:
            log_sent(nome, numero, "ERROR_LOCATE_BOX", str(e))
            return False, f"Caixa de texto não encontrada: {e}"

    try:
        box.click()
        # alguns contenteditable não aceitam clear(), então apenas enviamos keys
        box.send_keys(mensagem)
        time.sleep(0.4)
        box.send_keys(Keys.ENTER)
        log_sent(nome, numero, "SENT")
        return True, ""
    except Exception as e:
        log_sent(nome, numero, "ERROR_SEND", str(e))
        return False, str(e)

def send_media(driver, nome: str, numero: str, media_path: str):
    """
    Anexa e envia arquivo (imagem/pdf). Retorna (ok, detail).
    """
    try:
        p = Path(media_path).expanduser().resolve()
        if not p.exists():
            log_sent(nome, numero, "ERROR_MEDIA_NOT_FOUND", str(p))
            return False, f"Arquivo não encontrado: {p}"

        attach_btn = driver.find_element(By.XPATH, '//div[@title="Anexar" or @data-testid="clip"]')
        attach_btn.click()
        time.sleep(0.8)

        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys(str(p))
        time.sleep(1.5)

        send_btn = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
        send_btn.click()
        log_sent(nome, numero, "SENT_MEDIA", str(p))
        return True, ""
    except Exception as e:
        log_sent(nome, numero, "ERROR_MEDIA", str(e))
        return False, str(e)
