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
        std::string sendMetadata(std::string thing);
        void sendInt(int msg);
        void sendString(char *msg);
        int recvInt();
        std::string recvString();
        void recvToken(int* port, char *token);
        void sendToken(char *token);
        void sendFile(std::string fileName);

    private:
        int mySocket;
};

#endif
