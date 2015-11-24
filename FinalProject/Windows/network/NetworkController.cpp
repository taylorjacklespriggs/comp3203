#include "NetworkController.h"

NetworkController::NetworkController()
{	
	if (WSAStartup(MAKEWORD(2,2), &wsaData)!= 0)
	{
		// throw an error here
		std::cout << "WSAStartup failed!\n";
	}
}

NetworkController::~NetworkController()
{
	closesocket(mySocket);
	WSACleanup();
}

void NetworkController::startMetaSocket()
{
	if((mySocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) == SOCKET_ERROR)
	{
		// throw an error here.
		std::cout << "Socket failed!\n";
	}
}

void NetworkController::makeConnnection(std::string server, int port)
{
	struct sockaddr_in saServer;
	
	saServer.sin_family = AF_INET;
	saServer.sin_addr.s_addr = inet_addr(server.c_str());
	saServer.sin_port = htons(port);
	
	if (connect(mySocket, (SOCKADDR *)&saServer, sizeof(saServer)) == SOCKET_ERROR)
	{
		// throw an exception here.
		std::cout << "Connection failed!\n";
	}
}

std::string NetworkController::sendMetadata(std::vector<std::string> metadata)
{
	std::string response = "";
	int length = metadata.size()/2, recvbuflen = DEFAULT_BUFLEN, result, entries;
	
	sendInt(length);
	
	for (int i = 0; i < metadata.size(); ++i)
	{		
		sendString(metadata[i]);
	}
	
  /*   if (shutdown(mySocket, SD_SEND) == SOCKET_ERROR) {
		std::cout << "shutdown failed with error: " << WSAGetLastError() << "\n";
        closesocket(mySocket);
        WSACleanup();
    } */
	
	response = recvString();
	
	return response;
}

void NetworkController::sendInt(int msg)
{
	msg = htonl(msg);
	
	int result = send(mySocket, (char *)&msg, sizeof(msg), 0);
	if( result == SOCKET_ERROR )
	{
		// throw an exception here.
		std::cout << "send failed!\n";
	}
}

void NetworkController::sendString(std::string msg)
{
	const char *chararr = msg.c_str();
	int msgLen = (int)strlen(chararr);
	sendInt(msgLen);
	
	int result = send(mySocket, chararr, msgLen, 0);
	if( result == SOCKET_ERROR )
	{
		// throw an exception here.
		std::cout << "send failed!\n";
	}
}

int NetworkController::recvInt()
{
	int msg;
	recv(mySocket, (char *)&msg, 4, 0);
	return ntohl(msg);
}

std::string NetworkController::recvString()
{
	int len = recvInt();
	char msg[len];
	recv(mySocket, msg, len, 0);
	msg[len] = '\0';
	std::string msgStr(msg);
	return msgStr;
}

int NetworkController::startQueueSocket()
{
	if((mySocket = socket(AF_INET, SOCK_DGRAM, 0)) == SOCKET_ERROR)
	{
		// throw an error here.
		std::cout << "Socket failed!\n";
	}
	
	int port = 8888;
	struct sockaddr_in saServer;
	
	saServer.sin_family = AF_INET;
	saServer.sin_addr.s_addr = INADDR_ANY;
	saServer.sin_port = htons(port);
	
	if (bind(mySocket, (SOCKADDR *)&saServer, sizeof(saServer)) == SOCKET_ERROR)
	{
		// throw an exception here.
		std::cout << "Bind failed!\n";
	}
	
	return port;
}