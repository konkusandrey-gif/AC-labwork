#include <stdio.h>
#include <math.h> 

int main() {
    int n;
    unsigned long long op_count = 0; 

    printf("Введіть натуральне число n: ");
    scanf("%d", &n);

    if (n < 1) {
        printf("Помилка: n має бути натуральним числом (>= 1).\n");
        return 1;
    }

    double P = 1.0;
    op_count++; 

    for (int i = 1; i <= n; i++) {
       
        op_count += 3; 

       
        double numerator = 2.0 * i * log(i + 3.0);
        op_count += 5; 

        
        double inner_sum = 0.0;
        op_count++; 

        for (int j = 1; j <= i; j++) {
            
            op_count += 3; +

           
            inner_sum += (2 * j + 1);
            op_count += 3; 
        }
        op_count++; 

        double denominator = inner_sum;
        op_count++; 

        
        P *= (numerator / denominator);
        op_count += 2; 
    }
    op_count++; 

    printf("\nРезультат (P): %.7f\n", P);
    printf("Кількість операцій: %llu\n", op_count);

    return 0;
}