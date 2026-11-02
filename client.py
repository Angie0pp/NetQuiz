
import socket


HOST = "127.0.0.1"
PORT = 5000


def start_client():

    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        print("Connecting to NetQuiz server...")

        client.connect((HOST, PORT))

        print("[CONNECTED] Successfully connected to NetQuiz!")

        
        reader = client.makefile("r", encoding="utf-8")

        
        welcome = reader.readline()
        print(welcome.strip())

        
        if welcome.startswith("SERVER FULL!"):
            return

       
        prompt = reader.readline()
        print(prompt.strip())

       
        username = input("Your username: ").strip()

        while not username:
            username = input("Username cannot be empty. Try again: ").strip()

        
        client.sendall((username + "\n").encode("utf-8"))

        
        response = reader.readline()
        print(response.strip())

        print("\nYou are now connected to NetQuiz!")
        print("Waiting for the quiz to begin...")
        print("Type 'exit' to disconnect.\n")

        
        while True:
            command = input("NetQuiz > ").strip().lower()

            if command == "exit":
                print("Leaving NetQuiz...")
                break

            print("The quiz has not started yet. Please wait.")

    except ConnectionRefusedError:
        print("[ERROR] Could not connect to the server.")
        print("Make sure server.py is running.")

    except ConnectionError:
        print("[ERROR] Connection to the server was lost.")

    except Exception as error:
        print(f"[ERROR] {error}")

    finally:
        client.close()
        print("[DISCONNECTED] Client connection closed.")


if __name__ == "__main__":
    start_client()
