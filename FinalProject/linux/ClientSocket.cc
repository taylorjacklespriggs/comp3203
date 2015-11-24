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
    mySocket = socket(AF_INET, SOCK_STREAM, 0);
    if (mySocket < 0) error("ERROR: Can't open socket");
}

ClientSocket::~ClientSocket() {

    close(mySocket);
}

void ClientSocket::makeConnection(char *ipAddr, int portNum) {

    struct sockaddr_in servAddr;
    struct hostent *server;

    server = gethostbyname(ipAddr);
    if (server == NULL) error("ERROR: Can't find host");

    bzero((char *) &servAddr, sizeof(servAddr));

    servAddr.sin_family = AF_INET;
    bcopy((char *) server->h_addr, (char *) &servAddr.sin_addr.s_addr, server->h_length);
    servAddr.sin_port = htons(portNum);

    if (connect(mySocket, (struct sockaddr *) &servAddr, sizeof(servAddr)) < 0) error("ERROR: Couldn't connect\n");
}

std::string sendMetadata(std:: string thing) {
    
}

void ClientSocket::error(const char *msg) {
    perror(msg);
    exit(0);
}

int ClientSocket::sendInt(int msg) {
    int tmp = htonl(msg);
    return send(mySocket, &tmp, 4, 0);
}

int ClientSocket::sendString(char *msg) {
    int msgLen = strlen(msg);
    sendInt(msgLen);
    return send(mySocket, msg, msgLen, 0);
}

int ClientSocket::recvInt() {
    int tmp = 0;
    recv(mySocket, &tmp, 4, 0);
    return ntohl(tmp);
}

std::string ClientSocket::recvString() {
    int len = recvInt();
    char buffer[len];
    recv(mySocket, buffer, len, 0);
    buffer[len] = '\0';
    std::string retval(buffer);
    return retval;
}