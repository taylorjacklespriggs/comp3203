#include <iostream>

#include "DigiBoxClient.h"
#include "ClientSocket.h"

DigiBoxClient::DigiBoxClient(char *ipa, int p) : ipAddr(ipa), portNum(p) {
}

void DigiBoxClient::run() {
    std::cout << "Client Starting...\n";

    ClientSocket metaSock;

    metaSock.makeConnection(ipAddr, portNum);

    metaSock.sendInt(1);
    metaSock.sendString("Name");
    metaSock.sendString("The Duck Song");
    std::string reply = metaSock.recvString();

    std::cout << "Got this: " << reply << "\n";

    ClientSocket udpServer;

    int port = udpServer.serverBind();

    std::cout << "UDP ON PORT: " << port << "\n";

    metaSock.sendInt(port);

    //int streamPort = udpServer.recvInt();
    //std::cout << "GOT THIS: " << streamPort << "\n";

    int streamPort;
    char token[128];
    udpServer.recvToken(&streamPort, token);
    //std::string got = udpServer.recvString();
    //std::cout << "GOT THIS: " << got << "\n";
    
    ClientSocket streamSock;
    streamSock.makeConnection(ipAddr, streamPort);

    streamSock.sendToken(token);

    std::string streamReply = streamSock.recvString();
    std::cout << "STREAM REPLY: " << streamReply << "\n";
}
