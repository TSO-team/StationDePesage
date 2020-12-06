// File:        c/utils/uarm_scan_test.c
// By:          Samuel Duclos
// For:         My team.
// Description: uARM scan test (output values on terminal)
// Usage:       sudo bash c/utils/uarm_scan_test
// Example:     sudo bash c/utils/uarm_scan_test

#include <stdio.h>

void uarm_scan_for_object(void);

int main(int argc, char *argv[]) {
    uarm_scan_for_object()
    return 0;
}

// Ewww... Update this using new Python version.
void uarm_scan_for_object(void) {
    /*
    for (unsigned char m = 0; m < 128; m++) {
        n = (m % 64) ? (63 - (m % 64)) : (m % 64);
        y = n / 8;
        x = (y % 2) ? (7 - (n % 8)) : (n % 8);
        usleep(500000);
        //if (y == 0) interfaceMalyanM200_deplacement((y % 2) ? (7 - (n % 8)) : (n % 8));
        interfaceMalyanM200_deplacement(x, y, 5, 120, 3000); // 4.
    }
    */
}
