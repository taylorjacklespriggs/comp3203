#include <string>
#include <unordered_map>

#ifndef TAGLIB_STATIC
#define TAGLIB_STATIC
#endif

#include <taglib/fileref.h>
#include <taglib/tag.h>

class MetadataController 
{
public:
	MetadataController(std::string);
	~MetadataController();
	std::unordered_map<std::string, std::string> *getMetadata();
private:
	TagLib::FileRef *file;
};
