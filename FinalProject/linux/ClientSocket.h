#ifndef CLIENTSOCKET_H
#define CLIENTSOCKET_H

#include <stdio.h>
#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <unordered_map>

class ClientSocket
{
    public:
        ClientSocket();
        ~ClientSocket();
        void error(const char *msg);
        void makeConnection(char *ipAddr, int portNum);
        int serverBind();
        void findServer(int port, char *retAddr, int *retPort, int *retPlayPort);
        void sendMetadata(std::unordered_map<std::string, std::string> *metadata);
        void sendInt(int msg);
        void sendString(const char *msg);
        int recvInt();
        std::string recvString();
        void recvToken(int* port, char *token);
        void sendToken(char *token);
        void sendFile(std::string fileName);

    private:
        int mySocket;
};

#endif
