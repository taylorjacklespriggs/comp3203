#ifndef DIGIBOXCLIENT_H
#define DIGIBOXCLIENT_H

#include "MetadataController.h"

#include "ClientSocket.h"

class DigiBoxClient
{
    public:
        DigiBoxClient();
        ~DigiBoxClient();
        int run();
        std::unordered_map<std::string, std::string> setMetadata(std::string fileName);
        void connect();
        void playbackAction(std::string action);
    private:
        int playbackPort;
        char *serverAddr;
        int serverPort;
        std::string musicFile;
        std::unordered_map<std::string, std::string> metadata;
};

#endif

