#include <iostream>

#include "DigiBoxClient.h"
#include "ClientSocket.h"
#include "MetadataController.h"

DigiBoxClient::DigiBoxClient(char *ipa, int p) : ipAddr(ipa), portNum(p) {
}

void DigiBoxClient::run() {
    std::string musicFile = "/home/paul/Desktop/201TheImperialMarch.mp3";

    std::cout << "DigiBox Client (Linux) now starting...\n";

    // Open connection and send song metadata to server
    ClientSocket *metaSock = new ClientSocket();
    metaSock->makeConnection(ipAddr, portNum);

    MetadataController *metaCtrl = new MetadataController(musicFile);
    std::unordered_map<std::string, std::string> *metadata = metaCtrl->getMetadata();
    metaSock->sendMetadata(metadata);
    delete(metaCtrl);

    std::string reply = metaSock->recvString();
    if (reply.compare("wait") != 0) {
        std::cout << "Received error from server: " << reply << ". Aborting.\n";
        return;
    }

    // Setup and send UDP port
    ClientSocket *udpListener = new ClientSocket();
    int udpPort = udpListener->serverBind();
    std::cout << "Listening for stream port and token on UDP port " << udpPort << ".\n";
    metaSock->sendInt(udpPort);

    delete(metaSock); //metadata connection no longer needed

    // Get stream port and token from server
    int streamPort;
    char token[128];
    udpListener->recvToken(&streamPort, token);
    
    delete(udpListener); //udp connection no longer needed

    // Authenticate and stream file
    ClientSocket streamSock;
    streamSock.makeConnection(ipAddr, streamPort);

    streamSock.sendToken(token);
    std::string streamStatus = streamSock.recvString();
    if (streamStatus.compare("go") == 0) {
        std::cout << "Stream authentication successful.\n";
        streamSock.sendFile(musicFile);
        std::cout << "Streaming finished.\n";
    } else {
        std::cout << "Stream authentication failed: " << streamStatus << ". Aborting.\n";
    }
}
