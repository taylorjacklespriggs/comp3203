#ifndef NETWORKCONTROLLER_H
#define NETWORKCONTROLLER_H


extern "C"{
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iphlpapi.h>
}

#include <string>
#include <vector>
#include <iostream>
#include <fstream>

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
	void startBroadcastSocket(int, std::string *, int *, int *);
	void initiateStream(char *);

	void sendInt(int);
	void sendString(std::string);
	void sendToken(char *);
	void sendBytes(char *, int);
	void sendFile(std::string);
	int recvInt();
	std::string recvString();
	void recvToken(int *,char *);
private:
	WSADATA wsaData;
	SOCKET mySocket;
    const char* inet_ntop(int, const void*, char*, int);
    inet_pton(int, const char *, void *);
};

#endif
