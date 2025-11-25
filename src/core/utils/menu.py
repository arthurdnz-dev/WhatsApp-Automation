# src/core/utils/menu.py
from src.core.utils.banner import show_banner
from src.core.utils.helpers import clear_screen

def show_menu():
    clear_screen()
    show_banner()

    print("""
╔══════════════════════════════════════╗
║        WHATSAPP AUTOMATION PRO       ║
╠══════════════════════════════════════╣
║ 1) Enviar mensagens                  ║
║ 2) Visualizar templates              ║
║ 3) Configurações                     ║
║ 4) Sobre o projeto                   ║
║ 0) Sair                              ║
╚══════════════════════════════════════╝
""")

    choice = input("Escolha uma opção: ")
    return choice


def menu_settings():
    clear_screen()
    print("""
CONFIGURAÇÕES

1) Velocidade de envio
2) Ativar/Desativar DRY-RUN (edite .env)
0) Voltar
""")
    return input("Escolha: ")
