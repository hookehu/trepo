#include "../kernel/hooke-client.h"

int main(int argc, char** args)
{
    char address[] = "127.0.0.1";
    struct event_base* base = event_base_new();
    Connect(base, address, 5678);
    event_base_dispatch(base);
}
