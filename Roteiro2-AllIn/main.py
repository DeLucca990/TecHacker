import pyfiglet
from colorama import init, Fore
from utils.utils import print_styled
from modules.subdomain import subdomain_scan
from modules.dns_enum import dns_enum_scan
from modules.wappalyzer import wappalyzer_like_scan
from modules.portscan import main as portscan_main
from modules.whois_lookup import whois_lookup

init()

def main_menu():
    print_styled(pyfiglet.figlet_format("PDL CLI Module Scanner", font="slant"), Fore.LIGHTGREEN_EX)
    print_styled("[1] Port Scan", Fore.CYAN)
    print_styled("[2] WHOIS Lookup", Fore.CYAN)
    print_styled("[3] Subdomain Scanner", Fore.CYAN)
    print_styled("[4] DNS Enumeration", Fore.CYAN)
    print_styled("[5] Wappalyzer-like Scan", Fore.CYAN)
    print_styled("[0] Sair", Fore.CYAN)

    choice = input("\nEscolha a opção: ")
    return choice

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            portscan_main()
        elif choice == "2":
            domain = input("Digite o domínio para consulta WHOIS (ex: google.com): ")
            whois_lookup(domain)
        elif choice == "3":
            domain = input("Digite o domínio para varredura de subdomínios (ex: example.com): ")
            subdomain_scan(domain)
        elif choice == "4":
            domain = input("Digite o domínio para enumeração DNS (ex: example.com): ")
            dns_enum_scan(domain)
        elif choice == "5":
            url = input("Digite a URL para análise (ex: example.com): ")
            wappalyzer_like_scan(url)
        elif choice == "0":
            print_styled("Saindo...", Fore.YELLOW)
            break
        else:
            print_styled("Opção inválida.", Fore.RED)

if __name__ == "__main__":
    main()
