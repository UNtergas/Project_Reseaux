#include <stdio.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

// socket lib
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/select.h>
// threads lib
#include <pthread.h>

#define BUF_SIZE 1024
#define MAX 10
#define MESG_KEY 190234
#define PY_TO_C 2
#define C_TO_PY 3
#define False 0
#define True 1

#define PORT 8000
// structure for message queue
struct mesg_buffer
{
    long mesg_type;
    char mesg_text[100];
} message;

char *recv_from_python()
{
    // msgget creates a message queue
    // and returns identifier
    int msgid = msgget(MESG_KEY, 0666 | IPC_CREAT);
    message.mesg_type = PY_TO_C;

    // msgsnd to send message
    if (msgrcv(msgid, &message, sizeof(message), message.mesg_type, 0) == -1)
    {
        perror("Msgrcv failed");
    }
    // display the message
    char *buffer = (char *)calloc(BUF_SIZE, sizeof(char));
    bzero(buffer, BUF_SIZE);
    strncpy(buffer, message.mesg_text, sizeof(message.mesg_text));

    return buffer;
}
void send_to_python()
{
    int msgid = msgget(MESG_KEY, 0666 | IPC_CREAT);
    message.mesg_type = C_TO_PY;

    // msgsnd to send message
    if (msgsnd(msgid, &message, sizeof(message), 0) == -1)
    {
        perror("MsgSnd failed");
    }
}
void setup_connection(int *my_fd, struct sockaddr_in *address)
{
    if ((*my_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
    {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // create address structure for peer
    address->sin_family = AF_INET;
    address->sin_addr.s_addr = INADDR_ANY;
    address->sin_port = htons(PORT);

    printf("IP address is: %s\n", inet_ntoa(address->sin_addr));
    printf("port is: %d\n", (int)ntohs(address->sin_port));

    // bind address structure to peer
    if (bind(*my_fd, (struct sockaddr *)address, sizeof(*address)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // listen for the connection
    if (listen(*my_fd, 5) < 0)
    {
        perror("listen failed");
        exit(EXIT_FAILURE);
    }
}
void *send_to_peer()
{
    while (1)
    {
        // printf("\nstart read msg from python process\n");
        // char* hello = read_msg_from_python_process();
        // printf("\n%s\n", hello);
        char buffer__[2000] = {0};
        int PORT_to_send = PORT;

        int sock = 0, valread;
        struct sockaddr_in serv_addr;

        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        {
            perror("\nsocket creation error\n");
        }
        serv_addr.sin_addr.s_addr = INADDR_ANY;
        serv_addr.sin_port = htons(PORT_to_send);
        serv_addr.sin_family = AF_INET;

        if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
        {
            printf("\nconnection failed\n");
            exit(EXIT_FAILURE);
        }
        printf("\nconnect sucessfully, start reading msg from python process\n");
        char *buffer = recv_from_python();

        // sprintf(buffer__, "%s[PORT:%d] says: %s", name, PORT, buffer__);
        if (send(sock, buffer, strlen(buffer) + 1, 0) == -1)
        {
            perror("sending failure");
            exit(EXIT_FAILURE);
        }
        printf("\nmessage sent\n");
        close(sock);
    }
}
void *receive_from_peer(int server_fd)
{
    struct sockaddr_in address;
    int valread;
    char buffer[BUF_SIZE];
    bzero(buffer, BUF_SIZE);
    int addrlen = sizeof(address);
    fd_set current_sockets, ready_sockets;

    // Initialize my current set
    FD_ZERO(&current_sockets);
    FD_SET(server_fd, &current_sockets);
    int k = 0;
    while (1)
    {
        k++;
        ready_sockets = current_sockets;

        if (select(FD_SETSIZE, &ready_sockets, NULL, NULL, NULL) < 0)
        {
            perror("Error");
            exit(EXIT_FAILURE);
        }

        for (int i = 0; i < FD_SETSIZE; i++)
        {
            if (FD_ISSET(i, &ready_sockets))
            {

                if (i == server_fd)
                {
                    int client_socket;

                    if ((client_socket = accept(server_fd, (struct sockaddr *)&address,
                                                (socklen_t *)&addrlen)) < 0)
                    {
                        perror("accept");
                        exit(EXIT_FAILURE);
                    }
                    FD_SET(client_socket, &current_sockets);
                }
                else
                {
                    valread = recv(i, buffer, sizeof(buffer), 0);
                    printf("\nlen: %d, buff: %s\n", strlen(buffer), buffer);
                    // char buffer__[1024];
                    // printf("\nenter the coor: ");
                    // scanf("%s", buffer__);
                    send_to_python(buffer);
                    FD_CLR(i, &current_sockets);
                }
            }
        }

        if (k == (FD_SETSIZE * 2))
            break;
    }
}
int main()
{
    // char *buffer = (char *)calloc(BUF_SIZE, sizeof(char));
    // bzero(buffer, BUF_SIZE);
    // while (True)
    // {
    //     buffer = recv_from_python();
    //     printf("Data send is : %s \n", message.mesg_text);
    // }
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    config_peer(&server_fd, &address);

    // Each thread has its identifier.
    pthread_t t1;
    pthread_t t2;

    pthread_create(&t1, NULL, send_to_peer, NULL);
    pthread_create(&t2, NULL, receive_from_peer, &server_fd);

    pthread_join(t2, NULL);
    pthread_join(t1, NULL);

    return 0;
}