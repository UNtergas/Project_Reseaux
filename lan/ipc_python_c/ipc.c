#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/msg.h>
#include <string.h>

#define MAX_MSG_LEN 100
#define MSG_TYPE 1
#define KEY_FILE "msgfile"
#define KEY_CHAR 'a'

struct msg_buffer
{
    long mtype;
    char mtext[MAX_MSG_LEN];
};

int ipc()
{
    int msgid;
    struct msg_buffer msg;
    key_t key;

    // Créer la clé pour la file de message
    key = ftok(KEY_FILE, KEY_CHAR);

    // Obtenir l'ID de la file de message
    msgid = msgget(key, 0666 | IPC_CREAT);
    if (msgid == -1)
    {
        perror("Erreur lors de la création de la file de message");
        exit(EXIT_FAILURE);
    }

    // Processus receveur
    if (fork() == 0)
    {
        printf("Processus receveur\n");

        // Recevoir des messages jusqu'à ce que le message "exit" soit reçu
        while (1)
        {
            if (msgrcv(msgid, &msg, sizeof(msg), MSG_TYPE, 0) == -1)
            {
                perror("Erreur lors de la réception du message");
                exit(EXIT_FAILURE);
            }

            printf("Message reçu : %s\n", msg.mtext);

            if (strcmp(msg.mtext, "exit") == 0)
            {
                break;
            }
        }

        printf("Processus receveur terminé\n");
        exit(EXIT_SUCCESS);
    }

    // Processus émetteur
    printf("Processus émetteur\n");

    // Envoyer un message au processus receveur
    strcpy(msg.mtext, "Bonjour processus receveur !");
    msg.mtype = MSG_TYPE;
    if (msgsnd(msgid, &msg, sizeof(msg), 0) == -1)
    {
        perror("Erreur lors de l'envoi du message");
        exit(EXIT_FAILURE);
    }

    printf("Processus émetteur terminé\n");

    // Attendre que le processus receveur se termine
    wait(NULL);

    // Supprimer la file de message
    if (msgctl(msgid, IPC_RMID, NULL) == -1)
    {
        perror("Erreur lors de la suppression de la file de message");
        exit(EXIT_FAILURE);
    }

    return 0;
}

int main(int argc, char const *argv[])
{
    return ipc();
}
