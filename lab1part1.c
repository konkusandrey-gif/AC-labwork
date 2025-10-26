#include <stdio.h>

int main() {
    int x, y;

    printf("Введіть x: ");
    scanf("%d", &x);

    if (x > -15)
        if (x <= 3)
            y = 4 * x * x + 2;
        else if (x > 20)
            y = (3 * x * x * x) / 4 - 5;
        else {
            printf("Функція не існує для даного x.\n");
            return 0;
        }
    else if (x <= -30)
        y = (3 * x * x * x) / 4 - 5;
    else {
        printf("Функція не існує для даного x.\n");
        return 0;
    }

    printf("y = %d\n", y);
    return 0;
}
