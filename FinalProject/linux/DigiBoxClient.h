#ifndef DIGIBOXCLIENT_H
#define DIGIBOXCLIENT_H

class DigiBoxClient
{
    public:
        DigiBoxClient();
        ~DigiBoxClient();
        void run();
    private:
        char *serverAddr;
        int serverPort;
        std::string musicFile;
        void connect();
};

#endif

