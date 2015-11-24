#include <iostream>
#include <cstdlib>

#include "DigiBoxClient.h"

int main(int argc, char *argv[]) {
    std::cout << "Testy.\n";
    
    if (argc < 3) {
        std::cout << "Not enough parameters.\n";
        std::cout << "USAGE: " << argv[0] << " <IP Address> <Port Number>\n";
        return 0;
    }

    for (int i=0; i<argc; i++) std::cout << argv[i] << "\n";

    //DigiBoxClient *client = new DigiBoxClient(argv[1], boost::lexical_cast<int>(argv[2]));
                                                     //boost::lexical_cast<int>("12345");
    DigiBoxClient *client = new DigiBoxClient(argv[1], strtol(argv[2], NULL, 0));
    //boost::lexical_cast<int>("12345");
    //DigiBoxClient *client = new DigiBoxClient(argv[1], std::stoi(argv[2]));
    client->run();

    delete client;

    return 0;
}
