#include "../kernel.h"

int main(int argc, char** argv)
{
    Logger* log = new Logger();
    log->SetFile("./log.txt")
    log->Save();
    printf("fffff");
    return 0;
}
