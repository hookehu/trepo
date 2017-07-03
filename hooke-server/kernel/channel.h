#ifndef HOOKE_SERVER_CHANNEL_HA
#define HOOKE_SERVER_CHANNEL_HA

#include <string.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/service.h>
#include "../protocol/services.pb.h"

extern "C"{
#include <event.h>
}

using namespace google::protobuf;

typedef void (*WriterCb)(struct event_base*, int, char*, int);

namespace core
{
    class HookeChannel;
    class HookeService;
    class HookeServiceStub;

    class HookeChannel: public ::google::protobuf::RpcChannel
    {
        public:
        WriterCb writer;
        HookeService* service;
        HookeServiceStub* stub;
        int sock;
        struct event_base* base;

        public:
            HookeChannel();
            ~HookeChannel();
            virtual void SetWriter(WriterCb);
            virtual void SetSock(int);
            virtual void SetBase(struct event_base*);
            virtual void SetService(HookeService*);
            virtual void SetStub(HookeServiceStub*);
            virtual void CallMethod(const MethodDescriptor* method, RpcController* controller, const Message* request, Message* response, Closure* done);
            void CallMethod(string methodname, RpcController* controller);
            virtual void Receive(char* rcv);
    };

    class HookeService: public ::foo::bar::Foo
    {
        public:
            HookeService();
            ~HookeService();
            void CallMethod(int methodIdx);

        private:
    };

    class HookeServiceStub:public ::foo::bar::Foo_Stub
    {
        public:
            HookeServiceStub(::google::protobuf::RpcChannel* channel);
            ~HookeServiceStub();
            void CallMethod(int methodIdx);

        private:
    };

    void* GetChannel();
};
#endif //HOOKE_SERVER_CHANNEL_H
