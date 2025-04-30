from colorama import Fore, Style

def print_styled(text, color=Fore.WHITE, style=Style.BRIGHT):
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def load_wordlist(file_path):
    """Carrega uma wordlist de subdomínios a partir de um arquivo"""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print_styled(f"[!] Arquivo {file_path} não encontrado.", Fore.RED)
        return []
    except Exception as e:
        print_styled(f"[!] Erro ao carregar a wordlist: {e}", Fore.RED)
        return []

def save_report(report_data, filename):
    with open(f"./reports/{filename}", "w", encoding="utf-8", errors="ignore") as file:
        file.write(report_data)
    print_styled(f"[+] Relatório salvo em {filename}", Fore.GREEN)
