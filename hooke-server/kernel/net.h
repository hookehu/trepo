#ifndef HOOKE_SERVER_SERVER_H
#define HOOKE_SERVER_SERVER_H

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/epoll.h>
#include <map>

#include "channel.h"

#define MAXLINE 4096
#define MEM_SIZE 1024

using namespace core;

struct client
{
    int efd;
    int sock;
    core::HookeChannel* channel;
};

struct server
{
    int sock;
    char* address;
    int efd;
    int port;
    std::map<int, core::HookeChannel*> channels; //sock, channel pair
    int runing; //是否运行
};

struct msg
{
    int length;
    char* buffer;
};

int InitServer();
void Connect(struct client* clt, char* addr, int port);
struct server* GetServer(int efd, char* address, int port);
void WaitNet(int efd);
void StartServer(struct server* svr);
void StopServer(struct server* svr);
void Wirte(struct server* svr, int sock, char* args, int length);
void OnWrite(int sock, struct server* svr);//call when can write
void OnRead(int sock, struct server* svr);//call when can read
void OnAccept(int sock, struct server* svr);//call when accept
void OnRelease(struct server* svr);//call when release
#endif //HOOKE_SERVER_SERVER_H
