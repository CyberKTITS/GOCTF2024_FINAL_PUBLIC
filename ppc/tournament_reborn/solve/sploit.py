from pwn import *
import sys
import re
import math

if len(sys.argv) >= 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = "localhost"
    PORT = 8081

calming = False
punishing = False
punishment_count = 0
punishment_limit = 0

def strategy(enemy_history, calming, punishing, punishment_count, punishment_limit):
    if calming:
        calming = False
        return b"C"

    if punishing:
        if punishment_count < punishment_limit:
            punishment_count += 1
            return b"D"
        else:
            calming = True
            punishing = False
            punishment_count = 0
            return b"C"

    if "D" in enemy_history[-1:]:
        punishing = True
        punishment_count += 1
        punishment_limit += 1
        return b"D"

    return b"C"
    

conn = remote(HOST, PORT)
# conn.interactive()

data = conn.recvuntil(b"action [C or D] for me: ")
# print(data)



while True:
    # print(data)
    # print(history[-10:], enemy_history[-10:])
    if b"New match started!" in data:
        history = []
        enemy_history = []
        is_enemy_random = False

    if b"opponent" in data:
        matches = re.findall(r'You played (\w), opponent played (\w)', data.decode())
        history.append(matches[0][0])
        enemy_history.append(matches[0][1])
        turn = strategy(enemy_history, calming, punishing, punishment_count, punishment_limit)
        conn.sendline(turn)
    else:
        conn.sendline(b"C")
            
    data = conn.recvuntil(b"action [C or D] for me: ", timeout=2)
    if b"action [C or D] for me:" not in data:
        conn.interactive()
        break
    
    
