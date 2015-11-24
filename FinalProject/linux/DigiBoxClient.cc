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

    udpServer.serverListen();

    int get = udpServer.recvInt();
    std::cout << "GOT THIS: " << get << "\n";
}
