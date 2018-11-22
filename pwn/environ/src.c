#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <dlfcn.h>

int init_func() {
	setreuid(geteuid(), geteuid());
	setregid(getegid(), getegid());

	void (*printf_addr)() = dlsym(RTLD_NEXT, "printf");
	printf("Printf() : %p\n", printf_addr);
	return 0;
}

int vuln() {
	char buf[20];
	char * addr;
	void (*ptr)(void);

	puts("Tell me the address to \"Leak\" : ");
	fgets(buf, 20, stdin);
	addr = atoll(buf);
	write(1, addr, 4);

	puts("\nTell me the address to \"Jump\" : ");
	fgets(buf, 20, stdin);
	addr = atoll(buf);
	ptr = (void (*)(void))addr;
	ptr();

	puts("Did u got it?");
	exit(0);
}

int main(int argc, char **argv, char **envp) {
	char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80";

	init_func();
	vuln();
	return 0;
}
