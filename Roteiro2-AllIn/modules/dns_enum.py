import dns.resolver
from colorama import Fore
from utils.utils import print_styled, save_report

def dns_enum_scan(domain):
    """Realiza a enumeração básica de registros DNS"""
    record_types = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT']
    report = f"[+] Resultados de DNS Enumeration para: {domain}\n\n"

    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            report += f"\n{record} Records:\n"
            for rdata in answers:
                report += f"  - {rdata.to_text()}\n"
            print_styled(f"[+] {record} records encontrados.", Fore.GREEN)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            print_styled(f"[-] Nenhuma entrada {record} encontrada.", Fore.YELLOW)
        except Exception as e:
            print_styled(f"[!] Erro consultando {record}: {e}", Fore.RED)

    print_styled("\n" + report, Fore.CYAN)

    save_option = input("Deseja salvar o relatório? [S/N]: ")
    if save_option.upper() == "S":
        save_report(report, f"dns_enum_{domain.replace('.', '_')}.txt")
