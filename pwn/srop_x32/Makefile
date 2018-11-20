binary : src.c
	gcc -o binary src.c \
	-m32 \
	-O0 \
	-mpreferred-stack-boundary=2 \
	-fno-stack-protector \
	-zexecstack \
	-Wl,-z,relro \
	-no-pie

clean :
	rm binary
