# Projeto RSA com Comunicação TCP - Versão Avançada

Este projeto implementa um algoritmo RSA "from scratch" com comunicação via TCP, agora incluindo a troca de chaves do cliente e processamento adicional da mensagem. A comunicação ocorre entre dois arquivos Python: `servidor.py` e `cliente.py`.

## Visão Geral

### Servidor (`servidor.py`)
- Gera seu par de chaves RSA.
- Aguarda conexões no host `10.1.70.34` e porta `65432`.
- Envia sua chave pública para o cliente.
- Recebe a chave pública do cliente.
- Recebe a mensagem criptografada (ciphertext) enviada pelo cliente e a decripta usando sua chave privada.
- Converte a mensagem decriptografada para maiúsculas.
- Criptografa a mensagem em maiúsculas utilizando a chave pública do cliente.
- Envia o novo ciphertext de volta para o cliente.

### Cliente (`cliente.py`)
- Gera seu próprio par de chaves RSA (chave pública e chave privada).
- Conecta-se ao servidor no host `10.1.70.34` e porta `65432`.
- Recebe a chave pública do servidor.
- Envia sua chave pública para o servidor.
- Criptografa uma mensagem original usando a chave pública do servidor e a envia.
- Recebe o ciphertext modificado (mensagem em maiúsculas criptografada com sua chave pública) do servidor.
- Decripta a mensagem recebida usando sua chave privada, obtendo a mensagem final.

## Requisitos

- Python 3.x
- Bibliotecas padrão do Python: `socket`, `json`, `random`, `math`

## Instruções de Uso

### 1. Executar o Servidor

Abra um terminal e execute:
```
python servidor.py
```

O servidor gerará suas chaves RSA e ficará aguardando conexões no host 10.1.70.34 e porta 65432.

### 2. Executar o Cliente
Em outro terminal (ou em outra máquina, certificando-se de que o host 10.1.70.34 é acessível), execute:

```
python cliente.py
```
O cliente gerará seu par de chaves RSA, conectará ao servidor, realizará a troca de chaves e enviará a mensagem criptografada.

### 3. Fluxo de Comunicação

## Troca de Chaves:
- O servidor envia sua chave pública para o cliente.
- O cliente envia sua chave pública para o servidor.

## Envio e Processamento da Mensagem:
- O cliente criptografa uma mensagem original usando a chave pública do servidor e a envia.
- O servidor decripta a mensagem com sua chave privada, converte todos os caracteres para maiúsculas, recriptografa a mensagem com a chave pública do cliente e a envia de volta.

## Recepção e Decriptação:
- O cliente decripta a mensagem recebida utilizando sua chave privada, obtendo a mensagem final em maiúsculas.
