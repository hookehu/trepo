#include "channel.h"
#include <stdio.h>
#include <arpa/inet.h>

namespace core
{
    HookeChannel::HookeChannel()
    {
	SECTION_LEN = 1024;
        service = NULL; //service for other
        stub = NULL; //send to remote
        sock = -1;
        efd = -1;
        sendbuffer = (char*)malloc(sizeof(char) * SECTION_LEN);
        recvbuffer = (char*)malloc(sizeof(char) * SECTION_LEN);
	curWriteBufferSize = SECTION_LEN;
	curRecvBufferSize = SECTION_LEN;
	writeBufferLen = 0;
	recvBufferLen = 0;
    }

    HookeChannel::~HookeChannel()
    {
    }

    void HookeChannel::SetSock(int sock)
    {
        this->sock = sock;
    }

    void HookeChannel::SetService(HookeService* service)
    {
        this->service = service;
    }

    void HookeChannel::SetEpoll(int efd)
    {
        this->efd = efd;
    }

    void HookeChannel::SetStub(HookeServiceStub* stub)
    {
        this->stub = stub;
    }

    void PrintDebugArray(char* msg, int length)
    {
        int i = 0;
        for (i = 0; i < length; i++)
        {
            printf("idx %d content %d\n", i, msg[i]);
        }
    }

    void HookeChannel::CallMethod(const MethodDescriptor* method, RpcController* controller, const Message* request, Message* response, Closure* done)
    {//pkg data send to server
        printf("jkkk %d\n", method->index());
        int mid = method->index();
        int indexLen = sizeof(int);
        int pkgLen = sizeof(int);
        int len = 0;
	int buffLen = 0;
        //mid = 13;
        string a;
        request->SerializeToString(&a);
        len = a.length() + indexLen + pkgLen;
	buffLen = len;

        char* ch = (char*)malloc(sizeof(char) * len);
	mid = htonl(mid);
	len = htonl(len);
	memcpy(ch, &len, pkgLen);
	memcpy(ch + pkgLen, &mid, indexLen);
	memcpy(ch + pkgLen + indexLen, a.c_str(), a.length());

        PrintDebugArray(ch, buffLen);
        printf("channel send len pkg len %d total len %d %d\n", pkgLen, len, a.length());
        //writer(this->svr, this->sock, ch, len);
        this->Write(ch, buffLen);
    }

    void HookeChannel::CallMethod(string methodname, RpcController* controller)
    {
    }

    void HookeChannel::Receive(char* rcv, int len)
    {
	int totalLen = recvBufferLen + len;
	if(totalLen > curRecvBufferSize)
	{
		curRecvBufferSize += SECTION_LEN;
		char* tmp = (char*)malloc(sizeof(char) * curRecvBufferSize);
		memcpy(tmp, this->recvbuffer, recvBufferLen);
		memcpy(tmp + recvBufferLen, rcv, len);
		char* recv = this->recvbuffer;
		this->recvbuffer = tmp;
		this->recvBufferLen += len;
		free(recv);
	}
	else
	{
		memcpy(this->recvbuffer + recvBufferLen, rcv, len);
		this->recvBufferLen += len;
	}
	this->OnRecv();
    }

    void HookeChannel::OnRecv()
    {
	int len = 0;
	PrintDebugArray(recvbuffer, 10);
	memcpy(&len, recvbuffer, 4);
	len = ntohl(len);
	printf("recv pkg len %d\n", len);	
	if(recvBufferLen < len)
	{
		return;
	}
	char* tmp = (char*)malloc(sizeof(char) * len);
	memcpy(tmp, recvbuffer, len);
	int leftLen = recvBufferLen - len;
	memmove(recvbuffer, recvbuffer + len, leftLen);
	recvBufferLen = leftLen;
	pkgs.push(tmp);
	RPC();
    }

    void HookeChannel::RPC()
    {
	if(pkgs.size() == 0)
	{
		return;
	}
	printf("rpc 1\n");
	char* tmp = pkgs.front();
	pkgs.pop();
	int index = 0;
	int len = 0;
	memcpy(&len, recvbuffer, 4);
	memcpy(&index, recvbuffer + 4, 4);
	len = ntohl(len);
	index = ntohl(index);
	printf("rpc 2\n");
	char* pp = (char*)malloc(sizeof(char) * (len - 8));
	memcpy(pp, recvbuffer + 8, len -8);
	printf("rpc service begin\n");
	const MethodDescriptor* method = this->service->GetDescriptor()->method(index);
	Message* req = this->service->GetRequestPrototype(method).New();
	const string content(pp);
	printf("rpc 3\n");
	req->ParseFromString(content);	
	printf("rpc 4\n");
	this->service->CallMethod(method, NULL, req, NULL, NULL);
	printf("service call mthod %d\n", index);
	free(tmp);
	free(pp);
    }

    void HookeChannel::Write(char* send, int len)
    {
	int totalLen = writeBufferLen + len;
	if(totalLen > curWriteBufferSize)
	{
		curWriteBufferSize += SECTION_LEN;
		char* tmp = (char*)malloc(sizeof(char) * curWriteBufferSize);
		memcpy(tmp, sendbuffer, writeBufferLen);
		memcpy(tmp + writeBufferLen, send, len);
		char* w = sendbuffer;
		sendbuffer = tmp;
		writeBufferLen += len;
		free(w);
	}
	else
	{
		memcpy(sendbuffer + writeBufferLen, send, len);	
		writeBufferLen += len;
	}
	printf("buffer len %d\n", this->writeBufferLen);
	PrintDebugArray(this->sendbuffer, this->writeBufferLen);
        struct epoll_event ev;
        ev.data.ptr = this;
        ev.events = EPOLLIN | EPOLLOUT | EPOLLET;
        epoll_ctl(this->efd, EPOLL_CTL_MOD, this->sock, &ev);
        printf("write epoll add %d sock %d\n", this->efd, this->sock);
    }

    void HookeChannel::OnWrite()
    {
	if(writeBufferLen > 0)
	{
		printf("begin write %d\n", writeBufferLen);
		write(sock, sendbuffer, writeBufferLen);
		writeBufferLen = 0;
		sendbuffer = NULL;
		printf("after write\n");
	}	
    }


    HookeService::HookeService()
    {
    }

    HookeService::~HookeService()
    {
    }

    void HookeService::Bar(::google::protobuf::RpcController* controller,
				const ::foo::bar::FooReq* request,
				::foo::bar::FooResp* response,
				::google::protobuf::Closure* done)
    {
       printf("call service bar\n"); 
    }

    HookeServiceStub::HookeServiceStub(::google::protobuf::RpcChannel* channel):foo::bar::Foo_Stub(channel)
    {
    }

    HookeServiceStub::~HookeServiceStub()
    {
    }

    void* GetChannel()
    {
        return new HookeChannel();
    }
}
