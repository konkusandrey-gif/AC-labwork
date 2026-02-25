#include <stdio.h>
#include <math.h>

// Структура для повернення двох значень
typedef struct {
    double term; // Поточний член F_i
    double sum;  // Сума S_i
} ResultPair;


ResultPair recursion_ascent(int n, double x) {
    // Базовий випадок: i = 1
    if (n == 1) {
        ResultPair base;
        base.term = 1.0;
        base.sum = 1.0;
        return base;
    }

    // Рекурсивний виклик (йдемо в глибину до 1)
    ResultPair prev = recursion_ascent(n - 1, x);

    // Обчислення на "поверненні" (після виклику)
    double current_term = -prev.term * x * (3.0 * n - 5.0) / (3.0 * n - 3.0);
    double current_sum = prev.sum + current_term;

    ResultPair current;
    current.term = current_term;
    current.sum = current_sum;

    return current;
}

// Функція-обгортка (для зручності виклику в main)
double calculate_recursion_ascent(int n, double x) {
    if (n < 1) return 0.0;
    ResultPair res = recursion_ascent(n, x);
    return res.sum;
}

int main() {
    int n = 5;
    double x = 0.5;

    double result = calculate_recursion_ascent(n, x);
    double check = 1.0 / pow(1.0 + x, 1.0/3.0);

    printf("--- Спосіб 2 (Повернення + Struct) ---\n");
    printf("n = %d, x = %.2f\n", n, x);
    printf("Результат рекурсії: %.10f\n", result);
    printf("Точне значення:     %.10f\n", check);
    printf("Похибка:            %.10e\n", fabs(result - check));

    return 0;
}