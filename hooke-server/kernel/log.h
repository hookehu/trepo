#ifndef HOOKE_LOG
#define HOOKE_LOG

#include <string.h>
#include <execinfo.h>
#include <timer.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>

enum LOG_LEVEL{DEBUG, WARING, INFO, ERROR, CRIT};

class Logger
{
    public:
        int fd;
        LOG_LEVEL logLevel = 0;//0为debug, 1为waring, 2为info, 3为error, 4为crit
        Logger();
        ~Logger();
        void SetFile(char** path)
        void SetLevel(LOG_LEVEL level);
        void Debug(char** log);
        void Waring(char** log);
        void Error(char** log);
        void Info(char** log);
        void Crit(char** log);
        void Save();

    private:
        char* GetStack();
};
#endif
