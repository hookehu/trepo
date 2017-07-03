#include "channel.h"
#include <stdio.h>

namespace core
{
    HookeChannel::HookeChannel()
    {
        service = NULL; //service for other
        stub = NULL; //send to remote
        sock = -1;
    }

    HookeChannel::~HookeChannel()
    {
    }

    void HookeChannel::SetWriter(WriterCb w)
    {
        writer = w;
    }

    void HookeChannel::SetSock(int sock)
    {
        this->sock = sock;
    }

    void HookeChannel::SetService(HookeService* service)
    {
        this->service = service;
    }

    void HookeChannel::SetBase(struct event_base* base)
    {
        this->base = base;
    }

    void HookeChannel::SetStub(HookeServiceStub* stub)
    {
        this->stub = stub;
    }

    void PrintDebugArray(char* msg, int length)
    {
        ini i = 0;
        for (i = 0; i < length; i++)
        {
            printf("idx %d content %d\n", i, msg[i]);
        }
    }

    void HookeChannel::CallMethod(const MethodDescriptor* method, RpcController* controller, const Message* request, Message* response, Closure* done)
    {
        printf("jkkk %d\n", method->index());
        int mid = method->index();
        int indexLen = sizeof(int);
        int pkgLen = sizeof(int);
        int len = 0;
        mid = 13;
        string a;
        request->SerializeToString(&a);
        len = a.length() + indexLen + pkgLen;

        char* ch = (char*)malloc(sizeof(char)* len);
        memcpy(ch, &len, pkgLen);
        memcpy(ch + pkgLen, &mid, indexLen);
        memcpy(ch + pkgLen + indexLen, a.c_str(), a.length());

        PrintDebugArray(ch, len);
        printf("channel send len %d\n", len);
        writer(this->base, this->sock, ch, len);
    }

    void HookeChannel::CallMethod(string methodname, RpcController* controller)
    {
    }

    void HookeChannel::Receive(char* rcv)
    {
    }


    HookeService::HookeService()
    {
    }

    HookeService::~HookeService()
    {
    }

    void HookeService::CallMethod(int methodIdx)
    {
    }

    HookeServiceStub::HookeServiceStub(::google::protobuf::RpcChannel* channel):foo::bar::Foo_Stub(channel)
    {
    }

    HookeServiceStub::~HookeServiceStub()
    {
    }

    void HookeServiceStub::CallMethod(int methodIdx)
    {
    }

    void* GetChannel()
    {
        return new HookeChannel();
    }
}
