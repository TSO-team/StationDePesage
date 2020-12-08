#ifndef RC_UART_H
    #define RC_UART_H

    #ifdef __cplusplus
        extern "C" {
    #endif

    #include <stdint.h>

    /* bus           The bus number /dev/ttyO{bus}
     * @param[in]  baudrate      must be one of the standard speeds in the UART
     * spec. 115200 and 57600 are most common.
     * @param[in]  timeout       timeout is in seconds and must be >=0.1
     * @param[in]  canonical_en  0 for non-canonical mode (raw data), non-zero for
     * canonical mode where only one line ending in '\n' is read at a time.
     * @param[in]  stop_bits     number of stop bits, 1 or 2, usually 1 for most
     * sensors
     * @param[in]  parity_en     0 to disable parity, nonzero to enable. usually
     * disabled for most sensors.
     *
     * @return     0 on success, -1 on failure */

    int rc_uart_init(int bus, int baudrate, float timeout, int canonical_en, int stop_bits, int parity_en);
    int rc_uart_close(int bus);
    int rc_uart_get_fd(int bus);
    int rc_uart_flush(int bus);
    int rc_uart_write(int bus, uint8_t* data, size_t bytes);
    int rc_uart_read_bytes(int bus, uint8_t* buf, size_t bytes);
    int rc_uart_read_line(int bus, uint8_t* buf, size_t max_bytes);
    int rc_uart_bytes_available(int bus);

    #ifdef __cplusplus
        }
    #endif
#endif
