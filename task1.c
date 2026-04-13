#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char** argv) {

    char *s = (char*)malloc(15);
    if (s == NULL) {
        printf("Malloc fails\n");
        return 1;
    }

    memset(s, 0, 15);
    strncpy(s, "Hello World!", 12);

    printf("%s\n", s);

    free(s);
    return 0;
}