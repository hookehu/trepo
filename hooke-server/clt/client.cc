#include "../kernel/net.h"

int main(int argc, char** args)
{
    char address[] = "127.0.0.1";
    client clt;
    int efd = epoll_create(256);
    clt.efd = efd;
    Connect(&clt, address, 5678);
    WaitNet(efd);
    //Connect(base, address, 5678);
}
