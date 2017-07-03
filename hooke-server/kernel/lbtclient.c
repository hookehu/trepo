#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include <event.h>

#define MAXLINE 4096
#define MEM_SIZE 1024

struct event_base* base;
struct sock_ev
{
    struct event* read_ev;
    struct event* write_ev;
    char* read_buffer;
    char* write_buffer;
};

void release_sock_event(struct sock_ev* ev)
{
    event_del(ev->read_ev);
    free(ev->read_ev);
    free(ev->write_ev);
    free(ev->read_buffer);
    free(ev->write_buffer);
    free(ev);
}

void on_write(int sock, short event, void* arg)
{
    struct sock_ev* ev = (struct sock_ev*)arg;
    char* buffer = ev->send_buffer;
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
    ev->send_buffer = sendline;
    event_add(ev->write_ev, NULL);
    printf("sended\n");
}

void on_read(int sock, short event, void* arg)
{
    struct event* write_ev;
    int size;
    if(arg == NULL)
    {
        printf("arg is null\n");
        return;
    }

    struct sock_ev* ev = (struct sock_ev*)arg;
    ev->read_buffer = (char*)malloc(MEM_SIZE);
    bzero(ev->read_buffer, MEM_SIZE);
    size = recv(sock, ev->read_buffer, MEM_SIZE, 0);
    printf("receive data:%s, size:%d\n", ev->read_buffer, size);
    if(size == 0)
    {
        release_sock_event(ev);
        close(sock);
        return;
    }
}

int main(int argc, char** argv)
{
    int sockfd;
    struct sockaddr_in seraddr;
    char recvline[4096];
    char* sendline = (char *)malloc(sizeof(char) * 4096);
    struct sock_ev* ev = (struct sock_ev*)malloc(sizeof(struct sock_ev));
    ev->read_ev = (struct event*)malloc(sizeof(struct event));
    ev->write_ev = (struct event*)malloc(sizeof(struct event));

    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        printf("create socket error");
        exit(0);
    }
    if((sockfd = socket(AF_INET, SOCK_STREA, 0)) < 0)
    {
        printf("create socket error\n");
        exit(0);
    }
    memset(&seraddr, 0, sizeof(seraddr));
    seraddr.sin_family = AF_INET;
    seraddr.sin_port = htons(5678);
    if(inet_pton(AF_INET, argv[1], &seraddr.sin_addr) <= 0)
    {
        printf("inet_pton error\n");
        exit(0);
    }

    if(connect(sockfd, (struct sockaddr*)&seraddr, sizeof(seraddr)) < 0)
    {
        printf("connect error\n");
        exit(0);
    }

    fgets(sendline, 4096, stdin);
    ev->send_buffer = sendline;
    base = event_base_new();
    event_set(ev->read_ev, sockfd, EV_READ|EV_PERSIST, on_read, ev);
    event_base_set(base, ev->read_ev);
    event_add(ev->read_ev, NULL);
    event_set(ev->write_ev, sockfd, EV_WRITE, on_write, ev);
    event_base_set(base, ev->write_ev);
    event_add(ev->write, NULL);
    event_base_dispatch(base);

    return 0;
}
