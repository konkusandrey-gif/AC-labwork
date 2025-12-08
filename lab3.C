#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main() {
    
    srand(time(NULL));

    int n;
    double a, b;

    
    printf("Введіть значення a: ");
    if (scanf("%lf", &a) != 1) return 1;
    
    printf("Введіть значення b: ");
    if (scanf("%lf", &b) != 1) return 1;
    
    printf("Введіть розмір масиву n: ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("n має бути додатним цілим числом.\n");
        return 1;
    }

    
    double *Y = (double*)malloc(n * sizeof(double));
    double *Z = (double*)malloc(n * sizeof(double));

    if (Y == NULL || Z == NULL) {
        printf("Помилка виділення пам'яті.\n");
        return 1;
    }

    double range = (a != 0) ? fabs(a) * 2.5 : 10.0;
    
    printf("\nМасив Y:\n");
    for (int i = 0; i < n; i++) {
       
        double min = -range;
        double max = range;
        Y[i] = min + (rand() / (double)RAND_MAX) * (max - min);
        
        printf("%.3f ", Y[i]);
    }
    printf("\n");

    
    printf("\nМасив Z:\n");
    for (int i = 0; i < n; i++) {
        if (fabs(Y[i]) > a) {
            Z[i] = 5.0 - Y[i];
        } else {
            Z[i] = 3.0 * b * Y[i];
        }
        printf("%.3f ", Z[i]);
    }
    printf("\n");

   
    
    double R = -1.0; 
    
    for (int i = 0; i < n; i++) {
       
        double power_term = pow(-1, i + 1); 
        double value = fabs(Z[i] - power_term * a * b);

        
        if (i == 0 || value > R) {
            R = value;
        }
    }

    
    printf("\nРезультат R: %.3f\n", R);

   
    free(Y);
    free(Z);

    return 0;
}