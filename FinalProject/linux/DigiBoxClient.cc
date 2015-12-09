#include <iostream>
#include <string.h>
#include <gtkmm/application.h>

#include "DigiBoxClient.h"
#include "ClientSocket.h"
#include "ClientGUI.h"

DigiBoxClient::DigiBoxClient() {
    serverAddr = new char[16];
    musicFile = "/home/paul/Desktop/201TheImperialMarch.mp3";
}

DigiBoxClient::~DigiBoxClient() {
    delete[] serverAddr;
}

int DigiBoxClient::run() {
    std::cout << "DigiBox client (Linux) now starting...\n";

    ClientSocket findSocket;
    findSocket.findServer(43110, serverAddr, &serverPort);
    std::cout << "DigiBox server found at " << serverAddr << ":" << serverPort << "\n";

    auto app = Gtk::Application::create();

    ClientGUI gui(this);
    return app->run(gui);
}

std::unordered_map<std::string, std::string> DigiBoxClient::setMetadata(std::string fileName) {
    musicFile = fileName;

    MetadataController metaCtrl(fileName);
    std::unordered_map<std::string, std::string> *m= metaCtrl.getMetadata();
    metadata = *m;
    delete m;
    return metadata;
}

void DigiBoxClient::connect() {
    // Open connection and send song metadata to server
    ClientSocket *metaSock = new ClientSocket();
    metaSock->makeConnection(serverAddr, serverPort);

    //MetadataController *metaCtrl = new MetadataController(musicFile);
    //std::unordered_map<std::string, std::string> *metadata = metaCtrl->getMetadata();
    metaSock->sendMetadata(&metadata);
    //delete(metaCtrl);

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
    streamSock.makeConnection(serverAddr, streamPort);

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
