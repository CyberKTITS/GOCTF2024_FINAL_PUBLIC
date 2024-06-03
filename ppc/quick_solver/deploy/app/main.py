import socket
import os
from random import choice, randint
import threading

import numpy as np

FLAG = os.environ.get("FLAG")

if FLAG is None:
    FLAG = "flag{fake_flag}"
    
FLAG_PARTS =  [FLAG[i:i+26] for i in range(0, len(FLAG), 26)]

ROUNDS = 500 - len(FLAG_PARTS)

    
def generate_system_of_equation(answers):
    if len(answers) < 1:
        raise ValueError("The answers array must contain at least one value")
    
    num_vars = len(answers)
    
    x = np.array(answers).reshape((num_vars, 1))
    A = np.random.randint(1, 100, size=(num_vars, num_vars))
    b = np.dot(A, x)
    A = A.tolist()
    b = b.flatten().tolist()
    
    variables = [chr(ord('a') + i) for i in range(num_vars)]
    equations = []
    
    for row in A:
        equation = " + ".join(f"{coef}*{var}" for coef, var in zip(row, variables))
        equations.append(f"{equation} = {b.pop(0)}")
    return equations, answers

def handle_client(client_socket, client_address):
    client_socket.send(b"Here is an example!\n\n")
    
    example_eq, example_ans = generate_system_of_equation([randint(4,10) for _ in range(randint(2,5))])
    for eq in example_eq:
        client_socket.send(eq.encode())
        client_socket.send(b"\n")
    client_socket.send(b"\nSolutions (in alphabetical order of variables): ")
    client_socket.send(str(example_ans).encode() + b"\n")

    client_socket.send(b"1... 2... 3... Solve!\n\n")
    
    flag_sending_round = randint(100, 500)
    
    for rnd in range(ROUNDS):
        if rnd == flag_sending_round:
            for part in FLAG_PARTS:
                part = [ord(char) for char in part]
                equations, solutions = generate_system_of_equation(part)
                for eq in equations:
                    client_socket.send(eq.encode())
                    client_socket.send(b"\n")
                client_socket.send(b"Solutions (in alphabetical order of variables):")
                response = client_socket.recv(1024)
                if response.decode().strip() == str(solutions):
                        client_socket.send(b"\n")
                        continue
                else:
                    client_socket.send(b"Wrong!!!\n")
                    client_socket.close()
                    break
        else:
            equations, solutions = generate_system_of_equation([randint(50, 750) for _ in range(randint(8, 18))])
            # print(solutions)
            for eq in equations:
                client_socket.send(eq.encode())
                client_socket.send(b"\n")
            client_socket.send(b"Solutions (in alphabetical order of variables):")
            response = client_socket.recv(1024)
            if response.decode().strip() == str(solutions):
                    client_socket.send(b"\n")
                    continue
            else:
                client_socket.send(b"Wrong!!!\n")
                client_socket.close()
                break
    
    client_socket.send(b"Job Done! Goodbye! Your flag is goctf{b0a16919d9275dbb09e88264cb6c2fe3}\n\n P.S. Maybe you skipped something?")
    client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]}")

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server("0.0.0.0", 1488)