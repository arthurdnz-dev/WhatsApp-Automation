# src/services/messenger/whatsapp.py
import time
import urllib.parse
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from src.services.messenger.base import MessengerBase
from src.core.utils.utils import human_delay, DRY_RUN, PROFILE_PATH, log_sent

class WhatsAppSelenium(MessengerBase):
    """
    Implementação de MessengerBase usando Selenium + Chrome.
    - Mantém um único browser aberto para toda a execução (não abre uma aba por contato).
    - Usa PROFILE_PATH para manter sessão do WhatsApp.
    """

    def __init__(self, profile_path: str = None, headless: bool = False):
        self.driver = None
        self.profile_path = profile_path or PROFILE_PATH
        self.headless = headless

    def init(self):
        """Inicializa o driver Chrome (ou reutiliza se já inicializado)."""
        if self.driver:
            return self.driver

        options = Options()
        if self.profile_path:
            options.add_argument(f"--user-data-dir={self.profile_path}")
        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        # abre whatsapp web e espera o usuário escanear (se necessário)
        self.driver.get("https://web.whatsapp.com")
        return self.driver

    def open_chat(self, numero: str, mensagem: str):
        """
        Abre o chat do número (na mesma aba) com o texto pré-preenchido.
        """
        if not self.driver:
            raise RuntimeError("Driver não inicializado. Chame init() antes.")

        msg_encoded = urllib.parse.quote(mensagem)
        url = f"https://web.whatsapp.com/send?phone={numero}&text={msg_encoded}"
        self.driver.get(url)
        time.sleep(5)  # espera carregar a conversa

    def send_text(self, numero: str, mensagem: str) -> tuple:
        """Abre chat (se necessário) e envia texto."""
        try:
            if not self.driver:
                self.init()

            # abre o chat com a mensagem pré-preenchida (ajusta para garantir foco)
            self.open_chat(numero, mensagem)

            # tenta localizar caixa editável (vários seletores para fallback)
            try:
                box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true" and not(@data-testid)]')
            except Exception:
                box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab]')

            # envia ENTER para confirmar envio
            box.click()
            time.sleep(0.2)
            box.send_keys(Keys.ENTER)
            log_sent(numero, numero, "SENT")
            return True, ""
        except Exception as e:
            log_sent(numero, numero, "ERROR_SEND_TEXT", str(e))
            return False, str(e)

    def send_media(self, numero: str, caminho_arquivo: str) -> tuple:
        """Envia arquivo (imagem/pdf) usando o input[type=file] do WhatsApp Web."""
        try:
            if not self.driver:
                self.init()

            # abre chat sem texto para anexar mais facilmente
            self.open_chat(numero, "")

            p = Path(caminho_arquivo).expanduser().resolve()
            if not p.exists():
                log_sent(numero, numero, "ERROR_MEDIA_NOT_FOUND", str(p))
                return False, f"Arquivo não encontrado: {p}"

            # clicar botão anexar (clip)
            attach_btn = self.driver.find_element(By.XPATH, '//div[@title="Anexar" or @data-testid="clip"]')
            attach_btn.click()
            time.sleep(0.8)

            # input[type=file] para enviar arquivo
            file_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
            file_input.send_keys(str(p))
            time.sleep(1.5)

            # botão enviar (icone envio)
            send_btn = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_btn.click()

            log_sent(numero, numero, "SENT_MEDIA", str(p))
            return True, ""
        except Exception as e:
            log_sent(numero, numero, "ERROR_SEND_MEDIA", str(e))
            return False, str(e)

    def quit(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception:
            pass
