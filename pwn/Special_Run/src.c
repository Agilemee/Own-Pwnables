#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int init_func() {
    setreuid(geteuid(), geteuid());
    setregid(getegid(), getegid());
}

int check(const char *str) {
    const char *filter = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/\\";
    char *index = str;
    int result = 0;

    while (*index) {
        if (strchr(filter, *index)) 
            result = 1;
        index++;
    }

    return result;
}

int main() {
	char buf[128] = {0,};

    init_func();

    puts("input >");
	read(0, buf, 128-1);

	if(check(buf)) {
        puts("nop. rejected!");
		return -1;
	} else {
        puts("yes, gogogo!");
		system(buf);
	}

    puts("got it?");

	return 0;
}