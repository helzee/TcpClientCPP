#ifndef TCPSOCKET_H
#define TCPSOCKET_H

using namespace std;

#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/types.h> // for sockets
#include <unistd.h>

class TcpSocket
{
public:
   TcpSocket(const char *port);
   TcpSocket(const char *port, const char *address);

   int send(char *msg, int msgSize);

private:
   const int MAX_REQUESTS = 20;
   const char *port;
   const char *address;
   int sd;

   int createTcpSocket(const char *port, const char *server);
   int createNewSocket(addrinfo *servInfo);
};

#endif