# Roteiro 3: Squid Proxy - Controle de Acesso à Web

Este projeto utiliza o **Squid Proxy** para controlar o acesso a determinados sites e conteúdos na rede local. A configuração aplica dois conjuntos de regras:

---

## Exercício 1: Bloqueio por IP e Domínio

- Bloqueia o acesso aos sites `facebook.com` e `youtube.com` para **toda a rede**.
- Libera o acesso a esses dois sites **apenas para o IP `192.168.0.100`**.

---

## Exercício 2: Bloqueio por Expressão e Liberação de Domínio

- Bloqueia qualquer URL que contenha a **palavra "terra"**.
- Libera o site `terraviva` para toda a rede, mesmo contendo a palavra "terra".

---

## Como usar

### 1. Instale o Squid

```bash
sudo apt update
sudo apt install squid -y
```

### 2. Configure o Squid
Salve o conteúdo do squid.conf fornecido neste projeto no local correto (pode variar por distro):

```bash
sudo cp squid.conf /etc/squid/squid.conf
```

### 3. Reinicie o Squid

```bash
sudo systemctl restart squid
```

### 4. Verifique o status do Squid

```bash
sudo systemctl status squid
```

### 5. Teste as regras
- Acesse os sites `facebook.com` e `youtube.com` a partir de um navegador em um dispositivo na rede local.
- Tente acessar o site `terraviva` e verifique se ele está acessível.
- Tente acessar qualquer URL que contenha a palavra "terra" e verifique se o acesso é bloqueado.
- Tente acessar o site `terraviva` com a palavra "terra" e verifique se ele está acessível.
