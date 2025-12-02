#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 8 

int main() {
    
    srand(time(NULL));

    double A[N][N];
    double X;
    int i, j;
    
    
    printf("Генерування матриці %dx%d...\n", N, N);
    
    
    
    double currentDiagValue = 100.0; 
    
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            if (i == j) {
                
                
                currentDiagValue -= (rand() % 50) / 10.0; 
                A[i][j] = currentDiagValue;
            } else {
               
                A[i][j] = (rand() % 1000) / 10.0;
            }
        }
    }

    
    printf("\nМатриця А:\n");
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            
            if (i == j)
                printf("[%5.1f] ", A[i][j]);
            else
                printf(" %5.1f  ", A[i][j]);
        }
        printf("\n");
    }

   
    printf("\nВведіть число X для пошуку у головній діагоналі: ");
    scanf("%lf", &X);

    
    
   
    
    
    int left = 0;
    int right = N - 1;
    int foundIndex = -1; 
    int iterations = 0;  

    while (left <= right) {
        iterations++;
        int mid = left + (right - left) / 2;
        
        
        
        if (A[mid][mid] == X) {
            foundIndex = mid;
            break; 
        }
        
        if (A[mid][mid] < X) {
           
            
            right = mid - 1;
        } else { 
            
            
            left = mid + 1;
        }
    }

    
    printf("\n--- Результат пошуку ---\n");
    if (foundIndex != -1) {
        printf("Число %.1f знайдено!\n", X);
        printf("Координати: рядок %d, стовпець %d (індекси починаються з 0)\n", foundIndex, foundIndex);
        printf("Кількість ітерацій: %d\n", iterations);
    } else {
        printf("Число %.1f не знайдено у головній діагоналі.\n", X);
    }

    return 0;
}