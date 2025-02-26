import pyfiglet
import socket
import ipaddress
from colorama import Fore, init
from utils.utils import print_styled, save_report
from utils.dict_ports import WELL_KNOWN_PORTS, ALL_PORTS

init()

def get_os_info(banner):
    """Retorna informações sobre o sistema operacional"""
    banner_lower = banner.lower()
    if "windows" in banner_lower or "microsoft" in banner_lower:
        return "Possivelmente Windows"
    elif "linux" in banner_lower or "ubuntu" in banner_lower or "debian" in banner_lower:
        return "Possivelmente Linux"
    elif "freebsd" in banner_lower:
        return "Possivelmente FreeBSD"
    else:
        return "Não foi possível identificar o sistema operacional"

def tcp_scan_port(address, port, family=socket.AF_INET, timeout=1.0):
    """Faz o scan de uma porta TCP"""
    banner = ""
    with socket.socket(family, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((address, port))
            state = "aberta"
            try:
                banner = sock.recv(1024).decode(errors='ignore')
            except socket.timeout:
                pass
        except ConnectionRefusedError:
            state = "fechada"
        except socket.timeout:
            state = "filtrada"
        except OSError:
            state = "fechada"
    return state, banner

def udp_scan_port(address, port, family=socket.AF_INET, timeout=1.0):
    """Faz o scan de uma porta UDP"""
    banner = ""
    with socket.socket(family, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.sendto(b"teste", (address, port))
            data, _ = sock.recvfrom(1024)
            banner = data.decode(errors='ignore')
            state = "aberta"
        except socket.timeout:
            state = "filtrada"
        except ConnectionRefusedError:
            state = "fechada"
        except OSError:
            state = "fechada"
    return state, banner

def scan_host(host, start_port, end_port, PORTS, protocol="TCP", timeout=1.0):
    """
    Varre (host, range de portas) no protocolo especificado (TCP ou UDP).
    Identifica estado da porta e tenta banner grabbing (no caso TCP).
    """
    family = None
    try:
        ip_obj = ipaddress.ip_address(host)
        if ip_obj.version == 4:
            family = socket.AF_INET
        else:
            family = socket.AF_INET6
    except ValueError:
        infos = socket.getaddrinfo(host, None, socket.AF_UNSPEC, 0, socket.SOL_TCP)
        if len(infos) > 0:
            family = infos[0][0]
        else:
            print_styled(f"Não foi possível resolver {host}", Fore.RED)
            return

    report = f"[+] Iniciando varredura em: {host} (Protocolo: {protocol}) - Portas: {start_port}-{end_port}\n\n"
    print_styled(f"[+] Iniciando varredura em: {host} (Protocolo: {protocol}) - Portas: {start_port}-{end_port}\n", Fore.CYAN)
    ports_to_scan = sorted(
        p for p in PORTS.keys() if start_port <= p <= end_port
    )
    for port in ports_to_scan:
        if protocol.upper() == "UDP":
            state, banner = udp_scan_port(host, port, family=family, timeout=timeout)
        else:
            state, banner = tcp_scan_port(host, port, family=family, timeout=timeout)

        servico = PORTS.get(port, "Serviço desconhecido")
        if state == "aberta":
            if protocol.upper() == "TCP" and banner:
                os_info = get_os_info(banner)
                line = f"[*] Porta {port}/{protocol.upper()} ABERTA - Serviço: {servico} | SO: {os_info}\n"
                line += f"[?] BANNER: {banner.strip()}\n"
                print_styled(f"[*] Porta {port}/{protocol.upper()} ABERTA - Serviço: {servico} | SO: {os_info}", Fore.GREEN)
                print_styled(f"[?] BANNER: {banner.strip()}", Fore.BLUE)
            else:
                line = f"[*] Porta {port}/{protocol.upper()} ABERTA - Serviço: {servico}\n"
                print_styled(f"[*] Porta {port}/{protocol.upper()} ABERTA - Serviço: {servico}", Fore.GREEN)
        elif state == "filtrada":
            line = f"[-] Porta {port}/{protocol.upper()} FILTRADA - Serviço: {servico}\n"
            print_styled(f"[-] Porta {port}/{protocol.upper()} FILTRADA - Serviço: {servico}", Fore.YELLOW)
        elif state == "fechada":
            line = f"[X] Porta {port}/{protocol.upper()} FECHADA\n"
            print_styled(f"[X] Porta {port}/{protocol.upper()} FECHADA", Fore.RED)
        report += line

    report += "\n[+] Varredura finalizada.\n"
    print_styled("[+] Varredura finalizada.", Fore.MAGENTA)

    save_option = input("Deseja salvar o relatório? [S/N]: ")
    if save_option.upper() == "S":
        save_report(report, f"scan_{host}.txt")

def scan_network(network_cidr, start_port, end_port, PORTS, protocol="TCP", timeout=1.0):
    """
    Varre todas as hosts de uma rede (IPv4 ou IPv6) de acordo com o CIDR informado.
    """
    try:
        net_obj = ipaddress.ip_network(network_cidr, strict=False)
    except ValueError as e:
        print(f"CIDR inválido: {network_cidr} - Erro: {e}")
        return

    report = f"[+] Iniciando varredura na rede {network_cidr} (Protocolo: {protocol}) - Portas: {start_port}-{end_port}\n\n"
    print(f"\nIniciando varredura na rede {network_cidr} (Protocolo: {protocol}) - Portas: {start_port}-{end_port}")
    ports_to_scan = sorted(
        p for p in PORTS.keys() if start_port <= p <= end_port
    )
    for ip in net_obj.hosts():
        ip_str = str(ip)
        for port in ports_to_scan:
            if protocol.upper() == "UDP":
                estado, banner = udp_scan_port(ip_str, port, 
                                               family=socket.AF_INET6 if ip.version==6 else socket.AF_INET,
                                               timeout=timeout)
            else:
                estado, banner = tcp_scan_port(ip_str, port, 
                                               family=socket.AF_INET6 if ip.version==6 else socket.AF_INET,
                                               timeout=timeout)

            servico = PORTS.get(port, "Serviço desconhecido")
            if estado == "aberta":
                if protocol.upper() == "TCP" and banner:
                    os_info = get_os_info(banner)
                    line = f"[*] {ip_str}:{port}/TCP ABERTA - {servico} | Banner: {banner.strip()} | SO: {os_info}\n"
                    line += f"[?] BANNER: {banner.strip()}\n"
                    print_styled(f"[*] {ip_str}:{port}/TCP ABERTA - {servico} | SO: {os_info}", Fore.GREEN)
                    print_styled(f"[?] BANNER: {banner.strip()}", Fore.BLUE)
                else:
                    line = f"[*] {ip_str}:{port}/{protocol.upper()} ABERTA - {servico}\n"
                    print_styled(f"[*] {ip_str}:{port}/{protocol.upper()} ABERTA - {servico}", Fore.GREEN)
            elif estado == "filtrada":
                line = f"[-] {ip_str}:{port}/{protocol.upper()} FILTRADA - {servico}\n"
                print_styled(f"[-] {ip_str}:{port}/{protocol.upper()} FILTRADA - {servico}", Fore.YELLOW)
            elif estado == "fechada":
                line = f"[X] {ip_str}:{port}/{protocol.upper()} FECHADA\n"
                print_styled(f"[X] {ip_str}:{port}/{protocol.upper()} FECHADA", Fore.RED)
            report += line

    report += "\n[+] Varredura finalizada.\n"
    print_styled("\n[+] Varredura finalizada.\n", Fore.MAGENTA)

    save_option = input("Deseja salvar o relatório? [S/N]: ")
    if save_option.upper() == "S":
        save_report(report, f"scan_{network_cidr}.txt")

def main():
    print(pyfiglet.figlet_format("PDL Port Scanner"))
    mode = input("Escolha o modo [1: Host único | 2: Rede]: ")
    protocol = input("Escolha o protocolo [TCP/UDP]: ")
    ports = input("Escolha o range de portas [1: Well-Known | 2: Todas]: ")
    if mode not in ["1", "2"]:
        print_styled("Modo inválido", Fore.RED)
        return
    if protocol.upper() not in ["TCP", "UDP"]:
        print_styled("Protocolo inválido", Fore.RED)
        return
    if ports == "1":
        PORTS = WELL_KNOWN_PORTS
    elif ports == "2":
        PORTS = ALL_PORTS
    else:
        print_styled("Opção inválida", Fore.RED)
        return
    start_port = int(input("Porta inicial: "))
    end_port = int(input("Porta final: "))

    if mode == "1":
        host = input("Digite o host (IPv4 ou IPv6) (ex: 192.168.0.10 ou google.com): ")
        scan_host(host, start_port, end_port, PORTS, protocol=protocol)
    elif mode == "2":
        network_cidr = input("Digite a rede em formato CIDR (ex: 192.168.0.0/24 ou 2001:db8::/64):")
        scan_network(network_cidr, start_port, end_port, PORTS, protocol=protocol)
    else:
        print_styled("Modo inválido", Fore.RED)

if __name__ == "__main__":
    main()