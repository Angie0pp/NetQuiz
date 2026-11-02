
import socket
import threading


HOST = "0.0.0.0"
PORT = 5000
MAX_PLAYERS = 5


players = {}


players_lock = threading.Lock()


def handle_player(client_socket, client_address):
    """Handle communication with an individual player."""

    print(f"[NEW CONNECTION] {client_address} connected.")

    try:
        
        client_socket.sendall(
            b"Welcome to NetQuiz Multiplayer System!\n"
        )

        
        client_socket.sendall(
            b"Enter your username:\n"
        )

        
        username = client_socket.recv(1024).decode("utf-8").strip()

        if not username:
            username = f"Player_{client_address[1]}"

        
        with players_lock:
            players[client_address] = username
            player_count = len(players)

        print(f"[PLAYER JOINED] {username}")
        print(f"[PLAYERS ONLINE] {player_count}/{MAX_PLAYERS}")

        client_socket.sendall(
            f"Hello {username}! You have joined NetQuiz.\n".encode("utf-8")
        )

        
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

    except ConnectionError:
        print(f"[CONNECTION LOST] {client_address}")

    except Exception as error:
        print(f"[ERROR] {error}")

    finally:
       
        with players_lock:
            username = players.pop(client_address, None)

        if username:
            print(f"[PLAYER LEFT] {username}")

        client_socket.close()


def start_server():
    """Start the NetQuiz TCP server."""

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))

    server.listen()

    print("=" * 45)
    print("       NETQUIZ MULTIPLAYER SERVER")
    print("=" * 45)
    print(f"[SERVER STARTED] Host: {HOST}")
    print(f"[SERVER STARTED] Port: {PORT}")
    print(f"[SERVER READY] Waiting for players...")
    print(f"[PLAYER CAPACITY] {MAX_PLAYERS}")
    print("=" * 45)

    try:
        while True:
            client_socket, client_address = server.accept()

            with players_lock:
                if len(players) >= MAX_PLAYERS:
                    client_socket.sendall(
                        b"SERVER FULL! Please try again later.\n"
                    )
                    client_socket.close()
                    print(f"[REJECTED] {client_address} - Server full.")
                    continue

                
                players[client_address] = None

            player_thread = threading.Thread(
                target=handle_player,
                args=(client_socket, client_address),
                daemon=True
            )

            player_thread.start()

    except KeyboardInterrupt:
        print("\n[SERVER STOPPED] Shutting down...")

    finally:
        with players_lock:
            connected_sockets = list(players.keys())

        
        server.close()
        print("[SERVER CLOSED]")


if __name__ == "__main__":
    start_server()
