#include <stdio.h>
#include <math.h>

// Функція-обгортка (Wrapper)
double calculate_recursion_descent(int n, double x);

// i - поточний крок, current_term - поточний член, current_sum - накопичена сума
double recursion_descent_impl(int n, double x, int i, double current_term, double current_sum) {
    // Умова виходу: якщо поточний крок перевищує n, повертаємо накопичену суму
    if (i > n) {
        return current_sum;
    }

    // Обчислення наступного члена ряду на "спуску"
    double next_term = -current_term * x * (3.0 * i - 5.0) / (3.0 * i - 3.0);
    
    // Оновлення суми
    double next_sum = current_sum + next_term;

    // Рекурсивний виклик з новими даними
    return recursion_descent_impl(n, x, i + 1, next_term, next_sum);
}

// Реалізація обгортки
double calculate_recursion_descent(int n, double x) {
    if (n < 1) return 0.0;
    // Початкові значення: крок=2 (бо 1-й вже є), член=1, сума=1
    if (n == 1) return 1.0;
    return recursion_descent_impl(n, x, 2, 1.0, 1.0);
}

int main() {
    int n = 5;      // Згідно завдання
    double x = 0.5; // Довільне x (< 1)

    double result = calculate_recursion_descent(n, x);
    double check = 1.0 / cbrt(1.0 + x); // Перевірочна функція (стандартна бібліотека)

    printf("--- Спосіб 1 (Спуск) ---\n");
    printf("n = %d, x = %.2f\n", n, x);
    printf("Результат рекурсії: %.10f\n", result);
    printf("Точне значення:     %.10f\n", check);
    printf("Похибка:            %.10e\n", fabs(result - check));

    return 0;
}