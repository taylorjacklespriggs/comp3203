BINARY=comp3203
SOURCES=ui/ClientGUI.cpp metadata/MetadataController.cpp network/NetworkController.cpp DigiBoxClient.cpp main.cpp
LDFLAGS=-Wl,-Bdynamic `pkg-config gtkmm-3.0 --cflags --libs` -Wl,-Bstatic -lws2_32 -lIPHLPAPI -ltag -lz  
CFLAGS=-c -std=c++11 `pkg-config gtkmm-3.0 --cflags --libs`
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
