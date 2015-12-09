#include "DigiBoxClient.h"
#include "ui/ClientGUI.h"

DigiBoxClient::DigiBoxClient() 
{

}

DigiBoxClient::~DigiBoxClient()
{
}

void DigiBoxClient::run()
{
    std::cout << "DigiBox client (Windows) is now starting..." << std::endl;

    NetworkController *broadcastClient = new NetworkController();
    int metadataPort;
    broadcastClient->startBroadcastSocket(43110, &ip, &metadataPort);
    std::cout << "DigiBox server found at " << ip << ":" << metadataPort << std::endl; 

    auto app = Gtk::Application::create();
    ClientGUI gui(this);
    app->run(gui);
}

std::unordered_map<std::string, std::string> DigiBoxClient::setMetadata(std::string filename)
{
    musicFile = filename;

    MetadataController metadataController(musicFile);
    metadata = metadataController.getMetadata();
    return *metadata;
}
