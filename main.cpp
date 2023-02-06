#include "TcpSocket.h"
#include <iostream>

using namespace std;

int main()
{
   try
   {
      TcpSocket eeg("26783", "10.65.70.129");
      TcpSocket gizmo("26784", "10.65.70.129");
      cout << "connected";
      while (true)
      {
         sleep(1);
         eeg.send("0", 1);
         gizmo.send("0", 1);
      }
   }
   catch (runtime_error e)
   {
      e.what();
      exit(1);
   }
}