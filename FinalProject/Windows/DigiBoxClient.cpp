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
    broadcastClient->startBroadcastSocket(43110, &ip, &serverPort, &playbackPort);
    std::cout << "DigiBox server found at " << ip << ":" << serverPort << " Playback port: " << playbackPort << std::endl;

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
	
	metaClient->makeConnection(ip, serverPort);
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
	streamSocket->makeConnection(ip, streamPort);
	streamSocket->initiateStream(token);
	response = streamSocket->recvString();

    if (response.compare("go") == 0)
    {
        streamSocket->sendFile(musicFile);
    }
}

void DigiBoxClient::play()
{
    NetworkController sock;
    sock.startTCPSocket();
    sock.makeConnection(ip, playbackPort);
    sock.sendInt(3);
    sock.sendString("request");
    sock.sendString("playback");
    sock.sendString("action");
    sock.sendString("play");
    sock.sendString("password");
    sock.sendString("boxdigger");
    Sleep(5000);
}

void DigiBoxClient::pause() {
    NetworkController sock;
    sock.startTCPSocket();
    sock.makeConnection(ip, playbackPort);
    sock.sendInt(3);
    sock.sendString("request");
    sock.sendString("playback");
    sock.sendString("action");
    sock.sendString("pause");
    sock.sendString("password");
    sock.sendString("boxdigger");
    Sleep(5000); 
}
void DigiBoxClient::next() {
    NetworkController sock;
    sock.startTCPSocket();
    sock.makeConnection(ip, playbackPort);
    sock.sendInt(3);
    sock.sendString("request");
    sock.sendString("playback");
    sock.sendString("action");
    sock.sendString("next");
    sock.sendString("password");
    sock.sendString("boxdigger");
    Sleep(5000); //sleep a bit to prevent connection from breaking early
}

