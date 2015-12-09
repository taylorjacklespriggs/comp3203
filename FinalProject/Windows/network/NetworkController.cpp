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

void NetworkController::startTCPSocket()
{
	if((mySocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) == SOCKET_ERROR)
	{
		// throw an error here.
		std::cout << "Socket failed!\n";
	}
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

void NetworkController::startBroadcastSocket(int broadcastingPort,
                                             std::string *retAddr,
                                             int *retPort)
{
	if((mySocket = socket(AF_INET, SOCK_DGRAM, 0)) == SOCKET_ERROR)
	{
		std::cout << "Socket failed";
	}

	static int so_broadcast = TRUE;
	if(setsockopt(mySocket, SOL_SOCKET, SO_BROADCAST, (char *)&so_broadcast, sizeof(so_broadcast)) == SOCKET_ERROR)
	{
		std::cout << "Set Broadcast Failed.";
	}

	struct sockaddr_in saServer;

    PIP_ADAPTER_INFO pAdapterInfo;
    PIP_ADAPTER_INFO pAdapter;
    unsigned long ulOutBufLen = sizeof(IP_ADAPTER_INFO);
    pAdapterInfo = (IP_ADAPTER_INFO *) malloc(sizeof(IP_ADAPTER_INFO));

    if(GetAdaptersInfo(pAdapterInfo, &ulOutBufLen) 
      == ERROR_BUFFER_OVERFLOW){
        free(pAdapterInfo);
        pAdapterInfo = (IP_ADAPTER_INFO *) malloc(ulOutBufLen);
    }

    DWORD dwRetVal = 0;

    if ((dwRetVal = GetAdaptersInfo(pAdapterInfo, &ulOutBufLen)) 
        == NO_ERROR) {
        pAdapter = pAdapterInfo;
        while (pAdapter) {

            char *ipAddr = pAdapter->IpAddressList.IpAddress.String;
            char *subnet = pAdapter->IpAddressList.IpMask.String;
            struct in_addr host, mask;
            inet_pton(AF_INET, ipAddr, &host);
            inet_pton(AF_INET, subnet, &mask);

	        saServer.sin_family = AF_INET;
	        saServer.sin_addr.s_addr = host.s_addr | (~mask.s_addr);
	        saServer.sin_port = htons(broadcastingPort);

            int x = 0;
            if (sendto(mySocket, (char *) &x, sizeof(x), 0, 
                (sockaddr *)&saServer, sizeof(saServer)) == SOCKET_ERROR)
            {
                std::cout << "sendto failed on the broadcasting socket";
            }
            pAdapter = pAdapter->Next;
        }
    }

    if (pAdapterInfo){
        free(pAdapterInfo);
    }

    int numbytes;
    struct sockaddr_in their_addr;
    int buf = 0;
    int addr_len = sizeof(their_addr);
    numbytes = recvfrom(mySocket, (char *)&buf, 4, 0, 
               (struct sockaddr *)&their_addr, &addr_len);

    int serverPort = ntohl(buf);
    char serverAddr[16];
    inet_ntop(AF_INET, &their_addr.sin_addr, serverAddr, 16);

    *retPort = serverPort;
    *retAddr = std::string(serverAddr);    
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
	int length = metadata.size()/2;

	sendInt(length);

	for (int i = 0; i < metadata.size(); ++i)
	{
		sendString(metadata[i]);
	}

	response = recvString();

	return response;
}

void NetworkController::initiateStream(char *token)
{
	sendToken(token);
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

void NetworkController::sendToken(char *token)
{
	int result = send(mySocket, token, 128, 0);
	if( result == SOCKET_ERROR )
	{
		// throw an exception here.
		std::cout << "send failed!\n" << WSAGetLastError();
	}
}

void NetworkController::sendBytes(char *data, int size)
{
	sendInt(size);
	int result = send(mySocket, data, DEFAULT_BUFLEN, 0);
	if( result == SOCKET_ERROR )
	{
		// throw an exception here.
		std::cout << "send failed!\n" << WSAGetLastError();
	}
}

void NetworkController::sendFile(std::string filename)
{
	std::ifstream inFile;
	size_t size = 0;
	inFile.open(filename.c_str(), std::ios::in|std::ios::binary|std::ios::ate);

	if (inFile.is_open())
	{
		char *data = 0;
		inFile.seekg(0, std::ios::beg);
		while (!inFile.eof()){
			char *oldData = data;
			data = new char[DEFAULT_BUFLEN]();
			delete oldData;
			inFile.read(data, DEFAULT_BUFLEN);
			sendBytes(data, inFile.gcount());
		}

		delete data;
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

void NetworkController::recvToken(int *port, char *token)
{
	char msg[132];
	recv(mySocket, (char *)msg, 132, 0);
	*port = ntohl(*(int*)(void*)msg);
	memcpy(token, msg+4, 128);
}

const char* NetworkController::inet_ntop(int af, const void* src, char* dst,
                                         int cnt){
 
    struct sockaddr_in srcaddr;
 
    memset(&srcaddr, 0, sizeof(struct sockaddr_in));
    memcpy(&(srcaddr.sin_addr), src, sizeof(srcaddr.sin_addr));
 
    srcaddr.sin_family = af;
    if (WSAAddressToString((struct sockaddr*) &srcaddr, sizeof(struct sockaddr_in), 0, dst, (LPDWORD) &cnt) != 0) {
        DWORD rv = WSAGetLastError();
        std::cout << "WSAAddressToString() : %d\n",rv;
        return NULL;
    }
    return dst;
}

int NetworkController::inet_pton(int af, const char *src, void *dst)
{
  struct sockaddr_storage ss;
  int size = sizeof(ss);
  char src_copy[INET6_ADDRSTRLEN+1];

  ZeroMemory(&ss, sizeof(ss));
  /* stupid non-const API */
  strncpy (src_copy, src, INET6_ADDRSTRLEN+1);
  src_copy[INET6_ADDRSTRLEN] = 0;

  if (WSAStringToAddress(src_copy, af, NULL, (struct sockaddr *)&ss, &size) == 0) {
    switch(af) {
      case AF_INET:
    *(struct in_addr *)dst = ((struct sockaddr_in *)&ss)->sin_addr;
    return 1;
      case AF_INET6:
    *(struct in6_addr *)dst = ((struct sockaddr_in6 *)&ss)->sin6_addr;
    return 1;
    }
  }
  return 0;
}
