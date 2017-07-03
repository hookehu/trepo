#include "../kernel/hooke-server.h"

int main(int argc, char** argv)
{
    char address[] = "127,0,0,1\0";
    struct event_base* base = InitServer();
    struct server* svr = GetServer(base, address, 5678);
    PreServer(svr);
    StartServer(svr);
    printf("ffff");
    return 0;
}
