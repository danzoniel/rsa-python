import socket
import json
import random
from math import gcd

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
        raise Exception("O inverso modular não existe.")
    return x % phi

# Geração de chaves RSA
def generate_keys(bit_length=2048):
    def is_probable_prime(n, k=40):
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        s, d = 0, n - 1
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

    def generate_prime(bits):
        while True:
            candidate = random.getrandbits(bits)
            candidate |= (1 << (bits - 1)) | 1
            if is_probable_prime(candidate):
                return candidate

    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    return e, d, n

# Funções de conversão entre texto e inteiro
def text_to_int(text):
    return int.from_bytes(text.encode('utf-8'), byteorder='big')

def int_to_text(i):
    num_bytes = (i.bit_length() + 7) // 8
    return i.to_bytes(num_bytes, byteorder='big').decode('utf-8')

# Funções de criptografia e decriptação RSA
def encrypt(message, key, n):
    message_int = text_to_int(message)
    return pow(message_int, key, n)

def decrypt(cipher_int, key, n):
    message_int = pow(cipher_int, key, n)
    return int_to_text(message_int)

def main():
    HOST = '10.1.70.34'
    PORT = 65432

    print("Gerando chaves RSA do cliente...")
    # Para testes, usamos 512 bits; em produção, utilize 2048 bits ou conforme necessário.
    client_e, client_d, client_n = generate_keys(512)
    print("Chaves do cliente geradas.")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor {HOST}:{PORT}")

        # Receber a chave pública do servidor
        data = s.recv(4096)
        if not data:
            print("Nenhuma chave pública do servidor recebida.")
            return
        server_pub = json.loads(data.decode('utf-8'))
        server_e = server_pub["e"]
        server_n = server_pub["n"]
        print("Chave pública do servidor recebida.")

        # Enviar a chave pública do cliente para o servidor
        client_pub = {"e": client_e, "n": client_n}
        s.sendall(json.dumps(client_pub).encode('utf-8'))
        print("Chave pública do cliente enviada ao servidor.")

        # Mensagem original a ser enviada ao servidor
        original_message = "The information security is of significant importance to ensure the privacy of communications"
        print("Mensagem original:", original_message)

        # Criptografar a mensagem usando a chave pública do servidor
        ciphertext = encrypt(original_message, server_e, server_n)
        print("Mensagem criptografada (ciphertext):", ciphertext)

        # Enviar o ciphertext para o servidor
        s.sendall(str(ciphertext).encode('utf-8'))
        print("Ciphertext enviado ao servidor.")

        # Receber o novo ciphertext do servidor (mensagem em maiúsculas criptografada com a chave pública do cliente)
        data = s.recv(4096)
        if not data:
            print("Nenhum ciphertext recebido do servidor.")
            return
        new_ciphertext = int(data.decode('utf-8').strip())
        print("Novo ciphertext recebido do servidor:", new_ciphertext)

        # Decriptografar a mensagem usando a chave privada do cliente
        decrypted_message = decrypt(new_ciphertext, client_d, client_n)
        print("Mensagem decriptografada recebida do servidor:", decrypted_message)

if __name__ == "__main__":
    main()
