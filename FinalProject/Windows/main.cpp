#include <iostream>
#include <string>
#include <vector>

#include "metadata/MetadataController.h"
#include "network/NetworkController.h"

int main (int argc, char* argv[])
{
	if (argc > 1)
	{
		std::string filename = std::string(argv[1]);
		
		MetadataController *metaCtrl = new MetadataController(filename);
		NetworkController *metaClient = new NetworkController();
		metaClient->startMetaSocket();
		
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
		
		metaClient->makeConnnection("192.168.56.101", 3711);
		std::string test = metaClient->sendMetadata(metaDict);
		
		std::cout << "response: " << test << "\n";
		
		NetworkController *queueServer = new NetworkController();
		int serverPort = queueServer->startQueueSocket();
		metaClient->sendInt(serverPort);
		
		int response = queueServer->recvInt();
		
		std::cout << "Server GOT: " << response;
		
		while(1);
		
		delete metadata;
		delete metaCtrl;
		delete metaClient;
	}
}
