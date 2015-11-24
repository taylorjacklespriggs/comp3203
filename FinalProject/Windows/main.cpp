#include <iostream>
#include <string>
#include <vector>

#include "metadata/MetadataController.h"
#include "network/NetworkController.h"

#define IP_LOCAL "192.168.56.101"
#define IP_EXTERNAL "192.168.43.52"
#define IP IP_LOCAL

int main (int argc, char* argv[])
{
	if (argc > 1)
	{
		std::string filename = std::string(argv[1]);
		
		MetadataController *metaCtrl = new MetadataController(filename);
		NetworkController *metaClient = new NetworkController();
		metaClient->startTCPSocket();
		
		std::unordered_map<std::string, std::string> *metadata = metaCtrl->getMetadata();
		
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
		
		metaClient->makeConnnection(IP, 3711);
		std::string test = metaClient->sendMetadata(metaDict);
		
		std::cout << "response: " << test << "\n";
		
		NetworkController *queueServer = new NetworkController();
		int serverPort = queueServer->startQueueSocket();
		metaClient->sendInt(serverPort);
		
		int response;		
		char token[128];
		queueServer->recvToken(&response, token);
		std::cout << "Server GOT: " << response << "\n" << "token : " << token;
		
		delete queueServer;
		
		NetworkController *streamSocket = new NetworkController();
		streamSocket->startTCPSocket();
		streamSocket->makeConnnection(IP, 3912);
		//Sleep(10000);
		streamSocket->initiateStream(token);
		test = streamSocket->recvString();
		
		std::cout << "The Server said: " << test;
		
		while(1);
		
		delete metadata;
		delete metaCtrl;
		delete metaClient;
	}
}
