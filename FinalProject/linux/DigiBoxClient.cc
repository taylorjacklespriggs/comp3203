#include <iostream>

#include "DigiBoxClient.h"
#include "ClientSocket.h"

DigiBoxClient::DigiBoxClient(char *ipa, int p) : ipAddr(ipa), portNum(p) {
}

void DigiBoxClient::run() {
    std::string musicFile = "/home/paul/Desktop/201TheImperialMarch.mp3";

    std::cout << "DigiBox Client (Linux) now starting...\n";

    // Send song metadata to server
    ClientSocket *metaSock = new ClientSocket();

    metaSock->makeConnection(ipAddr, portNum);

    metaSock->sendInt(1);
    metaSock->sendString("Name");
    metaSock->sendString("The Duck Song");
    std::string reply = metaSock->recvString();

    //if (reply.compare("wait") == 0) {

    //} else {

    //}

    // Setup and send UDP port
    ClientSocket udpListener;

    int udpPort = udpListener.serverBind();

    std::cout << "Listening for stream port and token on UDP port " << udpPort << ".\n";

    metaSock->sendInt(udpPort);

    delete(metaSock);

    // Get stream port and token from server
    int streamPort;
    char token[128];
    udpListener.recvToken(&streamPort, token);

    // Authenticate and stream file
    ClientSocket streamSock;
    streamSock.makeConnection(ipAddr, streamPort);

    streamSock.sendToken(token);

    std::string streamStatus = streamSock.recvString();

    if (streamStatus.compare("go") == 0) {
        std::cout << "Stream authentication successful.\n";
        streamSock.sendFile(musicFile);
    } else {
        std::cout << "Stream authentication failed.\n";
    }
}
