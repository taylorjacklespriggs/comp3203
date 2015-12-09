#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
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
        error("In getsockname\n");

    return ntohs(sin.sin_port);
}

void ClientSocket::findServer(int broadcastPort, char *retAddr, int *retPort, int *retPlayPort) {
    mySocket = socket(AF_INET, SOCK_DGRAM, 0);
    if (mySocket < 0) error("Couldn't open socket\n");

    int broadcastPermission = 1;
    if (setsockopt(mySocket, SOL_SOCKET, SO_BROADCAST, (void *) &broadcastPermission,
                sizeof(broadcastPermission)) < 0) error("setsockopt() failed");

    struct sockaddr_in broadcastAddr;
    broadcastAddr.sin_family = AF_INET;
    inet_pton(AF_INET, "255.255.255.255", &(broadcastAddr.sin_addr));
    broadcastAddr.sin_port = htons(broadcastPort);

    short int x = 0;
    if (sendto(mySocket, &x, sizeof(x), 0, (struct sockaddr *) &broadcastAddr,
                sizeof(broadcastAddr)) != sizeof(x)) {
        error("sendto() sent a different number of bytes than expected");
    }

    int numbytes;
    struct sockaddr_in their_addr;
    struct {
       int a,b;
    } thing;
    socklen_t addr_len;
    addr_len = sizeof their_addr;
    if ((numbytes = recvfrom(mySocket, &thing, sizeof(thing), 0,
        (struct sockaddr *)&their_addr, &addr_len)) == -1) {
        error("recvfrom");
    }

    char serverAddr[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &their_addr.sin_addr, serverAddr, INET_ADDRSTRLEN);

    *retPort = ntohl(thing.a);
    *retPlayPort = ntohl(thing.b);
    strcpy(retAddr, serverAddr);
}

void ClientSocket::sendMetadata(std::unordered_map<std::string, std::string> *metadata) {
    sendInt(metadata->size());
    for (auto it = metadata->begin(); it != metadata->end(); ++it) {
        sendString(it->first.c_str());
        sendString(it->second.c_str());
    }
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

void ClientSocket::sendString(const char *msg) {
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
