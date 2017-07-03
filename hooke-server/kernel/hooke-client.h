#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <event.h>

#include "channel.h"

using namespace core;

#define MAXLINE 4096
#define MEM_SIZE 1024

struct sock_ev
{
    struct event* read_ev;
    struct event* write_ev;
    char* read_buffer;
    char* write_buffer;
};

struct client_msg
{
    int length;
    char* buffer;
};

struct client
{
    struct sock_ev* ev;
    core::HookeChannel* channel;
};

void ClientClose(int sock);
void ReleaseCLient(struct sock_ev* ev);
void ClientOnWrite(int sock, short event, void* arg);
void ClientOnRead(int sock, short event, void* arg);
void Connect(struct event_base* base, char* addr, int port);
void ClientWrite(struct event_base*, int sock, char* msg, int length);
