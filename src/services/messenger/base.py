# src/services/messenger/base.py
from abc import ABC, abstractmethod

class MessengerBase(ABC):
    """
    Interface/abstração para serviços de envio.
    Implementações (Selenium, API, etc) devem seguir esta interface.
    """

    @abstractmethod
    def init(self):
        """Inicializa recursos (navegador, conexões)."""
        raise NotImplementedError

    @abstractmethod
    def open_chat(self, numero: str, mensagem: str):
        """Abre chat / prepara conversa (opcional)."""
        raise NotImplementedError

    @abstractmethod
    def send_text(self, numero: str, mensagem: str) -> tuple:
        """
        Envia texto. Retorna (ok: bool, detail: str).
        """
        raise NotImplementedError

    @abstractmethod
    def send_media(self, numero: str, caminho_arquivo: str) -> tuple:
        """Envia arquivo (imagem/pdf). Retorna (ok, detalhe)."""
        raise NotImplementedError

    @abstractmethod
    def quit(self):
        """Finaliza recursos (fecha navegador)."""
        raise NotImplementedError
