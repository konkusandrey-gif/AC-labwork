#include <stdio.h>
#include <stdlib.h>

// --- Структури даних ---

// Вузол списку (універсальний для стека і черги)
typedef struct Node {
    char data;              // Інформаційне поле (символ)
    struct Node* next;      // Вказівник на наступний елемент
} Node;

// Структура Черги (Queue) - зберігає вказівники на початок і кінець
typedef struct {
    Node* front; // Голова (звідси забираємо)
    Node* rear;  // Хвіст (сюди додаємо)
} Queue;

// Структура Стека (Stack) - потрібен для розвороту даних
typedef struct {
    Node* top;   // Вершина стека
} Stack;

// --- Прототипи функцій ---
void initQueue(Queue* q);
void initStack(Stack* s);
int isQueueEmpty(Queue* q);
int isStackEmpty(Stack* s);

// Основні операції з протоколюванням
void enqueue(Queue* q, char value);     // Додати в чергу
char dequeue(Queue* q);                 // Витягти з черги
void push(Stack* s, char value);        // Додати в стек
char pop(Stack* s);                     // Витягти зі стека
void freeQueue(Queue* q);               // Очищення пам'яті

// --- Реалізація функцій ---

void initQueue(Queue* q) {
    q->front = NULL;
    q->rear = NULL;
}

void initStack(Stack* s) {
    s->top = NULL;
}

int isQueueEmpty(Queue* q) {
    return (q->front == NULL);
}

int isStackEmpty(Stack* s) {
    return (s->top == NULL);
}

// Додавання елемента в чергу (EnQueue)
void enqueue(Queue* q, char value) {
    // 1. Створення вузла
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Помилка виділення пам'яті!\n");
        exit(1);
    }
    newNode->data = value;
    newNode->next = NULL;

    // ПРОТОКОЛ: Вивід стану створення
    printf("[PROTOCOL] Allocated Node at %p | Data: '%c' | Next: NULL\n", (void*)newNode, value);

    // 2. Зв'язування
    if (q->rear == NULL) {
        // Якщо черга порожня, новий елемент стає і головою, і хвостом
        q->front = newNode;
        q->rear = newNode;
        printf("[PROTOCOL] Queue Empty -> Front & Rear set to %p\n", (void*)newNode);
    } else {
        // Додаємо в кінець
        printf("[PROTOCOL] Linking: Old Rear (%p)->next points to New Node (%p)\n", (void*)q->rear, (void*)newNode);
        q->rear->next = newNode;
        q->rear = newNode; // Оновлюємо хвіст
    }
    printf("--------------------------------------------------\n");
}

// Вилучення елемента з черги (DeQueue)
char dequeue(Queue* q) {
    if (isQueueEmpty(q)) {
        printf("Черга порожня!\n");
        return '\0';
    }

    // 1. Запам'ятовуємо вузол, який видаляємо
    Node* temp = q->front;
    char data = temp->data;

    // 2. Пересуваємо голову
    q->front = q->front->next;

    // Якщо черга стала порожньою, хвіст теж має бути NULL
    if (q->front == NULL) {
        q->rear = NULL;
    }

    // ПРОТОКОЛ: Вивід видалення
    printf("[PROTOCOL] Dequeueing Node at %p | Data: '%c'\n", (void*)temp, data);
    printf("[PROTOCOL] Freeing memory at %p\n", (void*)temp);
    
    free(temp); // Звільняємо пам'ять
    printf("--------------------------------------------------\n");

    return data;
}

// Додавання в стек (Push) - допоміжна функція для розвороту
void push(Stack* s, char value) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) exit(1);
    
    newNode->data = value;
    newNode->next = s->top; // Новий елемент вказує на старий топ
    s->top = newNode;       // Оновлюємо топ
    
    // Стек - це службова структура, тут можна менш детальний протокол, 
    // але для повноти картини покажемо і його.
    printf("[Stack PROTOCOL] Pushed '%c' at %p. Top is now %p\n", value, (void*)newNode, (void*)newNode);
}

// Вилучення зі стека (Pop)
char pop(Stack* s) {
    if (isStackEmpty(s)) return '\0';
    
    Node* temp = s->top;
    char data = temp->data;
    s->top = s->top->next;
    
    printf("[Stack PROTOCOL] Popped '%c' from %p. Freeing.\n", data, (void*)temp);
    free(temp);
    return data;
}

// Функція звільнення пам'яті (якщо щось залишилось)
void freeQueue(Queue* q) {
    printf("\n--- Очищення пам'яті черги ---\n");
    while (!isQueueEmpty(q)) {
        dequeue(q);
    }
}

// --- ГОЛОВНА ФУНКЦІЯ ---
int main() {
    Queue sourceQueue;
    Queue destQueue;
    Stack tempStack;

    initQueue(&sourceQueue);
    initQueue(&destQueue);
    initStack(&tempStack);

    int n;
    printf("Введіть кількість елементів n (n > 0): ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("Некоректне значення n.\n");
        return 1;
    }
    
    // Очистка буфера після введення числа (щоб scanf %c не зчитав Enter)
    while (getchar() != '\n'); 

    printf("\n=== 1. ЗАПОВНЕННЯ ПОЧАТКОВОЇ ЧЕРГИ ===\n");
    for (int i = 0; i < n; i++) {
        char val;
        printf("Введіть символ %d: ", i + 1);
        scanf("%c", &val);
        while (getchar() != '\n'); // Очистка буфера
        enqueue(&sourceQueue, val);
    }

    printf("\n=== 2. ОБРОБКА (ПЕРЕПИСУВАННЯ У ЗВОРОТНОМУ ПОРЯДКУ) ===\n");
    printf("Логіка: Черга1 -> Стек (для розвороту) -> Черга2\n\n");

    // Крок А: Переносимо з Черги 1 у Стек
    // Ми НЕ знаємо N тут (згідно умови не використовуємо лічильник),
    // ми просто робимо "поки черга не пуста".
    while (!isQueueEmpty(&sourceQueue)) {
        char val = dequeue(&sourceQueue);
        push(&tempStack, val);
    }

    printf("\n--- Проміжний етап: дані у Стеку (в пам'яті) ---\n\n");

    // Крок Б: Переносимо зі Стека у Чергу 2
    while (!isStackEmpty(&tempStack)) {
        char val = pop(&tempStack);
        enqueue(&destQueue, val);
    }

    printf("\n=== 3. РЕЗУЛЬТАТ (ВМІСТ НОВОЇ ЧЕРГИ) ===\n");
    // Щоб вивести, нам доведеться видалити елементи з черги (або пройтись, не видаляючи).
    // Оскільки в лабораторних часто вимагають коректне звільнення пам'яті в кінці,
    // ми будемо виводити, виймаючи елементи (стандартна поведінка черги).
    
    printf("Елементи нової черги (виведення = видалення):\n");
    while (!isQueueEmpty(&destQueue)) {
        // Тут ми просто викликаємо dequeue, яка сама друкує протокол видалення.
        // Але щоб побачити "чистий" результат, додамо вивід символу окремо.
        char val = destQueue.front->data; 
        printf(" -> Елемент: '%c'\n", val);
        dequeue(&destQueue);
    }

    printf("\n=== роботу завершено ===\n");
    return 0;
}