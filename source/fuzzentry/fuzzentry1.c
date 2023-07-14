#include <sys/socket.h> //connect,send,recv,setsockopt等
#include <sys/types.h>

#include <netinet/in.h> // sockaddr_in, “man 7 ip” ,htons
#include <poll.h> //poll,pollfd
#include <arpa/inet.h> //inet_addr,inet_aton
#include <unistd.h> //read,write
#include <netdb.h> //gethostbyname

#include <stdlib.h>//atoi
#include <assert.h>//assert

#include <error.h> //perror
#include <stdio.h>
#include <errno.h> //errno

#include <string.h> // memset

#define MAXLEN  0x10000

int main(int argc, char* argv[])
{
    int sockfd,n;
    struct sockaddr_in servaddr;
    int port;
    char recvline[MAXLEN] = {0};
    if(argc!=3)
    {
        puts("usage: fuzzenrty <IPaddress> <port>");
        exit(0);
    }
    if((sockfd = socket(AF_INET,SOCK_STREAM,0)) < 0)
    {
        puts("socker error");
        exit(0);
    }
    port = atoi(argv[2]);
    if(port<1)
    {
        puts("port error");
        exit(0);
    }
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(port);
    if(inet_pton(AF_INET, argv[1], &servaddr.sin_addr) <= 0)
    {
        printf("inet_pton error for %s", argv[1]);
        exit(0);
    }

    if(connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0)
    {
        puts("connect error");
        exit(0);
    }
    int len = read(STDIN_FILENO,recvline,0x10000);
    if(len<=0x10)
    {
        for(;len<=0x18;len++)
        {
            recvline[len-1] = '1';
        }
    }
    write(sockfd,recvline,len);
    usleep(10);
    close(sockfd);

    if((sockfd = socket(AF_INET,SOCK_STREAM,0)) < 0)
    {
        puts("socker error");
        exit(0);
    }
    int ret = connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
    if( ret < 0)
    {
        printf("crash!!!%d",ret);
        assert(0);
    }else{
        printf("not crash!!!%d",ret);
        close(sockfd);
    }

}