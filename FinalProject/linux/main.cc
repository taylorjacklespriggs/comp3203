#include <iostream>
#include <cstdlib>

#include "DigiBoxClient.h"

int main(int argc, char *argv[]) {
    DigiBoxClient *client = new DigiBoxClient();
    client->run();

    delete client;

    return 0;
}
