#include <arpa/inet.h>
#include "net.h"
#include <pthread.h>
#include <sys/epoll.h>
#include "../protocol/services.pb.h"

using namespace core;
using namespace foo::bar;

void StopServer(struct server* svr)
{
    svr->runing = 0;
}

void OnRelease(struct server* svr)
{
}

void OnWrite(int sock, msg* message)
{
    printf("cnt %s\n", message->buffer);
    send(sock, message->buffer, message->length, 0);
    printf("send %d\n", message->length);
}

void OnRead(int sock, struct server* svr)
{
    printf("on read\n");
    int size;
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

void OnAccept(int sock, struct server* svr)
{
    struct sockaddr_in clt_addr;
    socklen_t sin_size;
    int newfd;
    sin_size = sizeof(struct sockaddr_in);
    newfd = accept(sock, (struct sockaddr*)&clt_addr, &sin_size);
    HookeChannel* ch = (HookeChannel*)GetChannel();
    ch->SetEpoll(svr->efd);
    ch->SetSock(sock);
    printf("accept sock %d\n", sock);
    HookeService* service = new HookeService();
    HookeServiceStub* stub = new HookeServiceStub(ch);
    ch->SetService(service);
    ch->SetStub(stub);
    svr->channels[newfd] = ch;
}

void Connect(struct client* clt, char* addr, int port)
{
	int sock;
	struct sockaddr_in svraddr;
	sock = socket(AF_INET, SOCK_STREAM, 0);
	memset(&svraddr, 0, sizeof(svraddr));
	svraddr.sin_family = AF_INET;
	svraddr.sin_port = htons(port);
        svraddr.sin_addr.s_addr = inet_addr(addr);
	connect(sock, (struct sockaddr*)&svraddr, sizeof(svraddr));
	clt->sock = sock;
	printf("connect %d\n", sock);
	HookeChannel* ch = new HookeChannel();
        ch->SetSock(sock);
	ch->SetEpoll(clt->efd);
	HookeService* service = new HookeService();
	HookeServiceStub* stub = new HookeServiceStub(ch);
	ch->SetService(service);
	ch->SetStub(stub);
	clt->channel = ch;
    	struct epoll_event ev;
        ev.data.ptr = ch;
    	//ev.data.fd = clt->sock;
    	ev.events = EPOLLIN | EPOLLET;
    	epoll_ctl(clt->efd, EPOLL_CTL_ADD, clt->sock, &ev);
	FooReq req;
	req.set_id(1);
        stub->Bar(NULL, &req, NULL, NULL);
}

int InitServer()
{
    int efd = epoll_create(256);
    return efd;
}

struct server* GetServer(int efd, char* address, int port)
{
    struct server* svr = (struct server*)malloc(sizeof(struct server));
    svr->efd = efd;
    svr->address = address;
    svr->port = port;
    std::map<int, core::HookeChannel*> m;
    svr->channels = m;

    int listenfd;
    struct sockaddr_in seraddr, cltaddr;
    char buff[4096];
    int n, sin_size;
    int yes = 1;
    
    if((listenfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("create socket error\n");
        return svr;
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
        return svr;
    }

    listen(listenfd, 1024);
    struct epoll_event ev;
    svr->runing = 1;
    ev.data.fd = svr->sock;
    ev.events = EPOLLIN | EPOLLET | EPOLLOUT;
    epoll_ctl(svr->efd, EPOLL_CTL_ADD, svr->sock, &ev);
    printf("servicekk`... port %d\n", svr->port);
    return svr;
}

void WaitNet(int efd)
{
    struct epoll_event ev, events[20];
    int nfds, readlen;
    int connfd, sockfd;
    struct sockaddr cltaddr;
    socklen_t cltlen;
    char line[1024];
    printf("wait net %d\n", efd);
    while(1)
    {
        nfds = epoll_wait(efd, events, 20, 1500);
        printf("epoll num %d\n", nfds);
        for(int i = 0; i < nfds; i++)
        {
            if(events[i].events & EPOLLIN)
            {
                printf("epoll in\n");
                HookeChannel* ch = (HookeChannel*)events[i].data.ptr;
                sockfd = ch->sock;
                readlen = read(sockfd, line, MAXLINE);
                if(readlen < 0)
                {
                    if(errno == ECONNRESET)
                    {
                        close(sockfd);
                        events[i].data.fd = -1;
			printf("read error\n");
                    }
                    else
		    {
			printf("read error\n");
                    }
                }
                else if(readlen == 0)
                {
                    close(sockfd);
                    events[i].data.fd = -1;
                    printf("realen 0\n");
                }
                printf("read content %s\n", line);
		ch->Receive(line, readlen);
		ev.data.ptr = ch;
                ev.events = EPOLLOUT | EPOLLET;
                epoll_ctl(efd, EPOLL_CTL_MOD, sockfd, &ev);
            }
            else if(events[i].events & EPOLLOUT)
            {
                printf("epoll out\n");
                HookeChannel* ch = (HookeChannel*)events[i].data.ptr;
                if(ch == NULL)
                {printf("nnnnnnn\n");}
                sockfd = ch->sock;
		ch->OnWrite();
                ev.data.ptr = ch;
                ev.events = EPOLLIN | EPOLLET;
                epoll_ctl(efd, EPOLL_CTL_MOD, sockfd, &ev);
            }
        }
    }
    printf("wait net end\n");
}

void StartServer(struct server* svr)
{
    struct epoll_event ev, events[20];
    int nfds, readlen;
    int connfd, sockfd;
    struct sockaddr cltaddr;
    socklen_t cltlen;
    char line[MAXLINE];
    while(svr->runing == 1)
    {
       nfds = epoll_wait(svr->efd, events, 20, 500);
        for(int i = 0; i < nfds; i++)
        {
            if(events[i].data.fd == svr->sock)
            {
                connfd = accept(svr->sock, &cltaddr, &cltlen);
                if(connfd < 0)
                {
                    printf("connfd < 0");
                    continue;
                }
		printf("accept\n");
		HookeChannel* ch = new HookeChannel();
        	ch->SetSock(connfd);
		ch->SetEpoll(svr->efd);
		HookeService* service = new HookeService();
		HookeServiceStub* stub = new HookeServiceStub(ch);
		ch->SetService(service);
		ch->SetStub(stub);
                ev.data.ptr = ch;
                ev.events = EPOLLIN | EPOLLET;
                epoll_ctl(svr->efd, EPOLL_CTL_ADD, connfd, &ev);
            }
            else if(events[i].events & EPOLLIN)
            {
                printf("epoll in\n");
                HookeChannel* ch = (HookeChannel*)events[i].data.ptr;
                sockfd = ch->sock;
                readlen = read(sockfd, line, MAXLINE);
                if(readlen < 0)
                {
                    if(errno == ECONNRESET)
                    {
                        close(sockfd);
                        events[i].data.ptr = NULL;
                    }
                    else
		    {
			printf("read error\n");
			events[i].events = EPOLLIN | EPOLLET;
			epoll_ctl(svr->efd, EPOLL_CTL_MOD, sockfd, &events[i]);
			continue;
                    }
                }
                else if(readlen == 0)
                {
                    close(sockfd);
                    events[i].data.ptr = NULL;
                }
                printf("read content %d %s\n", readlen, line);
		ch->Receive(line, readlen);;
                ev.data.ptr = ch;
                ev.events = EPOLLOUT | EPOLLET;
                epoll_ctl(svr->efd, EPOLL_CTL_MOD, sockfd, &ev);
            }
            else if(events[i].events & EPOLLOUT)
            {
                printf("epoll out\n");
                HookeChannel* ch = (HookeChannel*)events[i].data.ptr;
                if(ch == NULL)
                {printf("nnnnnnn\n");}
                sockfd = ch->sock;
		ch->OnWrite();
                ev.data.ptr = ch;
                ev.events = EPOLLIN | EPOLLET;
                epoll_ctl(svr->efd, EPOLL_CTL_MOD, sockfd, &ev);
                //OnWrite(sockfd, svr);
            }
        }
    }
    printf("serving... end port: %d\n", svr->port);
}
