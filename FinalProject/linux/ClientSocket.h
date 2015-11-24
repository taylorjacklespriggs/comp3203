#ifndef CLIENTSOCKET_H
#define CLIENTSOCKET_H

#include <stdio.h>
#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

class ClientSocket
{
    public:
        ClientSocket();
        ~ClientSocket();
        void error(const char *msg);
        void makeConnection(char *ipAddr, int portNum);
        int serverBind();
        void serverListen();
        std::string sendMetadata(std::string thing);
        int sendInt(int msg);
        int sendString(char *msg);
        int recvInt();
        std::string recvString();

    private:
        int mySocket;
        int listenSocket;
};

#endif
