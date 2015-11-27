#include <iostream>
#include <cstdlib>

#include "DigiBoxClient.h"

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cout << "Not enough parameters.\n";
        std::cout << "USAGE: " << argv[0] << " <IP Address> <Port Number>\n";
        return 0;
    }

    DigiBoxClient *client = new DigiBoxClient(argv[1], strtol(argv[2], NULL, 0));
    client->run();

    delete client;

    return 0;
}
