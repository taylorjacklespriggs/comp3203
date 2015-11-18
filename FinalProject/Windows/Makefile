BINARY=comp3203
SOURCES=MetadataController.cpp main.cpp
LDFLAGS=-static -ltag -lz
CFLAGS=-c -std=c++11
CC=g++

OBJECTS=$(SOURCES:.cpp=.o)
INCFLAGS=-I/c/Libraries/taglib/include
LIBFLAGS=-L/c/Libraries/taglib/lib

all: $(SOURCES) $(BINARY)

$(BINARY): $(OBJECTS)
	$(CC) $(LIBFLAGS) $(OBJECTS) $(LDFLAGS) -o $@
	
.cpp.o:
	$(CC) $(INCFLAGS) $(CFLAGS) -fPIC $< -o $@
	
distclean: clean
	rm -f $(BINARY)
	
clean:
	rm -f $(OBJECTS)