#include <iostream>

#include "DigiBoxClient.h"
#include "ClientSocket.h"

DigiBoxClient::DigiBoxClient(char *ipa, int p) : ipAddr(ipa), portNum(p) {
}

void DigiBoxClient::run() {
    std::cout << "Client Starting...\n";

    ClientSocket sock(ipAddr, portNum);

    sock.makeConnection(ipAddr, portNum);

    sock.sendInt(1);
    sock.sendString("Name");
    sock.sendString("The Duck Song");
    std::string reply = sock.recvString();

    std::cout << "Got this: " << reply << "\n";
}
