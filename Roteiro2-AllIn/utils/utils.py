from colorama import Fore, Style

def print_styled(text, color=Fore.WHITE, style=Style.BRIGHT):
    print(f"{style}{color}{text}{Style.RESET_ALL}")

def save_report(report_data, filename):
    with open(f"./reports/{filename}", "w", encoding="utf-8", errors="ignore") as file:
        file.write(report_data)
    print_styled(f"[+] Relatório salvo em {filename}", Fore.GREEN)