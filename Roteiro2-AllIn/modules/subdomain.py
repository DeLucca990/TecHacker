import socket
from colorama import Fore
from utils.utils import print_styled, save_report, load_wordlist

def subdomain_scan(domain, wordlist=None):
    """Faz um scanner de subdomínios usando uma wordlist"""

    wl_choice = input("Deseja usar a wordlist completa? (Esse processo pode demorar alguns miutos) [S/N]: ")
    if wl_choice.upper() == "S":
        wordlist = load_wordlist("./worldlist/subdomains_large.txt")
    elif wl_choice.upper() == "N":
        wordlist = load_wordlist("./worldlist/subdomains_small.txt")
    else:
        print_styled("Opção inválida. Usando wordlist pequena por padrão.", Fore.YELLOW)
        wordlist = load_wordlist("./worldlist/subdomains_small.txt")

    found_subdomains = []
    report = f"[+] Subdomain scan para {domain}\n\n"

    for sub in wordlist:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            found_subdomains.append((subdomain, ip))
            line = f"[+] Encontrado: {subdomain} -> {ip}\n"
            report += line
            print_styled(line.strip(), Fore.GREEN)
        except socket.gaierror:
            pass
        except Exception as e:
            print_styled(f"[!] Erro ao resolver {subdomain}: {e}", Fore.RED)

    if not found_subdomains:
        print_styled("Nenhum subdomínio encontrado.", Fore.YELLOW)

    report += "\n[+] Varredura finalizada.\n"
    
    save_option = input("Deseja salvar o relatório? [S/N]: ")
    if save_option.upper() == "S":
        save_report(report, f"subdomain_scan_{domain.replace('.', '_')}.txt")
