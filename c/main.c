# File:        c/main.c
# By:          Samuel Duclos
# For:         My team.
# Description: uARM and balance control in C for TSO_team.
# TODO:        - parallelize processes
#              - implement missing functionality
#              - translate from Python

#include <signal.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define SHELL "/bin/bash"

void cleanup(void);

int main(int argc, char *argv[]) {
    const char *command = "/usr/bin/python3 /home/debian/workspace/StationDePesage/python/uARM.py"
    int status;
    pid_t pid;
    char CAN_input;

    pid = fork();

    while (1) {
        while (1) {
            CAN_input = getchar(); // CAN input goes here.

            switch (pid) {
                case -1: // error
                    fputs("FORK ERROR!", stderr);
                        status = -1;
                        break;
                case 0: // child
                    signal(SIGHUP, cleanup);
                    signal(SIGINT, cleanup);
                    signal(SIGTERM, cleanup);
                    execl(SHELL, SHELL, "-c", command, NULL);
                    _exit(EXIT_FAILURE); // Avoid flushing fully-buffered streams such as STDOUT.
                    break;
                default: // parent
                    switch (CAN_input) {
                        case 'k':
                            fputs("Killing child!", stderr);
                            kill(pid, SIGTERM);
                            sleep(3);
                            break;
                        case 'l':
                            if (waitpid(pid, &status, 0) != pid) {
                                status = 1;
                            }
                            break;
                        default:
                            fputs("PROTOCOL ERROR!", stderr)
                            break;
                    }

                    break;

            printf("%d", status); // CAN output goes there.
        }
    }
}

void cleanup(void) {
    puts("Termination signal received! (do some complex cleanup...)");
    exit(0);
}