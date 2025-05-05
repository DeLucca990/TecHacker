import re
import requests
from colorama import Fore
from utils.utils import print_styled, save_report

def wappalyzer_like_scan(url):
    """Análise de tecnologias via regex no HTML, headers, scripts, links e metas dados"""
    tech_detected = []
    report = f"[+] Tecnologia detectada para: https://{url}\n\n"

    html_patterns = {
        "WordPress": r'wp-content|wordpress|<meta name="generator" content="WordPress',
        "Drupal": r'drupal|<meta name="generator" content="Drupal',
        "Joomla": r'joomla|<meta name="generator" content="Joomla',
        "Shopify": r'shopify|cdn\.shopify\.com',
        "ReactJS": r'react(?:[\.\-]dom)?|data-reactroot|__REACT_DEVTOOLS_GLOBAL_HOOK__',
        "AngularJS": r'angular(?:\.min)?\.js|ng-app|ng-controller',
        "VueJS": r'vue(?:\.min)?\.js|v-bind|v-model',
        "jQuery": r'jquery(?:\.min)?\.js',
        "Bootstrap CSS": r'bootstrap(?:\.min)?\.css',
        "Font Awesome": r'font-awesome|fontawesome(?:\.min)?\.css',
        "Google Analytics": r'www\.google-analytics\.com|gtag\(\'config\'',
        "Hotjar": r'hotjar\.com|static\.hotjar\.com',
        "Cloudflare": r'cloudflare',
        "Wix": r'wix\.com|wix-code',
        "Squarespace": r'squarespace\.com',
    }

    script_patterns = {
        "Hotjar": r'hotjar\.com|static\.hotjar\.com',
        "Google Analytics": r'www\.google-analytics\.com/analytics\.js|gtag/js',
        "jQuery": r'jquery(?:\.min)?\.js',
        "Bootstrap JS": r'bootstrap(?:\.min)?\.js',
        "VueJS": r'vue(?:\.min)?\.js',
        "AngularJS": r'angular(?:\.min)?\.js',
        "ReactJS": r'react(?:[\.\-]dom)?(?:\.min)?\.js',
    }

    link_patterns = {
        "Bootstrap CSS": r'bootstrap(?:\.min)?\.css',
        "Font Awesome": r'font-awesome|fontawesome(?:\.min)?\.css',
    }

    meta_patterns = {
        "WordPress": r'<meta name="generator" content="WordPress',
        "Drupal": r'<meta name="generator" content="Drupal',
        "Joomla": r'<meta name="generator" content="Joomla',
    }

    try:
        response = requests.get(f"https://{url}", timeout=10)
        headers = response.headers
        html = response.text.lower()

        # Headers
        server = headers.get('Server')
        powered = headers.get('X-Powered-By')
        if server:
            tech_detected.append(f"Servidor: {server}")
        if powered:
            tech_detected.append(f"Powered by: {powered}")

        # Scripts
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
        for script in scripts:
            for tech, pattern in script_patterns.items():
                if re.search(pattern, script):
                    if tech not in tech_detected:
                        tech_detected.append(tech)

        # Links CSS
        links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', html)
        for link in links:
            for tech, pattern in link_patterns.items():
                if re.search(pattern, link):
                    if tech not in tech_detected:
                        tech_detected.append(tech)

        # Metas
        metas = re.findall(r'<meta[^>]+content=["\']([^"\']+)["\']', html)
        for meta_content in metas:
            for tech, pattern in meta_patterns.items():
                if re.search(pattern, meta_content):
                    if tech not in tech_detected:
                        tech_detected.append(tech)

        # HTML geral
        for tech, pattern in html_patterns.items():
            if re.search(pattern, html):
                if tech not in tech_detected:
                    tech_detected.append(tech)

        if tech_detected:
            for tech in tech_detected:
                report += f"- {tech}\n"
                print_styled(f"[+] {tech}", Fore.GREEN)
        else:
            report += "Nenhuma tecnologia detectada com os padrões definidos.\n"
            print_styled("Nenhuma tecnologia detectada com os padrões definidos.", Fore.YELLOW)

    except requests.exceptions.RequestException as e:
        print_styled(f"Erro ao acessar {url}: {e}", Fore.RED)
        return

    save_option = input("Deseja salvar o relatório? [S/N]: ")
    if save_option.upper() == "S":
        save_report(report, f"wappalyzer_scan_{url.replace('https://','').replace('http://','').replace('.', '_')}.txt")