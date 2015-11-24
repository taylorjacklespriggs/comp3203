BINARY=comp3203
SOURCES=MetadataController.cpp main.cpp
LDFLAGS=-ltag -lz
CFLAGS=-c -std=c++11
CC=g++

OBJECTS=$(SOURCES:.cpp=.o)
INCFLAGS=
LIBFLAGS=

all: $(SOURCES) $(BINARY)

$(BINARY): $(OBJECTS)
	$(CC) $(LIBFLAGS) $(OBJECTS) $(LDFLAGS) -o $@
	
.cpp.o:
	$(CC) $(INCFLAGS) $(CFLAGS) -fPIC $< -o $@
	
distclean: clean
	rm -f $(BINARY)
	
clean:
	rm -f $(OBJECTS)
