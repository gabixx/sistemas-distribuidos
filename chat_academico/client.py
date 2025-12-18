import socket
import threading

username = input("Escolha seu nome de usuário: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    """Escuta mensagens do servidor."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USER':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print("Erro na conexão!")
            client.close()
            break

def write():
    """Envia mensagens para o servidor."""
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('utf-8'))

# Inicia threads para receber e enviar dados ao mesmo tempo
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()