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
#include <map>

extern "C"{
#include <event.h>
}

#include "channel.h"

#define MAXLINE 4096
#define MEM_SIZE 1024

using namespace core;

struct sock_ev
{
    struct event* read_ev;
    struct event* write_ev;
    char* buffer;
};

struct server
{
    int sock;
    char* address;
    int port;
    struct event_base* base;
    std::map<int, core::HookeChannel*> channels; //sock, channel pair
};

struct msg
{
    int length;
    char* buffer;
};

struct event_base* InitServer();
struct server* GetServer(struct event_base*, char* address, int port);
void PreServer(struct server* svr);
void StartServer(struct server* svr);
void Close();
void StopServer();
void Wirte(struct event_base*, int sock, char* args, int length);
void OnWrite(int sock, short event, void* arg);
void OnRead(int sock, short event, void* arg);
void OnAccept(int sock, short event, void* arg);
void OnRelease(struct server* svr);
#endif //HOOKE_SERVER_SERVER_H
