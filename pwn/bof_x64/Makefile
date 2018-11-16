binary : src.c
	gcc -o binary src.c \
	-O0 \
	-mpreferred-stack-boundary=4 \
	-fno-stack-protector \
	-zexecstack \
	-Wl,-z,relro \
	-no-pie

clean :
	rm binary
