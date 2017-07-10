#include "../kernel/net.h"

int main(int argc, char** argv)
{
    char address[] = "127.0.0.1";
    int efd = InitServer();
    struct server* svr = GetServer(efd, address, 5678);
    StartServer(svr);
    printf("ffff");
    return 0;
}
