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
		NetworkController *netCtrl = new NetworkController("tcp");
		
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
		
		netCtrl->makeConnnection("192.168.1.104", 3711);
		std::string test = netCtrl->sendMetadata(metaDict);
		
		std::cout << "response: " << test << "\n";
		
		std::cout << "Title: " << metadata->at(std::string("title")) << "\n";
		std::cout << "Artist: " << metadata->at(std::string("artist")) << "\n";
		std::cout << "Album: " << metadata->at(std::string("album")) << "\n";
		std::cout << "Genre: " << metadata->at(std::string("genre")) << "\n";
		std::cout << "Year: " << metadata->at(std::string("year")) << "\n";
		
		delete metadata;
		delete metaCtrl;
	}
}
