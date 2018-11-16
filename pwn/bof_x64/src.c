#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	char buf[256] = {0,};
	
	init();
	read(0, buf, 1024);
	write(1, buf, 256);
	return 0;
}

int init() {
	setreuid(geteuid());
	setregid(getegid());
}
