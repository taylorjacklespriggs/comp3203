#include <iostream>

#include "DigiBoxClient.h"
#include "ClientSocket.h"

DigiBoxClient::DigiBoxClient(char *ipa, int p) : ipAddr(ipa), portNum(p) {
}

void DigiBoxClient::run() {
    std::cout << "Client Starting...\n";

    ClientSocket sock(ipAddr, portNum);

    sock.makeConnection(ipAddr, portNum);
}
