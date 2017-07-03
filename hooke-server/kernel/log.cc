#include "log.h"

Logger::Logger()
{
}

Logger::~Logger()
{
}

void Logger::SetFile(char** path)
{
    fd = open(path, O_WRONLY|O_CREAT);
    if(fd == -1)
    {
        fprintf(stderr, "error %s\n", strerror(errno));
        exit(1);
    }
}

void Logger::SetLevel(LOG_LEVEL level)
{
    this->logLevel = level;
}

void Logger::Debug(char** log)
{
}

void Logger::Waring(char** log)
{
}

void Logger::Error(char** log)
{
}

void Logger::Info(char** log)
{
}

void Logger::Crit(char** log)
{
}

void Save()
{
    if(this->fd == -1)
    {
        return;
    }
    close(this->fd);
}

char* GetStack()
{
}
