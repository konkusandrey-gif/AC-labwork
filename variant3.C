#include <stdio.h>
#include <math.h>

double calculate_recursion_mixed(int n, double x);


// i - поточний індекс, current_term - вже обчислений член для цього індексу
double recursion_mixed_impl(int n, double x, int i, double current_term) {
    // Базовий випадок: якщо вийшли за межі n, додавати нічого
    if (i > n) {
        return 0.0;
    }

    // Обчислюємо наступний член для передачі "вниз"
    // Наступний крок буде i+1
    double next_term = -current_term * x * (3.0 * (i + 1) - 5.0) / (3.0 * (i + 1) - 3.0);

    // Поточний член + результат рекурсивного виклику
    return current_term + recursion_mixed_impl(n, x, i + 1, next_term);
}

double calculate_recursion_mixed(int n, double x) {
    if (n < 1) return 0.0;
    // Починаємо з i=1, де член=1.0
    return recursion_mixed_impl(n, x, 1, 1.0);
}

int main() {
    int n = 5;
    double x = 0.5;

    double result = calculate_recursion_mixed(n, x);
    double check = 1.0 / cbrt(1.0 + x);

    printf("--- Спосіб 3 (Змішаний) ---\n");
    printf("n = %d, x = %.2f\n", n, x);
    printf("Результат рекурсії: %.10f\n", result);
    printf("Точне значення:     %.10f\n", check);
    printf("Похибка:            %.10e\n", fabs(result - check));

    return 0;
}