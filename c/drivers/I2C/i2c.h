// i2c.h

#ifndef RC_I2C_H
    #define RC_I2C_H

    #ifdef  __cplusplus
        extern "C" {
    #endif

    #include <stddef.h>
    #include <stdint.h>

    #define I2C_MAX_BUS 5
    #define I2C_BUFFER_SIZE 128

    int rc_i2c_init(int bus, uint8_t devAddr);
    int rc_i2c_close(int bus);
    int rc_i2c_set_device_address(int bus, uint8_t devAddr);
    int rc_i2c_read_byte(int bus, uint8_t regAddr, uint8_t *data);
    int rc_i2c_read_bytes(int bus, uint8_t regAddr, size_t count,  uint8_t *data);
    int rc_i2c_read_word(int bus, uint8_t regAddr, uint16_t *data);
    int rc_i2c_read_words(int bus, uint8_t regAddr, size_t count, uint16_t* data);
    int rc_i2c_write_byte(int bus, uint8_t regAddr, uint8_t data);
    int rc_i2c_write_bytes(int bus, uint8_t regAddr, size_t count, uint8_t* data);
    int rc_i2c_write_word(int bus, uint8_t regAddr, uint16_t data);
    int rc_i2c_write_words(int bus, uint8_t regAddr, size_t count, uint16_t* data);
    int rc_i2c_send_bytes(int bus, size_t count, uint8_t* data);
    int rc_i2c_send_byte(int bus, uint8_t data);
    int rc_i2c_lock_bus(int bus);
    int rc_i2c_unlock_bus(int bus);
    int rc_i2c_get_lock(int bus);
    int rc_i2c_get_fd(int bus);

    #ifdef RC_AUTOPILOT_EXT
        int rc_i2c_read_data(int bus, uint8_t regAddr, size_t length, uint8_t *data);
    #endif

    #ifdef __cplusplus
        }
    #endif
#endif
