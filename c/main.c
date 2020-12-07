// File:        c/main.c
// By:          Samuel Duclos
// For:         My team.
// Description: uARM and balance control in C for TSO_team.
//              - finish Python (see Python)
//              - translate from Python

#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SHELL "/bin/bash"

static pid_t return_value; // Modify for execl() in child.

static void cleanup(int signo) {
    fprintf(stderr, "Termination signal received (%d)! Cleaning up!\n", signo);
    fprintf(stderr, "Killing child!\n");
    kill(pid, SIGTERM);
    sleep(3);
}

int main(int argc, char *argv[]) {
    const char *command = "/usr/bin/python3 /home/debian/workspace/StationDePesage/python/uARM_payload.py";
    int pipefd[2], status;
    pid_t ppid = getpid(), pid;
    char CAN_input;
    bool is_breaking = false;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <string>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    if (pipe(pipefd) == -1) {
        fputs("PIPE ERROR!", stderr);
        exit(EXIT_FAILURE);
    }

    return_value = fork();
    pid = getpid();

    if (return_value == -1) { // error
        fputs("FORK ERROR!", stderr);
        status = -1;
        //exit(EXIT_FAILURE);

    } else if (!return_value) { // child
        if (signal(SIGTERM, cleanup) == SIG_ERR) {
            fputs("Error while setting SIGTERM signal handler!", stderr);
            return EXIT_FAILURE;
        }

        if (signal(SIGINT, cleanup) == SIG_ERR) {
            fputs("Error while setting SIGINT signal handler!", stderr);
            return EXIT_FAILURE;
        }

        if (signal(SIGHUP, cleanup) == SIG_ERR) {
            fputs("Error while setting SIGHUP signal handler!", stderr);
            return EXIT_FAILURE;
        }

        //execl(SHELL, SHELL, "-c", command, NULL);
        //_exit(EXIT_FAILURE); // Fun fact: Avoids flushing fully-buffered streams like STDOUT.

        close(pipefd[1]); // Close unused write end.
        while (read(pipefd[0], &buf, 1) > 0) {
            write(STDOUT_FILENO, &buf, 1);
        }

        write(STDOUT_FILENO, "\n", 1);
        close(pipefd[0]);
        _exit(EXIT_SUCCESS);

    } else { // parent
        close(pipefd[0]); // Close unused read end.
        write(pipefd[1], argv[1], strlen(argv[1]));

        while (1) {
            is_factory_reset = getchar(); // Simulating factory reset.

            if (is_factory_reset == 'y') {
                while (1) {
                    CAN_input = getchar(); // CAN input goes here.

                    if (CAN_input == 'k') is_breaking = true;
                    else if (CAN_input == 'l') {
                        puts("Parent continues normally, everyone is happy!");
                    } else {
                        fputs("PROTOCOL ERROR!", stderr);
                        is_breaking = true;
                    }

                    puts(status); // CAN output goes there.

                    if (is_breaking) break;
            } else break;
        }

        close(pipefd[1]); // Reader will see EOF.
        //if (waitpid(pid, &status, 0) != pid) {
        //   status = 1;
        //}
        wait(NULL); // Wait for child.
        exit(EXIT_SUCCESS);
    }

    if (raise(SIGINT)) {
        fputs("Error while raising SIGINT signal!", stderr);
        return EXIT_FAILURE;
    }

    exit(EXIT_SUCCESS);
}
