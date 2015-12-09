#include "DigiBoxClient.h"
#include "ui/ClientGUI.h"

DigiBoxClient::DigiBoxClient() 
{
    metadata = 0;
}

DigiBoxClient::~DigiBoxClient()
{
    delete metadata;
}

void DigiBoxClient::run()
{
    std::cout << "DigiBox client (Windows) is now starting..." << std::endl;

    NetworkController *broadcastClient = new NetworkController();
    broadcastClient->startBroadcastSocket(43110, &ip, &port);
    std::cout << "DigiBox server found at " << ip << ":" << port << std::endl; 

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

void DigiBoxClient::connect()
{
    NetworkController *metaClient = new NetworkController();
    metaClient->startTCPSocket();
		
	std::vector<std::string> metaDict;
	metaDict.push_back(std::string("title"));
	metaDict.push_back(metadata->at(std::string("title")));
	metaDict.push_back(std::string("artist"));
	metaDict.push_back(metadata->at(std::string("artist")));
	metaDict.push_back(std::string("album"));
	metaDict.push_back(metadata->at(std::string("album")));
	metaDict.push_back(std::string("genre"));
	metaDict.push_back(metadata->at(std::string("genre")));
	metaDict.push_back(std::string("year"));
	metaDict.push_back(metadata->at(std::string("year")));
	
	metaClient->makeConnnection(ip, port);
	std::string response = metaClient->sendMetadata(metaDict);

    if(response.compare("wait") != 0)
    {
        return;
    }

    NetworkController *queueServer = new NetworkController();
    int serverPort = queueServer->startQueueSocket();
    metaClient->sendInt(serverPort);
    delete(metaClient);

    int streamPort;		
	char token[128];
	queueServer->recvToken(&streamPort, token);

    delete(queueServer);

    NetworkController *streamSocket = new NetworkController();
	streamSocket->startTCPSocket();
	streamSocket->makeConnnection(ip, streamPort);
	streamSocket->initiateStream(token);
	response = streamSocket->recvString();

    if (response.compare("go") == 0)
    {
        streamSocket->sendFile(musicFile);
    }
}
