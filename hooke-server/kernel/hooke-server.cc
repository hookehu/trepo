#include <arpa/inet.h>
#include "hooke-server.h"
#include <pthread.h>
#include "../protocol/services.pb.h"

using namespace core;
using namespace foo::bar;

void Close()
{
}

void StopServer()
{
}

void OnReadlease(struct server** svr)
{
    //event_del(ev->read_ev);
    //event_del(ev->write_ev);
    //free(ev->read_ev);
    //free(ev->write_ev);
    //free(ev->buffer);
    //free(ev);
}

void Write(struct event_base* b, int sock, char* message, int length)
{
    printf("pre write %d\n", length);
    struct event* write_ev;
    struct msg* pkg;
    write_ev = (struct event*)malloc(sizeof(struct event));
    memset(write_ev, 0, sizeof(struct event));
    pkg = (struct msg*)malloc(sizeof(struct msg));
    memset(pkg, 0, sizeof(struct msg));
    pkg->length = length;
    pkg->buffer = message;
    event_set(write_ev, sock, EV_WRITE, OnWrite, pkg);
    int bs = event_base_set(b, write_ev);
    int rst = event_add(write_ev, NULL);
}

void OnWrite(int sock, short event, void* arg)
{
    msg* message = (msg*)arg;
    printf("cnt %s\n", message->buffer);
    send(sock, message->buffer, message->length, 0);
    printf("send %d\n", message->length);
}

void OnRead(int sock, short event, void* arg)
{
    printf("on read\n");
    int size;
    struct server* svr = (struct server*)arg;
    char* buffer = (char*)malloc(MEM_SIZE);
    bzero(buffer, MEM_SIZE);
    size = recv(sock, buffer, MEM_SIZE, 0);
    printf("receive data:%s, size:%d\n", buffer, size);
    if(size == 0)
    {
        OnRelease(svr);
        close(sock);
        printf("close\n");
        return;
    }
    if(svr->channels.count(sock) < 0)
    {
        printf("not the sock %d\n", sock);
    }
    FooReq req;
    req.set_id(12);
    svr->channels[sock]->stub->Bar(NULL, &req, NULL, NULL);
}

void OnAccept(int sock, short event, void* arg)
{
    struct sockaddr_in clt_addr;
    socklen_t sin_size;
    int newfd;
    struct server* svr = (struct server*)arg;
    struct sock_ev* ev = (struct sock_ev*)malloc(sizeof(struct sock_ev));
    ev->read_ev = (struct event*)malloc(sizeof(struct event));
    ev->write_ev = (struct event*)malloc(sizeof(struct event));
    sin_size = sizeof(struct sockaddr_in);
    newfd = accept(sock, (struct sockaddr*)&clt_addr, &sin_size);
    event_set(ev->read_ev, newfd, EV_READ|EV_PERSIST, OnRead, svr);
    event_base_set(svr->base, ev->read_ev);
    event_add(ev->read_ev, NULL);
    HookeChannel* ch = (HookeChannel*)GetChannel();
    ch->SetBase(svr->base);
    printf("accept sock %d\n", sock);
    HookeService* service = (HookeService*)new HookeService();
    HookeServiceStub* stub = (HookeServiceStub*)new HookeServiceStub(ch);
    ch->SetService(service);
    ch->SetStub(stub);
    svr->channels[newfd] = ch;
}

struct event_base* InitServer()
{
    struct event_base* base = event_base_new();
    return base;
}

struct server* GetServer(struct event_base* base, char* address, int port)
{
    struct server* svr = (struct server*)malloc(sizeof(struct server));
    svr->base = base;
    svr->address = address;
    svr->port = port;
    std::map<int, core::HookeChannel*> m;
    svr->channels = m;
    return svr;
}

void PreServer(struct server* svr)
{
    int listenfd;
    struct sockaddr_in seraddr, cltaddr;
    char buff[4096];
    int n, sin_size;
    int yes = 1;
    struct event listen_ev;
    
    if((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("create socket error\n");
        return;
    }
    svr->sock = listenfd;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));
    memset(&seraddr, 0, sizeof(seraddr));
    seraddr.sin_family = AF_INET;
    seraddr.sin_addr.s_addr = inet_addr(svr->address);
    seraddr.sin_port = htons(svr->port);

    if(bind(listenfd, (struct sockaddr*)&seraddr, sizeof(seraddr)) == -1)
    {
        printf("bind socket error port:%d\n", svr->port);
        return;
    }

    listen(listenfd, 1024);
    event_set(&listen_ev, listenfd, EV_READ|EV_PERSIST, OnAccept, svr);
    event_base_set(svr->base, &listen_ev);
    event_add(&listen_ev, NULL);
    printf("service... port %d\n", svr->port);
}

void StartServer(struct server* svr)
{
    int baseRst = event_base_dispatch(svr->base);
    printf("serving... end port: %d, base rst %d\n", svr->port, baseRst);
}
