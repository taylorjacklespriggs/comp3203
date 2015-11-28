PROGRAM = DigiBoxClient

STD = -std=c++11

ODIR = object/

all:	$(ODIR) $(PROGRAM)

$(ODIR):
	mkdir -p $(ODIR)

$(PROGRAM):	$(ODIR)main.o $(ODIR)DigiBoxClient.o $(ODIR)ClientSocket.o $(ODIR)MetadataController.o
	g++ $(STD) -o $(PROGRAM) $(ODIR)main.o $(ODIR)DigiBoxClient.o $(ODIR)ClientSocket.o $(ODIR)MetadataController.o -ltag -lz

$(ODIR)main.o:	main.cc
	g++ -c main.cc -o $(ODIR)main.o

$(ODIR)DigiBoxClient.o:	DigiBoxClient.h DigiBoxClient.cc
	g++ $(STD) -c DigiBoxClient.cc -o $(ODIR)DigiBoxClient.o

$(ODIR)ClientSocket.o: ClientSocket.h ClientSocket.cc
	g++ $(STD) -c ClientSocket.cc -o $(ODIR)ClientSocket.o

$(ODIR)MetadataController.o:	MetadataController.h MetadataController.cc
	g++ $(STD) -c MetadataController.cc -o $(ODIR)MetadataController.o -ltag -lz
