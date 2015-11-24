#include "NetworkController.h"

NetworkController::NetworkController(std::string protocolStr)
{
	int familyInt = SOCK_STREAM, protocolInt = IPPROTO_TCP;
	
	if(protocolStr.compare("udp") == 0){
		familyInt = SOCK_DGRAM;
		protocolInt = IPPROTO_UDP;
	}
	
	if (WSAStartup(MAKEWORD(2,2), &wsaData)!= 0)
	{
		// throw an error here
		std::cout << "WSAStartup failed!\n";
	}
	
	std::cout << "WSAStartup succeeded!\n";
	
	if((mySocket = socket(AF_INET, familyInt, protocolInt)) == SOCKET_ERROR)
	{
		// throw an error here.
		std::cout << "Socket failed!\n";
	}
	
	std::cout << "Socket succeeded!\n";
}

NetworkController::~NetworkController()
{
	closesocket(mySocket);
	WSACleanup();
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
	
	length = htonl(length);
	result = send(mySocket, (char *)&length, sizeof(length), 0);
	if( result == SOCKET_ERROR )
	{
		// throw an exception here.
		std::cout << "send failed!\n";
	}
	
	for (int i = 0; i < metadata.size(); ++i)
	{
		const char *tmp = (metadata[i]).c_str();
		length = htonl(strlen(tmp));
		
		result = send(mySocket, (char *)&length, sizeof(length), 0);
		if( result == SOCKET_ERROR )
		{
			// throw an exception here.
			std::cout << "send failed!\n";
		}
		
		result = send(mySocket, tmp, strlen(tmp), 0);
		if( result == SOCKET_ERROR )
		{
			// throw an exception here.
			std::cout << "send failed!\n";
		}
	}
	
    if (shutdown(mySocket, SD_SEND) == SOCKET_ERROR) {
		std::cout << "shutdown failed with error: " << WSAGetLastError() << "\n";
        closesocket(mySocket);
        WSACleanup();
    }
	
	do {
		result = recv(mySocket, recvbuf, recvbuflen, 0);
		if (result > 0){
			response.append(recvbuf);
			
			std::cout << recvbuf << " : " << result << "\n";
		}
		if (result  < 0){
			//throw an exception
			std::cout << "recv failed!" << result << "\n";
		}
	} while ( result > 0);
		
	return response;
}