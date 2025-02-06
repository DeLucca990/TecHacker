import socket
import ipaddress
from utils import WELL_KNOWN_PORTS

def scan_port(ip, port, timeout=1):
    """Faz o scan de uma porta TCP"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((ip, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

def scan_host(host, start_port, end_port):
    """Faz o scan de um host em um intervalo de portas"""
    print(f"\nIniciando varredura em: {host} | Portas: {start_port}-{end_port}")
    flag = False
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            flag = True
            service = WELL_KNOWN_PORTS.get(port, 'Serviço Desconhecido')
            print(f"Porta {port} ABERTA - Serviço: {service}")
    if not flag:
        print(f"Não foram encontradas portas abertas para o intervalo de portas especificado")
    print(f"Varredura finalizada\n")

def scan_network(network_cidr, start_port, end_port):
    """Faz o scan de portas em todos os IP's de uma rede"""
    network = ipaddress.ip_network(network_cidr, strict=False)
    print(f"\nIniciando varredura em: {network} | Portas: {start_port}-{end_port}")
    flag = False
    for ip in network.hosts():
        for port in range(start_port, end_port + 1):
            if scan_port(str(ip), port):
                flag = True
                service = WELL_KNOWN_PORTS.get(port, 'Serviço Desconhecido')
                print(f"IP {ip} - Porta {port} ABERTA - Serviço: {service}")
    if not flag:
        print(f"Não foram encontradas portas abertas para o intervalo de portas especificado")
    print(f"Varredura finalizada\n")

def main():
    print("Port Scan PDL")
    mode = input("Escolha o modo [1: Host único | 2: Rede]: ")

    start_port = int(input("Porta inicial: "))
    end_port = int(input("Porta final: "))

    if mode == "1":
        host = input("Digite o host (ex: 192.168.0.10 ou google.com): ")
        scan_host(host, start_port, end_port)
    elif mode == "2":
        network_cidr = input("Digite a rede em formato CIDR (ex: 192.168.0.0/24): ")
        scan_network(network_cidr, start_port, end_port)
    else:
        print("Modo inválido")

if __name__ == "__main__":
    main()