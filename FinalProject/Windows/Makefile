BINARY=comp3203
SOURCES=metadata/MetadataController.cpp network/NetworkController.cpp main.cpp
LDFLAGS=-lws2_32 -static -ltag -lz
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