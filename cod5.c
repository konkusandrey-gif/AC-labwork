#include <stdio.h>
#include <stdlib.h>
#include <time.h>


#define N 8


void printMatrix(int matrix[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
           
            if (i == j) {
                printf("\033[1;32m%4d\033[0m", matrix[i][j]); 
            } else {
                printf("%4d", matrix[i][j]);
            }
        }
        printf("\n");
    }
    printf("\n");
}




int binarySearch(int matrix[N][N], int item, int low, int high) {
    while (high >= low) {
        int mid = (low + high) / 2;
        
        
        
        if (item > matrix[mid][mid]) {
            high = mid - 1;
        } else {
            
            low = mid + 1;
        }
    }
    return low;
}


void binaryInsertionSortDiagonal(int matrix[N][N]) {
    int i, j, loc, selected;

    
    for (i = 1; i < N; ++i) {
        j = i - 1;
        selected = matrix[i][i]; 

        
        loc = binarySearch(matrix, selected, 0, j);

        
        while (j >= loc) {
            matrix[j + 1][j + 1] = matrix[j][j];
            j--;
        }

        
        matrix[loc][loc] = selected;
    }
}

int main() {
    int matrix[N][N];
    
   
    srand(time(NULL));

   
    printf("Генерування матрицi %dx%d...\n", N, N);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            matrix[i][j] = 10 + rand() % 90;
        }
    }

    
    matrix[0][0] = 10;
    matrix[N-1][N-1] = 99;

    printf("--- Початкова матриця (зеленим видiлена головна дiагональ) ---\n");
    printMatrix(matrix);

    
    binaryInsertionSortDiagonal(matrix);

    printf("--- Матриця пiсля сортування головної дiагоналi (за незбiльшенням) ---\n");
    printMatrix(matrix);

    
    int isSorted = 1;
    for(int i = 0; i < N - 1; i++) {
        if(matrix[i][i] < matrix[i+1][i+1]) {
            isSorted = 0;
            break;
        }
    }
    
    if(isSorted) {
        printf("Результат: Дiагональ успiшно вiдсортована!\n");
    } else {
        printf("Результат: Помилка сортування.\n");
    }

    return 0;
}