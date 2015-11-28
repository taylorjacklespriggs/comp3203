#include "MetadataController.h"

MetadataController::MetadataController(std::string filename)
{
	file = new TagLib::FileRef(filename.c_str());
}

MetadataController::~MetadataController()
{
	delete file;
}

std::unordered_map<std::string, std::string> *MetadataController::getMetadata()
{
	if (file->isNull())
	{
		return NULL;
	}
	
	std::unordered_map<std::string, std::string> *metadata = new std::unordered_map<std::string, std::string>();
	
	std::string artist = file->tag()->artist().to8Bit();
	std::string album = file->tag()->album().to8Bit();
	std::string title = file->tag()->title().to8Bit();
	std::string genre = file->tag()->genre().to8Bit();
	std::string year = std::to_string(file->tag()->year());
	
	metadata->insert(std::make_pair(std::string("artist"), artist));
	metadata->insert(std::make_pair(std::string("album"), album));
	metadata->insert(std::make_pair(std::string("title"), title));
	metadata->insert(std::make_pair(std::string("genre"), genre));
	metadata->insert(std::make_pair(std::string("year"), year));
	
	return metadata;
}
