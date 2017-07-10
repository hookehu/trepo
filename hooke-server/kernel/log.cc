#include "log.h"

Logger::Logger():logLevel(DEBUG)
{
    //this->logLevel = DEBUG;
}

Logger::~Logger()
{
    this->Save();    
}

void Logger::SetFile(char* path)
{
    this->fd = open(path, O_WRONLY|O_CREAT);
    if(this->fd == -1)
    {
        fprintf(stderr, "error %s\n", strerror(errno));
        exit(1);
    }
}

void Logger::SetLevel(LOG_LEVEL level)
{
    this->logLevel = level;
}

void Logger::Debug(char* log)
{
    if(this->logLevel != DEBUG)
    {
        return;
    }
    time_t rawtime;
    time(&rawtime);
    struct tm *timeinfo;
    timeinfo = localtime(&rawtime);
    std::string s(asctime(timeinfo));
    s[s.size() - 1] = ' ';
    s.append("[DEBUG] ");
    s.append(log);
    s.append("\n");
    write(this->fd, s.c_str(), s.size());
}

void Logger::Waring(char* log)
{
    if(this->logLevel == INFO || this->logLevel == ERROR || this->logLevel == CRIT)
    {
        return;
    }
    time_t rawtime;
    time(&rawtime);
    struct tm *timeinfo;
    timeinfo = localtime(&rawtime);
    std::string s(asctime(timeinfo));
    s[s.size() - 1] = ' ';
    s.append("[WARN] ");
    s.append(log);
    s.append("\n");
    write(this->fd, s.c_str(), s.size());
}

void Logger::Error(char* log)
{
    if(this->logLevel == CRIT)
    {
        return;
    }
    time_t rawtime;
    time(&rawtime);
    struct tm *timeinfo;
    timeinfo = localtime(&rawtime);
    std::string s(asctime(timeinfo));
    s[s.size() - 1] = ' ';
    s.append("[Error] ");
    s.append(log);
    s.append("\n");
    write(this->fd, s.c_str(), s.size());
}

void Logger::Info(char* log)
{
    if(this->logLevel == ERROR || this->logLevel == CRIT)
    {
        return;
    }
    time_t rawtime;
    time(&rawtime);
    struct tm *timeinfo;
    timeinfo = localtime(&rawtime);
    std::string s(asctime(timeinfo));
    s[s.size() - 1] = ' ';
    s.append("[INFO] ");
    s.append(log);
    s.append("\n");
    write(this->fd, s.c_str(), s.size());
}

void Logger::Crit(char* log)
{
    time_t rawtime;
    time(&rawtime);
    struct tm *timeinfo;
    timeinfo = localtime(&rawtime);
    std::string s(asctime(timeinfo));
    s[s.size() - 1] = ' ';
    s.append("[CRIT] ");
    s.append(log);
    s.append("\n");
    write(this->fd, s.c_str(), s.size());
}

void Logger::Save()
{
    if(this->fd == -1)
    {
        return;
    }
    close(fd);
}

char* Logger::GetStack()
{
}
