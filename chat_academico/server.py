import socket
import threading

# Configurações do Servidor
HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def broadcast(message):
    """Envia mensagem para todos os clientes conectados."""
    for client in clients:
        client.send(message)

def handle_client(client):
    """Gerencia a comunicação individual de cada cliente."""
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} saiu do chat!'.encode('utf-8'))
            usernames.remove(username)
            break

def receive():
    """Aceita novas conexões."""
    print(f"Servidor rodando em {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Conectado com {str(address)}")

        client.send('USER'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(f"Usuário: {username}")
        broadcast(f"{username} entrou no chat!".encode('utf-8'))
        client.send('Conectado ao servidor acadêmico!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()