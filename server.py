import socket
import json
import random
from math import gcd

# Função Miller-Rabin para teste de primalidade
def is_probable_prime(n, k=40):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Gera um número primo com o número de bits desejado
def generate_prime(bit_length):
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1  # Garante que candidate tenha o tamanho correto e seja ímpar
        if is_probable_prime(candidate):
            return candidate

# Algoritmo Estendido de Euclides para calcular o inverso modular
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise Exception('O inverso modular não existe.')
    return x % phi

# Gera as chaves RSA: para ter n com 4096 bits, p e q terão 2048 bits cada.
def generate_keys(bit_length=2048):
    print("Gerando o primeiro primo p...")
    p = generate_prime(bit_length)
    print("Primo p gerado.")
    print("Gerando o segundo primo q...")
    q = generate_prime(bit_length)
    print("Primo q gerado.")
    n = p * q
    phi = (p - 1) * (q - 1)
    # Valor comum para e
    e = 65537
    if gcd(e, phi) != 1:
        raise Exception("e e φ(n) não são coprimos; tente gerar novos primos.")
    d = mod_inverse(e, phi)
    return (e, d, n)

# Converte uma string em inteiro (usando codificação UTF-8)
def text_to_int(text):
    return int.from_bytes(text.encode('utf-8'), byteorder='big')

# Converte um inteiro de volta para string
def int_to_text(i):
    num_bytes = (i.bit_length() + 7) // 8
    return i.to_bytes(num_bytes, byteorder='big').decode('utf-8')

# Função de criptografia: C = M^e mod n
def encrypt(message, key, n):
    message_int = text_to_int(message)
    cipher_int = pow(message_int, key, n)
    return cipher_int

# Função de decriptação: M = C^d mod n
def decrypt(cipher_int, key, n):
    message_int = pow(cipher_int, key, n)
    return int_to_text(message_int)

def main():
    print("Gerando chaves RSA (n terá 4096 bits)...\nEsse processo pode demorar alguns minutos.")
    e, d, n = generate_keys(2048)
    print("\nChaves geradas com sucesso!")
    print("Chave Pública (e, n):")
    print(f"e = {e}\n n = {n}\n")
    print("Chave Privada (d, n):")
    print(f"d = {d}\n n = {n}\n")
    
    # Configura o servidor TCP
    HOST = '10.1.70.34'  # ou '' para aceitar conexões de todas as interfaces
    PORT = 65432        # porta definida para comunicação
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Servidor aguardando conexão em {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print("Conexão estabelecida com", addr)
            # Envia a chave pública para o cliente em formato JSON
            public_key = json.dumps({"e": e, "n": n})
            conn.sendall(public_key.encode('utf-8'))
            print("Chave pública enviada para o cliente.")
            
            # Aguarda o ciphertext enviado pelo cliente
            data = conn.recv(4096)
            if not data:
                print("Nenhum dado recebido.")
                return
            ciphertext_str = data.decode('utf-8').strip()
            cipher_int = int(ciphertext_str)
            print("\nCiphertext recebido:")
            print(cipher_int)
            
            # Decripta a mensagem recebida
            decrypted_message = decrypt(cipher_int, d, n)
            print("\nMensagem decriptografada:")
            print(decrypted_message)

if __name__ == "__main__":
    main()
