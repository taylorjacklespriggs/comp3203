PROGRAM = DigiBoxClient

ODIR = object/

all:	$(ODIR) $(PROGRAM)

$(ODIR):
	mkdir -p $(ODIR)

$(PROGRAM):	$(ODIR)main.o $(ODIR)DigiBoxClient.o $(ODIR)ClientSocket.o
	g++ $(STD) -o $(PROGRAM) $(ODIR)main.o $(ODIR)DigiBoxClient.o $(ODIR)ClientSocket.o

$(ODIR)main.o:	main.cc
	g++ -c main.cc -o $(ODIR)main.o

$(ODIR)DigiBoxClient.o:	DigiBoxClient.h DigiBoxClient.cc
	g++ -c DigiBoxClient.cc -o $(ODIR)DigiBoxClient.o

$(ODIR)ClientSocket.o: ClientSocket.h ClientSocket.cc
	g++ -c ClientSocket.cc -o $(ODIR)ClientSocket.o
