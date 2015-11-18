#include <iostream>
#include <string>

#include "MetadataController.h"

int main (int argc, char* argv[])
{
	if (argc > 1)
	{
		std::string filename = std::string(argv[1]);
		
		MetadataController *metaCtrl = new MetadataController(filename);
		
		std::unordered_map<std::string, std::string> *metadata = metaCtrl->getMetadata();
		
		std::cout << "Title: " << metadata->at(std::string("title")) << "\n";
		std::cout << "Artist: " << metadata->at(std::string("artist")) << "\n";
		std::cout << "Album: " << metadata->at(std::string("album")) << "\n";
		std::cout << "Genre: " << metadata->at(std::string("genre")) << "\n";
		std::cout << "Year: " << metadata->at(std::string("year")) << "\n";
		
		delete metadata;
		delete metaCtrl;
	}
}
