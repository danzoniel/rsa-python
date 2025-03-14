import socket
import json

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

def main():
    HOST = 'localhost'  # Endereço do servidor
    PORT = 65432        # Porta do servidor

    # Conecta ao servidor via TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado ao servidor em {HOST}:{PORT}")
        
        # Recebe a chave pública do servidor
        data = s.recv(4096)
        public_key = json.loads(data.decode('utf-8'))
        e = public_key["e"]
        n = public_key["n"]
        print("Chave pública recebida:")
        print(f"e = {e}\n n = {n}\n")
        
        # Mensagem a ser criptografada
        message = "The information security is of significant importance to ensure the privacy of communications"
        print("Mensagem a ser criptografada:")
        print(message)
        
        # Criptografa a mensagem utilizando a chave pública
        cipher_int = encrypt(message, e, n)
        print("\nMensagem criptografada (ciphertext):")
        print(cipher_int)
        
        # Envia o ciphertext para o servidor
        s.sendall(str(cipher_int).encode('utf-8'))
        print("Ciphertext enviado ao servidor.")

if __name__ == "__main__":
    main()
