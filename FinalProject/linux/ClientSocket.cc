#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#include "ClientSocket.h"

ClientSocket::ClientSocket(char *ipAddr, int portNum) {
    std::cout << "ClientSocket ctor starting.\n";

    //int sockfd, portno, n;
    //struct sockaddr_in serverAddr;
    //struct hostent *server;

    mySocket = socket(AF_INET, SOCK_STREAM, 0);
    if (mySocket < 0) error("ERROR: Can't open socket");

    //server = gethostbyname(ipAddr);
    //if (server == NULL) error("ERROR: Can't find host");

    std::cout << "ClientSocket ctor ending.\n";
}

ClientSocket::~ClientSocket() {

    std::cout << "TEST1\n";
    close(mySocket);
    std::cout << "TEST2\n";
}

void ClientSocket::makeConnection(char *ipAddr, int portNum) {

    struct sockaddr_in servAddr;
    struct hostent *server;
    int e;

    server = gethostbyname(ipAddr);
    if (server == NULL) error("ERROR: Can't find host");

    bzero((char *) &servAddr, sizeof(servAddr));

    servAddr.sin_family = AF_INET;
    bcopy((char *) server->h_addr, (char *) &servAddr.sin_addr.s_addr, server->h_length);
    //servAddr.sin_addr.s_addr = ipAddr;
    servAddr.sin_port = htons(portNum);

    std::cout << "TEST3\n";
    if (connect(mySocket, (struct sockaddr *) &servAddr, sizeof(servAddr)) < 0) error("ERROR: Couldn't connect\n");
    std::cout << "TEST4\n";

    int tmp;
    tmp = htonl(1);
    e = send(mySocket, &tmp, 4, 0);
    std::cout << "1: " << e << "\n";

    tmp = htonl(4);
    e = send(mySocket, &tmp, 4, 0);
    e = send(mySocket, "Name", 4, 0);
    
    tmp = htonl(5);
    e = send(mySocket, &tmp, 4, 0);
    e = send(mySocket, "Squig", 5, 0);

    char buffer[255];
    bzero(buffer, 255);
    int bytes;
    e = read(mySocket, buffer, strlen(buffer)+1);
    //std::cout << "Got this many bytes: " << e << "\n";
    bytes = recv(mySocket, buffer, strlen(buffer)-1, 0);
    std::cout << "Got this many bytes: " << bytes << "\n";
    //buffer[bytes] = '\0';

    for (int i=0; i<12; i++) std::cout << "CHECK IT: " << buffer[i] << "\n";

    std::cout << "GOT THIS: " << buffer << "\n";
    std::cout << "\n";

    while (1);
    
}

std::string sendMetadata(std:: string thing) {
    
}

void ClientSocket::error(const char *msg) {
    perror(msg);
    exit(0);
}
