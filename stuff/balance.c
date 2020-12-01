// serial_write.c
#include <stdio.h>
#include <string.h>
#include <fcntl.h>   /* File Control Definitions           */
#include <termios.h> /* POSIX Terminal Control Definitions */
#include <unistd.h>  /* UNIX Standard Definitions          */
#include <errno.h>   /* ERROR Number Definitions           */

#define BUFFER_SIZE(buffer) (sizeof(buffer) / sizeof(buffer[0]))

int serial_write(int, char *);
int serial_read(int, char *);
void print_buffer(char *);
int balance_write(int, char *);
int balance_read(int);

int main(void) {
        struct termios SerialPortSettings;
        int fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_SYNC);

        if (fd < 0) printf("Error! Could not open ttyUSB0!\n");

        tcgetattr(fd, &SerialPortSettings);                           // Get the current attributes of the Serial port.

        cfmakeraw(&SerialPortSettings);

        cfsetspeed(&SerialPortSettings, B9600);                       // Set Speed at 9600 bauds.

        SerialPortSettings.c_iflag |= (ICANON | ECHO | ECHOE | ISIG); // Non Canonical mode.
        SerialPortSettings.c_oflag |= (ICANON | ECHO | ECHOE | ISIG); // Non Canonical mode.

        if ((tcsetattr(fd, TCSANOW, &SerialPortSettings)) < 0) printf("ERROR! Could not set attributes!\n");

        tcflush(fd, TCIFLUSH);                                        // Discards old data in the rx buffer.

        (void)balance_write(fd, "T");
        (void)balance_write(fd, "Z");
        (void)balance_read(fd);
        (void)balance_write(fd, "T13.37");
        (void)balance_read(fd);

        close(fd);

        return 0;
}

int serial_write(int fd, char *buffer) {return write(fd, buffer, BUFFER_SIZE(buffer));}

int serial_read(int fd, char *buffer) {return read(fd, buffer, 32);}

void print_buffer(char *buffer) {puts(buffer);}

int balance_write(int fd, char *buffer) {
        char new_buffer[32];
        int bytes_written = 0;
        strncpy(new_buffer, buffer, strlen(buffer));
        strncat(new_buffer, "\r\n", 2);
        bytes_written = serial_write(fd, new_buffer);
        sleep(5);
        return bytes_written;
}

int balance_read(int fd) {
        char buffer[32];
        int bytes_read = 0;
        (void)balance_write(fd, "P");
        bytes_read = serial_read(fd, buffer);
        print_buffer(buffer);
        sleep(10);
        return bytes_read;
}
