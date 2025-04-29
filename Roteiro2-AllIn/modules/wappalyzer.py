import requests
from colorama import Fore
from utils.utils import print_styled, save_report

def wappalyzer_like_scan(url):
    """Faz uma análise simples de tecnologias de um site"""
    tech_detected = []
    report = f"[+] Tecnologia detectada para: https://{url}\n\n"

    try:
        response = requests.get(f"https://{url}", timeout=10)
        headers = response.headers
        html = response.text.lower()

        # Verificação básica nos headers
        server = headers.get('Server')
        powered = headers.get('X-Powered-By')
        if server:
            tech_detected.append(f"Servidor: {server}")
        if powered:
            tech_detected.append(f"Powered by: {powered}")

        if "wp-content" in html or "wordpress" in html:
            tech_detected.append("WordPress")
        if "shopify" in html:
            tech_detected.append("Shopify")
        if "drupal" in html:
            tech_detected.append("Drupal")
        if "joomla" in html:
            tech_detected.append("Joomla")
        if "jquery" in html:
            tech_detected.append("jQuery")
        if "react" in html:
            tech_detected.append("ReactJS")
        if "vue" in html:
            tech_detected.append("VueJS")
        if "angular" in html:
            tech_detected.append("AngularJS")
        if "bootstrap" in html:
            tech_detected.append("Bootstrap CSS")
        if "font-awesome" in html:
            tech_detected.append("Font Awesome")

        if tech_detected:
            for tech in tech_detected:
                report += f"- {tech}\n"
                print_styled(f"[+] {tech}", Fore.GREEN)
        else:
            report += "Nenhuma tecnologia detectada com os padrões básicos.\n"
            print_styled("Nenhuma tecnologia detectada com os padrões básicos.", Fore.YELLOW)

    except requests.exceptions.RequestException as e:
        print_styled(f"Erro ao acessar {url}: {e}", Fore.RED)
        return

    save_option = input("Deseja salvar o relatório? [S/N]: ")
    if save_option.upper() == "S":
        save_report(report, f"wappalyzer_scan_{url.replace('https://','').replace('http://','').replace('.', '_')}.txt")
