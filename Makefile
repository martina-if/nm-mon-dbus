CFLAGS=-Wall
DFLAGS=-g -Wall
FLAGS=-fPIC
LDFLAGS=-lxcb

TARGET=libwmname.so
OBJECT_FILES=wmname.o

all: $(TARGET)

$(TARGET): $(OBJECT_FILES)
	$(CC) -shared -Wl,-soname,$(TARGET) -o $(TARGET) $(OBJECT_FILES) $(LDFLAGS)

%.o : %.c
	$(CC) $(CFLAGS) $(FLAGS) -c $< -o $@

test:
	$(CC) $(DFLAGS) wmname.c -o test_wmname $(LDFLAGS)

clean:
	rm -f *.o *.so test_wmname

