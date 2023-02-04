#include "TcpSocket.h"
#include <stdexcept>
#include <iostream>
#include <cstring>

using namespace std;

TcpSocket::TcpSocket(const char *port, const char *address) : port(port), address(address)
{
   sd = createClientTcpSocket(port, address);
   if (sd < 0)
   {
      throw runtime_error("Could not connect to TCP server at " + *address + ':' + *port);
   }
}

TcpSocket::TcpSocket(const char *port) : port(port), address(nullptr)
{
   // create server
}

int TcpSocket::createClientTcpSocket(const char *port, const char *server)
{
   // create server info structure
   struct addrinfo hints, *servInfo; // loaded with getaddrinfo()
   memset(&hints, 0, sizeof(hints)); // initialize memory in struct hints
   hints.ai_family = AF_UNSPEC;      // use IPv4 or IPv6
   hints.ai_socktype = SOCK_STREAM;  // use TCP
   hints.ai_flags = AI_PASSIVE;

   // call getaddrinfo() to update servInfo
   int error = getaddrinfo(server, port, &hints, &servInfo);
   if (error != 0)
   {
      cerr << "getaddrinfo() Error! " << error << endl;
      exit(1);
   }

   return createNewSocket(servInfo);
}

int TcpSocket::createNewSocket(addrinfo *servInfo)
{
   // make a socket, bind it, listen to it
   int clientSd = socket(servInfo->ai_family, servInfo->ai_socktype,
                         servInfo->ai_protocol);
   if (clientSd < 0)
   {
      cerr << "Socket creation error!" << errno << endl;

      return -1;
   }
   // lose pesky "Address already in use" error message
   int status = connect(clientSd, servInfo->ai_addr, servInfo->ai_addrlen);
   if (status < 0)
   {
      cerr << "Failed to connect to the server" << errno << endl;

      return -1;
   }

   return clientSd;
}

int TcpSocket::send(char *msg, int msgSize)
{
   int totalBytesSent = 0;
   while (totalBytesSent < msgSize)
   {
      int bytesSent = write(sd, (char *)msg, msgSize);
      if (bytesSent < 0)
      {
         cerr << "SEND ERROR" << errno << endl;
         return -1;
      }
      else
      {
         totalBytesSent += bytesSent;
      }
   }

   return 0;
}