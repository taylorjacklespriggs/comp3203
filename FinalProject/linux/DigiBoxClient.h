#ifndef DIGIBOXCLIENT_H
#define DIGIBOXCLIENT_H

class DigiBoxClient
{
    public:
        DigiBoxClient(char *ipa, int p);
        void run();
    private:
        char *ipAddr;
        int portNum;
};

#endif

