#ifndef DIGIBOXCLIENT_H
#define DIGIBOXCLIENT_H

#include <iostream>
#include <string>
#include <vector>

#include "metadata/MetadataController.h"
#include "network/NetworkController.h"

class DigiBoxClient {
public:
    DigiBoxClient();
    ~DigiBoxClient();
    void run();
    std::unordered_map<std::string, std::string> setMetadata(std::string);
    void connect();
private:
    std::string ip;
    int serverPort;
    int playbackPort;
    std::unordered_map<std::string, std::string> *metadata;
    std::string musicFile;
};

#endif
