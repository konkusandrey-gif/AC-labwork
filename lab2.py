class Node:
    """Клас для вузла зв'язного списку"""
    def __init__(self, data):
        self.data = data  # Інформаційне поле (символ)
        self.next = None  # Вказівник на наступний елемент


class Queue:
    """Клас, що реалізує чергу на основі однозв'язного списку"""
    def __init__(self):
        self.head = None  # Початок черги
        self.tail = None  # Кінець черги

    def is_empty(self):
        """Перевірка, чи черга порожня"""
        return self.head is None

    def enqueue(self, data):
        """Додавання елемента в кінець черги"""
        new_node = Node(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        """Вилучення елемента з початку черги"""
        if self.is_empty():
            return None
        
        data = self.head.data
        self.head = self.head.next
        
        # Якщо після вилучення черга стала порожньою, хвіст теж None
        if self.head is None:
            self.tail = None
            
        return data

    def display(self):
        """Виведення елементів черги у консоль"""
        if self.is_empty():
            print("Черга порожня")
            return
            
        current = self.head
        while current:
            print(f"'{current.data}'", end=" -> " if current.next else "\n")
            current = current.next

    def clear(self):
        """Звільнення пам'яті (очищення черги)"""
        # Імітація ручного звільнення: послідовно видаляємо всі елементи,
        # знімаючи посилання, щоб збирач сміття Python звільнив пам'ять.
        while not self.is_empty():
            self.dequeue()


def reverse_transfer(source_queue, dest_queue):
    """
    Процедура для переписування черги у зворотному порядку 
    без використання лічильника (за допомогою рекурсії).
    """
    # Базовий випадок: якщо вихідна черга порожня, зупиняємо рекурсію
    if source_queue.is_empty():
        return
    
    # Крок 1: Вилучаємо елемент з початку
    char = source_queue.dequeue()
    
    # Крок 2: Рекурсивний виклик для наступних елементів
    reverse_transfer(source_queue, dest_queue)
    
    # Крок 3: На зворотному шляху рекурсії додаємо елемент у нову чергу.
    # Оскільки це зворотний хід, перший вилучений елемент додасться останнім.
    dest_queue.enqueue(char)


def main():
    try:
        n = int(input("Введіть кількість елементів n (n > 0): "))
        if n <= 0:
            print("Кількість елементів має бути більшою за 0.")
            return
    except ValueError:
        print("Помилка: введіть ціле число.")
        return

    # Створюємо дві черги
    q1 = Queue()
    q2 = Queue()

    print("\n--- Заповнення першої черги ---")
    for i in range(n):
        # Беремо лише перший символ, щоб гарантувати тип даних "символ"
        char_input = input(f"Введіть символ {i + 1}: ")
        symbol = char_input[0] if char_input else ' ' 
        q1.enqueue(symbol)

    print("\nВихідна черга 1 до перенесення:")
    q1.display()

    # Виконуємо завдання за варіантом
    reverse_transfer(q1, q2)

    print("\n--- Результат ---")
    print("Вихідна черга 1 після перенесення:")
    q1.display() # Має бути порожньою, бо ми все вилучили

    print("Нова черга 2 (в оберненому порядку):")
    q2.display()

    # Коректне звільнення пам'яті (Пункт 6)
    q1.clear()
    q2.clear()
    print("\nПам'ять успішно звільнено.")

if __name__ == "__main__":
    main()