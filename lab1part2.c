#include <stdio.h>

int main() {
    int x, y;

    printf("Введіть x: ");
    scanf("%d", &x);

    if ((x > -15 && x <= 3)) {
        y = 4 * x * x + 2;
        printf("y = %d\n", y);
    } 
    else if ((x <= -30) || (x > 20)) {
        y = (3 * x * x * x) / 4 - 5;
        printf("y = %d\n", y);
    } 
    else {
        printf("Функція не існує для даного x.\n");
    }

    return 0;
}
