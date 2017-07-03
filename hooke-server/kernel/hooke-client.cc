#include "hooke-client.h"

void ReleaseClient(struct sock_ev* ev)
{
    event_del(ev->read_ev);
    free(ev->read_ev);
    free(ev->write_ev);
    free(ev->read_buffer);
    free(ev->write_buffer);
    free(ev);
}

void ClientWrite(struct event_base* b, int sock, char* msg, int length)
{
    printf("pre write\n");
    struct event* write_ev;
    write_ev = (struct event*)malloc(sizeof(struct event));
    memset(write_ev, 0, sizeof(struct event));
    event_set(write_ev, sock, EV_WRITE, ClientOnWrite, msg);
    int bs = event_base_set(b, write_ev);
    int rst = event_add(write_ev, NULL);
}

void ClientOnWrite(int sock, short event, void* arg)
{
    struct sock_ev* ev = (struct sock_ev*)arg;
    char* buffer = ev->write_buffer;
    if(buffer == NULL)
    {
        printf("buffer is null\n");
        return;
    }

    send(sock, buffer, strlen(buffer), 0);
    if(buffer != NULL)
    {
        free(buffer);
    }
    char* sendline = (char *)malloc(sizeof(char) * 4096);
    fgets(sendline, 4096, stdin);
    ev->write_buffer = sendline;
    event_add(ev->write_ev, NULL);
    printf("sended\n");
}

void ClientOnRead(int sock, short event, void* arg)
{
    struct event* write_ev;
    int size;
    if(arg == NULL)
    {
        printf("arg is null\n");
        return;
    }

    struct client* clt = (struct client*) arg;
    struct sock_ev* ev = clt->ev;
    ev->read_buffer = (char*)malloc(MEM_SIZE);
    bzero(ev->read_buffer, MEM_SIZE);
    size = recv(sock, ev->read_buffer, MEM_SIZE, 0);
    printf("receive data:%s, size:%d\n", ev->read_buffer, size);
    HookeChannel* ch = clt->channel;
    ch->Receive(ev->read_buffer);
    if(size == 0)
    {
        ReleaseClient(ev);
        ClientClose(sock);
        return;
    }
}

void Connect(struct event_base* base, char* addr, int port)
{
    int sockfd;
    struct sockaddr_in seraddr;
    char recvline[4096];
    char* sendline = (char *)malloc(sizeof(char) * 4096);
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("create socket error");
        exit(0);
    }
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("create socket error\n");
        exit(0);
    }
    memset(&seraddr, 0, sizeof(seraddr));
    seraddr.sin_family = AF_INET;
    seraddr.sin_port = htons(port);
    if(inet_pton(AF_INET, addr, &seraddr.sin_addr) <= 0)
    {
        printf("inet_pton error\n");
        exit(0);
    }

    if(connect(sockfd, (struct sockaddr*)&seraddr, sizeof(seraddr)) < 0)
    {
        printf("connect error\n");
        exit(0);
    }
    struct sock_ev* ev = (struct sock_ev*)malloc(sizeof(struct sock_ev));
    struct client* clt = (struct client*)malloc(sizeof(struct client));
    HookeChannel* ch = (HookeChannel*)GetChannel();
    clt->ev = ev;
    clt->channel = ch;
    ev->read_ev = (struct event*)malloc(sizeof(struct event));
    ev->write_ev = (struct event*)malloc(sizeof(struct event));
    ch->SetWriter(&ClientWrite);
    ch->SetBase(base);
    ch->SetSock(sockfd);
    HookeService* service = (HookeService*)new HookeService();
    HookeServiceStub* stub = (HookeServiceStub*)new HookeServiceStub(ch);
    ch->SetService(service);
    ch->SetStub(stub);
    
    fgets(sendline, 4096, stdin);
    ev->write_buffer = sendline;
    event_set(ev->read_ev, sockfd, EV_READ|EV_PERSIST, ClientOnRead, clt);
    event_base_set(base, ev->read_ev);
    event_add(ev->read_ev, NULL);
    event_set(ev->write_ev, sockfd, EV_WRITE, ClientOnWrite, ev);
    event_base_set(base, ev->write_ev);
    event_add(ev->write_ev, NULL);
}

void ClientClose(int sock)
{
}
