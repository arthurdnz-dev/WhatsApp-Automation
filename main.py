# main.py
import os
from time import sleep
from dotenv import load_dotenv

# módulos do projeto
from src.core.utils.menu import show_menu, menu_settings
from src.core.utils.helpers import clear_screen
from src.core.utils.banner import show_banner
from src.core.messages.templates import load_templates
from src.core.loader import read_contacts
from src.core.utils.utils import human_delay, DRY_RUN, log_sent

# nova service (Selenium)
from src.services.messenger.whatsapp import WhatsAppSelenium

load_dotenv()

def prepare_message(template, nome):
    """Substitui placeholder {nome}"""
    return template.replace("{nome}", nome)

def run_campaign_with_service(service, template_key=None, contacts_path="data/contatos.csv"):
    templates = load_templates()
    df = read_contacts(contacts_path)
    if len(df) == 0:
        print("Nenhum contato encontrado.")
        return

    print(f"{len(df)} contatos carregados. DRY_RUN={DRY_RUN}")

    if not DRY_RUN:
        service.init()
        print("Aguardando WhatsApp Web carregar (escaneie QR se necessário)...")

    try:
        for idx, row in df.iterrows():
            nome = str(row.get("nome", "")).strip()
            numero = str(row.get("telefone", "")).strip().replace(" ", "")
            contact_message = str(row.get("message", "")).strip()
            image = str(row.get("image", "")).strip()
            pdf = str(row.get("pdf", "")).strip()

            if contact_message:
                mensagem = contact_message
            elif template_key:
                mensagem = templates.get(template_key, "Olá {nome}, tudo bem?")
            else:
                mensagem = "Olá {nome}, tudo bem?"

            mensagem = prepare_message(mensagem, nome)

            print(f"[{idx+1}/{len(df)}] -> {nome} | {numero} | media={bool(image or pdf)}")

            if DRY_RUN:
                log_sent(nome, numero, "DRY_RUN", mensagem)
                print("  (dry run) - not sending.")
            else:
                if image:
                    ok, detail = service.send_media(numero, image)
                    if not ok:
                        print("  erro media:", detail)

                if pdf:
                    ok, detail = service.send_media(numero, pdf)
                    if not ok:
                        print("  erro pdf:", detail)

                ok, detail = service.send_text(numero, mensagem)
                if not ok:
                    print("  erro text:", detail)

            delay = human_delay()
            print(f"  waiting {delay:.1f}s")

    finally:
        if not DRY_RUN:
            service.quit()
        print("Processo finalizado.")

def show_templates_preview():
    templates = load_templates()
    clear_screen()
    print("TEMPLATES DISPONÍVEIS:\n")
    for name, msg in templates.items():
        print(f"- {name}: {msg}")
    input("\nPressione ENTER para voltar.")

def open_settings():
    c = menu_settings()
    if c == "1":
        print("Configurações de velocidade e limites ainda em desenvolvimento.")
    input("\nEnter para voltar.")

def show_about():
    clear_screen()
    print("""
WhatsApp Automation PRO
Versão 1.0
Desenvolvido por Arthur Diniz
""")
    input("\nEnter para voltar.")

def start_app():
    service = WhatsAppSelenium(
        profile_path=os.getenv("PROFILE_PATH", ""),
        headless=False
    )

    while True:
        choice = show_menu()

        if choice == "1":
            clear_screen()
            templates = load_templates()
            print("Templates disponíveis:")
            for k in templates.keys():
                print(" -", k)
            template_key = input("Digite o nome do template (ou Enter para usar mensagem por contato): ").strip() or None

            print("Iniciando campanha...")
            run_campaign_with_service(service, template_key=template_key, contacts_path="data/contatos.csv")

            input("\nEnter para voltar ao menu.")

        elif choice == "2":
            show_templates_preview()

        elif choice == "3":
            open_settings()

        elif choice == "4":
            show_about()

        elif choice == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")
            sleep(1)

if __name__ == "__main__":
    start_app()
