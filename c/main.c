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
    const char *command = "/usr/bin/python3 /home/debian/workspace/StationDePesage/python/uARM.py";
    int status;
    pid_t pid;
    char CAN_input;

    while (1) {
        pid = fork();

        is_factory_reset = getchar(); // Simulating factory reset.

        if (is_factory_reset == 'y') {
            while (1) {
                CAN_input = getchar(); // CAN input goes here.

                if (pid < 0) { // error
                    fputs("FORK ERROR!", stderr);
                    status = -1;
                } else if (pid == 0) { // child
                    signal(SIGHUP, cleanup);
                    signal(SIGINT, cleanup);
                    signal(SIGTERM, cleanup);
                    execl(SHELL, SHELL, "-c", command, NULL);
                    _exit(EXIT_FAILURE); // Fun fact: Avoids flushing fully-buffered streams like STDOUT.
                } else { // parent
                    if (CAN_input == 'k') {
                        break;
                    } else if (CAN_input == 'l') {
                        if (waitpid(pid, &status, 0) != pid) {
                            status = 1;
                        }
                    } else {
                        fputs("PROTOCOL ERROR!", stderr);
                    }
                }

                puts(status); // CAN output goes there.
            }
        } else {
            cleanup();
            break;
        }

        cleanup();
    }

    exit(EXIT_SUCCESS);
}

void cleanup(void) {
    puts("Termination signal received! (do some complex cleanup...)");
    fputs("Killing child!", stderr);
    kill(pid, SIGTERM);
    sleep(3);
    exit(0);
}
