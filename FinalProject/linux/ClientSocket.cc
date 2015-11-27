#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <fstream>

#include "ClientSocket.h"

ClientSocket::ClientSocket() {
}

ClientSocket::~ClientSocket() {

    close(mySocket);
}

void ClientSocket::makeConnection(char *ipAddr, int portNum) {
    mySocket = socket(AF_INET, SOCK_STREAM, 0);
    if (mySocket < 0) error("Couldn't open socket\n");

    struct sockaddr_in servAddr;
    struct hostent *server;

    server = gethostbyname(ipAddr);
    if (server == NULL) error("Couldn't find host\n");

    bzero((char *) &servAddr, sizeof(servAddr));

    servAddr.sin_family = AF_INET;
    bcopy((char *) server->h_addr, (char *) &servAddr.sin_addr.s_addr, server->h_length);
    servAddr.sin_port = htons(portNum);

    if (connect(mySocket, (struct sockaddr *) &servAddr, sizeof(servAddr)) < 0) error("Couldn't connect\n");
}

int ClientSocket::serverBind() {
    mySocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (mySocket < 0) error("Couldn't open socket\n");

    struct sockaddr_in servAddr;
    servAddr.sin_family = AF_INET;
    servAddr.sin_addr.s_addr = INADDR_ANY;
    servAddr.sin_port = htons(0); //Let OS assign port

    if (bind(mySocket, (struct sockaddr *) &servAddr, sizeof(servAddr)) < 0) error("Couldn't bind\n");

    struct sockaddr_in sin;
    socklen_t len = sizeof(sin);
    if (getsockname(mySocket, (struct sockaddr *)&sin, &len) == -1)
        perror("In getsockname\n");

    return ntohs(sin.sin_port);
}

std::string sendMetadata(std:: string thing) {
    
}

void ClientSocket::error(const char *msg) {
    perror(msg);
    exit(0);
}

void ClientSocket::sendInt(int msg) {
    int tmp = htonl(msg);
    int success = send(mySocket, &tmp, 4, 0);
    if (success < 0) error("Problem sending int\n");
}

void ClientSocket::sendString(char *msg) {
    int msgLen = strlen(msg);
    sendInt(msgLen);
    int success = send(mySocket, msg, msgLen, 0);
    if (success < 0) error("Problem sending string\n");
}

int ClientSocket::recvInt() {
    int tmp = 0;
    int success = recv(mySocket, &tmp, 4, 0);
    if (success < 0) error("Problem receiving int\n");
    return ntohl(tmp);
}

std::string ClientSocket::recvString() {
    int len = recvInt();
    char buffer[len];
    int success = recv(mySocket, buffer, len, 0);
    if (success < 0) error("Problem receiving string\n");
    buffer[len] = '\0';
    std::string retval(buffer);
    return retval;
}

void ClientSocket::recvToken(int *port, char *token) {
    char buffer[132];
    int success = recv(mySocket, buffer, 132, 0);
    if (success < 0) error("Problem receiving token\n");

    *port = ntohl(*(int*) (void *)buffer);

    memcpy(token, buffer+4, 128);
}

void ClientSocket::sendToken(char *token) {
    int success = send(mySocket, token, 128, 0);
    if (success < 0) error("Problem sending token\n");
}

void ClientSocket::sendFile(std::string fileName) {
    std::cout << "STREAMING FILE: " << fileName << "\n";

    std::ifstream infile;
    infile.open(fileName.c_str(), std::ios::binary|std::ios::in|std::ios::ate);

    int BUFFERSIZE = 512;
    infile.seekg(0, std::ios::beg);

    while (!infile.eof()) {
        char buffer[BUFFERSIZE];
        infile.read(buffer, BUFFERSIZE);
        sendInt(infile.gcount());
        send(mySocket, buffer, infile.gcount(), 0);
    }

    sendInt(0);
    infile.close();
}
