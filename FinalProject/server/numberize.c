#include <stdio.h>
#include <unistd.h>

int main() {
    unsigned char c;
    while(read(0, &c, 1))
        printf("%d\n", c);
    return 0;
}
