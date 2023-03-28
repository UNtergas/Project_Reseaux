#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

void *threadFunc(void *tid)
{
    long *myID = (long *)tid;
    printf("THIS IS THREAD %ld\n", *myID);
};

int main()
{
    // thread identifier
    pthread_t tid0;
    pthread_create(&tid0, NULL, threadFunc, (void *)&tid0);
    // wait for the threadFunc to be well executed before the main exit
    pthread_exit(NULL);
    return 0;
}