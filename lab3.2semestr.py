import random
from tkinter import *

# Параметри 
n1, n2, n3, n4 = 5, 1, 0, 4
seed_val = 5104
n = 10
k = 0.73

# Генерація матриць
random.seed(seed_val)

# Напрямлена матриця (A_dir)
A_dir = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        value = random.uniform(0, 2.0) * k
        if value >= 1.0:
            A_dir[i][j] = 1

# Ненапрямлена матриця (A_undir)
A_undir = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        # Якщо в напрямленій є зв'язок (1), робимо його двостороннім у ненапрямленій
        if A_dir[i][j] == 1:
            A_undir[i][j] = 1
            A_undir[j][i] = 1

#  Вивід матриць у консоль 
print("Матриця суміжності напрямленого графа (A_dir):")
for row in A_dir:
    print(*row)

print("\nМатриця суміжності ненапрямленого графа (A_undir):")
for row in A_undir:
    print(*row)


# Графічна частина 
root = Tk()
root.title("Лабораторна робота 3 - Напрямлений та Ненапрямлений графи")

# Робимо вікно широким (1200 пікселів), щоб помістилося два графи
canvas = Canvas(root, width=1200, height=600, bg="white")
canvas.pack()

# Функція для розрахунку координат трикутника від заданої центральної точки
def get_triangle_coords(start_x, start_y):
    step_x = 100
    step_y = 100
    return [
        (start_x, start_y),
        (start_x - step_x/2, start_y + step_y),
        (start_x + step_x/2, start_y + step_y),
        (start_x - step_x, start_y + 2*step_y),
        (start_x, start_y + 2*step_y),
        (start_x + step_x, start_y + 2*step_y),
        (start_x - 1.5*step_x, start_y + 3*step_y),
        (start_x - 0.5*step_x, start_y + 3*step_y),
        (start_x + 0.5*step_x, start_y + 3*step_y),
        (start_x + 1.5*step_x, start_y + 3*step_y)
    ]

# Отримуємо списки координат: лівий граф - центр на X=300, правий на X=900
coords_dir = get_triangle_coords(300, 100)
coords_undir = get_triangle_coords(900, 100)
r = 20 # Радіус вершин

# Заголовки над графами
canvas.create_text(300, 50, text="Напрямлений граф", font=("Arial", 14, "bold"))
canvas.create_text(900, 50, text="Ненапрямлений граф", font=("Arial", 14, "bold"))

# Малювання ребер (ліній)

# Лінії для напрямленого графа (зі стрілочками)
for i in range(n):
    for j in range(n):
        if A_dir[i][j] == 1:
            x1, y1 = coords_dir[i]
            x2, y2 = coords_dir[j]
            canvas.create_line(x1, y1, x2, y2, arrow=LAST, fill="black" , arrowshape=(20, 30, 8))

# Лінії для ненапрямленого графа (без стрілочок)
for i in range(n):
    for j in range(n):
        if A_undir[i][j] == 1:
            x1, y1 = coords_undir[i]
            x2, y2 = coords_undir[j]
            # Малюємо звичайну лінію без arrow=LAST
            canvas.create_line(x1, y1, x2, y2, fill="black")


# Малювання вершин поверх ліній
# Винесли у функцію, щоб не писати двічі один і той самий цикл
def draw_vertices(coords):
    for i in range(n):
        x, y = coords[i]
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue", outline="black")
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12, "bold"))

draw_vertices(coords_dir)
draw_vertices(coords_undir)

root.mainloop()