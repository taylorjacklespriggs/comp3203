extern "C"{
#include <winsock2.h>	
#include <windows.h>
}

#include <string>
#include <vector>
#include <iostream>

#define DEFAULT_BUFLEN 512

class NetworkController
{
public:
	NetworkController();
	~NetworkController();
	void makeConnnection(std::string, int);
	std::string sendMetadata(std::vector<std::string>);
	int startQueueSocket();
	void startTCPSocket();
	void initiateStream(char *);
	
	void sendInt(int);
	void sendString(std::string);
	void sendToken(char *);
	int recvInt();
	std::string recvString();
	void recvToken(int *,char *);
private:
	WSADATA wsaData;
	SOCKET mySocket;
};