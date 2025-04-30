# Roteiro 2 - Respostas
1. **Ferramentas de reconhecimento mais úteis além do Port Scan**

    **1.1 Shodan** – motor de busca que indexa banners de serviços expostos. Ele permite filtrar resultados por CVE, versão ou palavra-chave e se tornou indispensável para identificar dispositivos IoT e serviços de CI/CD abertos. Em janeiro de 2025, pesquisadores mostraram como operadores de ransomware exploraram o search engine para localizar instâncias Jenkins vulneráveis e depois lançar exploits automatizados. [Link1](https://firecompass.com/jenkins-cve-2024-23897-vulnerability-exposed/?), [Link2](https://www.vectra.ai/blog/how-attackers-use-shodan-fofa)

    **1.2 theHarvester** – ferramenta OSINT capaz de reunir e-mails corporativos, subdomínios, IPs e nomes de funcionários a partir de fontes públicas (Google, Bing, LinkedIn, GitHub, etc.). Pentesters costumam usá-la para montar listas de spear-phishing ou descobrir infraestrutura de terceiros; laboratórios didáticos de 2024 mostram sua aplicação prática em coletas pré-ataque. [Link1](https://github.com/laramies/theHarvester), [Link2](https://hassen-hannachi.medium.com/lab-8-information-gathering-using-theharvester-ce7f4b88c393)

    **1.3 OWASP Amass** – realiza enumeração passiva e ativa de subdomínios, mapeia ASNs e constrói um grafo da superfície externa. Em oficinas da Recon Village (DEF CON 31 / 2024), equipes de bug bounty relataram como o Amass revelou APIs “shadow” que não constavam nos registros oficiais do cliente, permitindo relatórios premiados. [Link](https://github.com/owasp-amass/amass)

    **1.4 Maltego** – plataforma de correlação gráfica que cruza domínios, certificados, perfis sociais e endereços IP, desenhando relações ocultas. A Cyber Police da Ucrânia divulgou estudo de caso em que Maltego foi decisivo para mapear afiliados de ransomware e suas infraestruturas de suporte. [Link](https://www.maltego.com/blog/case-study-ukrainian-cyber-police-fights-crime-with-maltego)

    **1.5 Gobuster** – brute-forcer escrito em Go para enumeração de diretórios, vhosts e subdomínios. Exercícios da sala “Skynet” (TryHackMe, 2025) mostram como ele encontrou caminhos como /backup/ contendo ZIPs com credenciais, algo recorrente em programas de bug bounty. [Link](https://tryhackme.com/resources/blog/skynet-writeup)

2. **Diferenças entre um SYN Scan e um TCP Connect Scan**

    Em um SYN Scan (Nmap -sS), o atacante envia apenas o primeiro passo do three-way handshake (SYN). Se o alvo responder com SYN/ACK, o scanner devolve um RST e encerra a sessão (por isso é chamado de half-open). Esse método exige privilégios para pacotes crus, é rápido e produz menos ruído em logs, embora IDS modernos ainda o detectem. Já o TCP Connect Scan (Nmap -sT) utiliza a chamada de sistema connect(), completando todo o handshake. Não requer privilégios de root, mas é mais lento e inevitavelmente registrado pelos serviços de destino. Assim, o SYN Scan é preferido quando se quer velocidade e certa discrição; o TCP Connect serve quando o usuário não tem acesso a raw sockets ou quando firewalls bloqueiam pacotes artesanais.

3. **Técnicas para evitar detecção por IPS durante o reconhecimento**

    **3.1** Reduzir a taxa de pacotes (--scan-delay / --min-rate) mantém o fluxo abaixo dos limiares de detecção de muitos IPS; a desvantagem é um reconhecimento bem mais demorado.

    **3.2** Fragmentar pacotes (--mtu) pode confundir IPS que não reassemblem pacotes, embora muitos já consigam detectar fragmentos.

    **3.3** Usar IPs decoy (-D RND:10) mistura tráfego real com pacotes de endereços-isca, dificultando atribuição. A eficácia depende da qualidade dos decoys e pode poluir os próprios logs do pentester.

    **3.4** Idle Scan / spoofing (-sI) explora um host “zumbi” para enviar pacotes e ler variação de IP ID, permitindo varredura sem que o endereço real toque no alvo. Requer máquina ociosa e resulta em respostas mais limitadas. 

    **3.5** Alterar o User-Agent (-A) pode ajudar a evitar bloqueios em aplicações web, mas não é eficaz contra IPS.

    **3.6** Utilizar proxies ou VPNs pode ocultar o IP real, mas pode introduzir latência e não é infalível contra logs de acesso.

    **3.7** Ordem aleatória e varredura seletiva (--randomize-hosts, --top-ports) quebra padrões sequenciais que gatilham correlações em IPS, mas sacrifica a descoberta rápida de blocos contíguos de serviços.