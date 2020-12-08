#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <rc/uart.h>

#define BUF_SIZE 32
#define TIMEOUT_S 0.5
#define BAUDRATE 115200

static void __print_usage(void) {
    puts("Hey hey!");
    return;
}

int main(int argc, char *argv[]) {
    char* test_str = "TSO";
    int bus, bytes = strlen(test_str), ret; // get number of bytes in test string
    uint8_t buf[BUF_SIZE];

    // Parse arguments
    if(argc != 2) {
        __print_usage();
        return -1;
    } else bus = atoi(argv[1]);

    if (!(bus==0||bus==1||bus==2||bus==5)) {
        __print_usage();
        return -1;
    }

    printf("\ntesting UART bus %d\n\n", bus);

    // Disable canonical (0), 1 stop bit (1), disable parity (0).
    if(rc_uart_init(bus, BAUDRATE, TIMEOUT_S, 0,1,0)) {
        printf("Failed to rc_uart_init%d\n", bus);
        return -1;
    }

    // Flush and Write
    printf("Sending  %d bytes: %s \n", bytes, test_str);
    rc_uart_flush(bus);
    rc_uart_write(bus, (uint8_t*)test_str, bytes);

    // Read
    printf("reading bytes:\n");
    memset(buf,0,sizeof(buf));
    ret = rc_uart_read_bytes(bus, buf, bytes);
    if (ret<0) fprintf(stderr,"Error reading bus\n");
    else if (ret==0) printf("timeout reached, %d bytes read\n", ret);
    else printf("Received %d bytes: %s \n", ret, buf);

    // Now write again.
    printf("\n");
    printf("Sending  %d bytes: %s \n", bytes, test_str);
    rc_uart_write(bus, (uint8_t*)test_str, bytes);

    // read back as line
    printf("reading line:\n");
    memset(buf,0,sizeof(buf));
    ret = rc_uart_read_line(bus, buf, sizeof(buf));
    if (ret<0) fprintf(stderr,"Error reading bus\n");
    else if (ret==0) printf("timeout reached, %d bytes read\n", ret);
    else printf("Received %d bytes: %s \n", ret, buf);

    // close
    rc_uart_close(bus);
    return 0;
}
