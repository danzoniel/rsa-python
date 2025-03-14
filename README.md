# Projeto RSA com Comunicação TCP

Este projeto implementa o algoritmo RSA "from scratch" com comunicação via TCP. Ele é composto por dois arquivos Python:

- `servidor.py`
- `cliente.py`

## Visão Geral

### Servidor (`servidor.py`)
- Gera as chaves RSA com um módulo de 4096 bits (utilizando dois primos de 2048 bits cada).
- Envia a chave pública para o cliente via TCP.
- Recebe o ciphertext criptografado enviado pelo cliente, decripta a mensagem e exibe o texto original.

### Cliente (`cliente.py`)
- Conecta-se ao servidor via TCP.
- Recebe a chave pública do servidor.
- Criptografa a mensagem:
  > "The information security is of significant importance to ensure the privacy of communications"
- Envia o ciphertext de volta para o servidor.

## Requisitos

- Python 3.x
- Bibliotecas padrão do Python: `socket`, `json`, `random`, `math`

## Instruções de Uso

### 1. Executar o Servidor

Abra um terminal e execute:
```
python servidor.py
```

### 2. Executar o Cliente
Em outro terminal (ou em outra máquina, ajustando o endereço IP se necessário), execute:
```
python cliente.py
```
O cliente se conectará ao servidor, receberá a chave pública, criptografará a mensagem e enviará o ciphertext para o servidor.

### 3. Verificação
No terminal do servidor, após receber o ciphertext, a mensagem decriptografada será exibida, confirmando o sucesso do processo de criptografia e decriptação.

## Estrutura do Código
##Servidor (servidor.py)

## Geração de Primos e Chaves RSA:
- Utiliza o teste de primalidade Miller-Rabin para gerar primos.
- Calcula N = p * q e a função totiente φ(N) = (p-1) * (q-1).
- Define o expoente público e (geralmente 65537) e calcula o inverso modular para obter a chave privada d.

## Comunicação TCP:
- Configura um socket TCP para escutar em localhost na porta 65432.
- Envia a chave pública (no formato JSON) para o cliente.
- Recebe o ciphertext, decripta a mensagem e exibe o resultado.

## Cliente (cliente.py)
## Comunicação TCP:
- Conecta-se ao servidor utilizando um socket TCP.
- Recebe a chave pública enviada pelo servidor (em formato JSON).

## Criptografia:
- Converte a mensagem em um inteiro.
- Aplica a fórmula RSA (C = M^e mod n) para criptografar a mensagem.
- Envia o ciphertext para o servidor.
