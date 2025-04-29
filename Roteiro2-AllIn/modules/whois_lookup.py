import whois
from colorama import Fore
from utils.utils import print_styled, save_report

def whois_lookup(domain):
    """Realiza consulta WHOIS de um domínio"""
    try:
        info = whois.whois(domain)
        report = f"[+] WHOIS Lookup para: {domain}\n\n"
        for key, value in info.items():
            report += f"{key}: {value}\n"
        print_styled(report, Fore.GREEN)

        save_option = input("Deseja salvar o relatório? [S/N]: ")
        if save_option.upper() == "S":
            save_report(report, f"whois_{domain}.txt")

    except Exception as e:
        print_styled(f"Erro ao realizar WHOIS lookup: {e}", Fore.RED)
