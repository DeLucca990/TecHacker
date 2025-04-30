# PDL CLI Scanner - Ferramenta de Reconhecimento e Varredura

## Descrição
O PDL CLI Scanner é uma ferramenta de linha de comando desenvolvida em Python para realizar reconhecimento e varredura em alvos específicos. A ferramenta é projetada para ser simples de usar, permitindo que os usuários realizem uma variedade de tarefas de segurança cibernética.

## Funcionalidades

| Módulo                  | Descrição                                                                 |
|-------------------------|---------------------------------------------------------------------------|
| PortScan                | Varredura TCP/UDP com banner grabbing e detecção de sistema operacional. |
| WHOIS Lookup            | Consulta WHOIS de domínios.                                               |
| DNS Enumeration         | Coleta registros DNS (A, MX, NS, TXT, etc).                              |
| Subdomain Scanner       | Busca subdomínios via wordlist.                                          |
| Wappalyzer-like Scanner | Identifica tecnologias usadas em sites.                                  |

---

## Estrutura do Projeto
```
Roteiro2-ScanModule/
├── modules/
│   ├── portscan.py
│   ├── whois_lookup.py
│   ├── dns_enum.py
│   ├── subdomain.py
│   └── wappalyzer.py
├── reports/
├── utils/
│   ├── dict_ports.py
│   ├── utils.py
├── wordlist/
│   ├── subdomains_large.txt
│   └── subdomains_small.txt
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/DeLucca990/TecHacker.git
    # ou
    git clone git@github.com:DeLucca990/TecHacker.git
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv .venv
    # ou
    python3 -m venv .venv
    ```
    Ative o ambiente virtual:
    - No Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - No Linux/Mac:
      ```bash
      source .venv/bin/activate
      ```
3. Navegue até o diretório do projeto:
    ```bash
    cd TecHacker/Roteiro2-ScanModule
    ```
4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
  
## Uso
1. Execute o script principal:
    ```bash
    python main.py
    # ou
    python3 main.py
    ```
2. Escolha o módulo desejado e siga as instruções na tela.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir um issue ou pull request.