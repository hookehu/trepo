#ifndef HOOKE_SERVER_CHANNEL_HA
#define HOOKE_SERVER_CHANNEL_HA

#include <queue>
#include <string.h>
#include <sys/epoll.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/service.h>
#include "../protocol/services.pb.h"

using namespace google::protobuf;

typedef void (*WriterCb)(struct server*, int, char*, int);

namespace core
{
    class HookeChannel;
    class HookeService;
    class HookeServiceStub;

    class HookeChannel: public ::google::protobuf::RpcChannel
    {
        public:
        HookeService* service;
        HookeServiceStub* stub;
        int sock;
        int efd;
        char* sendbuffer;//发送的缓冲区
        char* recvbuffer;//接收的缓冲区
        int writeBufferLen;//发送缓冲区长度
	int recvBufferLen;//接收缓冲区长度
        int SECTION_LEN;//基础缓冲区长度，用于自动扩展发送缓冲区／接收缓冲区大小
	int curWriteBufferSize;
	int curRecvBufferSize;
	std::queue<char*> pkgs;

        public:
            HookeChannel();
            ~HookeChannel();
            virtual void SetSock(int);
            virtual void SetEpoll(int efd);
            virtual void SetService(HookeService*);
            virtual void SetStub(HookeServiceStub*);
            virtual void CallMethod(const MethodDescriptor* method, RpcController* controller, const Message* request, Message* response, Closure* done);
            void CallMethod(string methodname, RpcController* controller);
            virtual void Receive(char* rcv, int len);
            virtual void OnRecv();
	    virtual void RPC();
            virtual void Write(char* send, int len);
	    virtual void OnWrite();
    };

    class HookeService: public ::foo::bar::Foo
    {
        public:
            HookeService();
            ~HookeService();
            void Bar(::google::protobuf::RpcController* controller,
			const ::foo::bar::FooReq* request,
			::foo::bar::FooResp* response,
			::google::protobuf::Closure* done);

        private:
    };

    class HookeServiceStub:public ::foo::bar::Foo_Stub
    {
        public:
            HookeServiceStub(::google::protobuf::RpcChannel* channel);
            ~HookeServiceStub();

        private:
    };

    void* GetChannel();
    void PrintDebugArray(char*, int);
};
#endif //HOOKE_SERVER_CHANNEL_H
