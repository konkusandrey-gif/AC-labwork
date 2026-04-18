import random
import math

# Параметры варианта 5104
n1, n2, n3, n4 = 5, 1, 0, 4
seed_val = 5104
n = 10
k = 0.93

random.seed(seed_val)

# Генерируем базовую матрицу случайных чисел B
B = [[random.uniform(0, 2.0) for _ in range(n)] for _ in range(n)]

# Матрица смежности A_dir и A_undir
A_dir = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if B[i][j] * k >= 1.0:
            A_dir[i][j] = 1

A_undir = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if A_dir[i][j] == 1:
            A_undir[i][j] = A_undir[j][i] = 1

# Матрица весов W по формулам из методички
# C - веса на основе B
C = [[math.ceil(B[i][j] * 100 * A_undir[i][j]) for j in range(n)] for i in range(n)]
# D - вспомогательная матрица
D = [[1 if C[i][j] > 0 else 0 for j in range(n)] for i in range(n)]
# H - матрица несимметричности
H = [[1 if D[i][j] != D[j][i] else 0 for j in range(n)] for i in range(n)]
# Tr - верхняя треугольная матрица
Tr = [[1 if i < j else 0 for j in range(n)] for i in range(n)]

# Финальная матрица весов W (делаем её симметричной)
W = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        # Формула из методички: (d_ij + h_ij * tr_ij) * c_ij
        weight = (D[i][j] + H[i][j] * Tr[i][j]) * C[i][j]
        W[i][j] = weight

# Делаем W симметричной (так как граф ненаправленный)
for i in range(n):
    for j in range(n):
        if W[i][j] > 0:
            W[j][i] = W[i][j]

# --- Вывод матриц в консоль ---
print("Матриця суміжності (A_undir):")
for row in A_undir:
    print(*row)

print("\nМатриця ваг (W):")
for row in W:
    # Выводим красиво, заменяя 0 на "-" для наглядности
    print(*(f"{x:3}" if x > 0 else "  -" for x in row))

    import random
import math
from tkinter import *

# ==========================================
# 1. МАТЕМАТИКА ТА МАТРИЦІ (k=0.93)
# ==========================================
n1, n2, n3, n4 = 5, 1, 0, 4
seed_val = 5104
n = 10
k = 0.93

random.seed(seed_val)
B = [[random.uniform(0, 2.0) for _ in range(n)] for _ in range(n)]

A_dir = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if B[i][j] * k >= 1.0:
            A_dir[i][j] = 1

A_undir = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if A_dir[i][j] == 1:
            A_undir[i][j] = A_undir[j][i] = 1

C = [[math.ceil(B[i][j] * 100 * A_undir[i][j]) for j in range(n)] for i in range(n)]
D = [[1 if C[i][j] > 0 else 0 for j in range(n)] for i in range(n)]
H = [[1 if D[i][j] != D[j][i] else 0 for j in range(n)] for i in range(n)]
Tr = [[1 if i < j else 0 for j in range(n)] for i in range(n)]

W = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        W[i][j] = (D[i][j] + H[i][j] * Tr[i][j]) * C[i][j]

for i in range(n):
    for j in range(n):
        if W[i][j] > 0:
            W[j][i] = W[i][j]


# ПІДГОТОВКА ДО АЛГОРИТМУ КРАСКАЛА
# Збираємо всі ребра у список у форматі: (вага, вершина_1, вершина_2)
edges = []
for i in range(n):
    for j in range(i + 1, n): # i+1, щоб не дублювати ребра (граф ненапрямлений)
        if W[i][j] > 0:
            edges.append((W[i][j], i, j))

# Головний крок Краскала - сортуємо ребра за зростанням ваги!
edges.sort()

# Структура Union-Find для перевірки циклів
parent = list(range(n))

def find(i):
    if parent[i] == i:
        return i
    return find(parent[i])

def union(i, j):
    root_i = find(i)
    root_j = find(j)
    if root_i != root_j:
        parent[root_i] = root_j


# ГРАФІЧНИЙ ІНТЕРФЕЙС (Tkinter)

root = Tk()
root.title("Лабораторна робота 6 - Алгоритм Краскала (Мінімальний кістяк)")

canvas = Canvas(root, width=800, height=700, bg="white")
canvas.pack()

# Координати трикутника
def get_triangle_coords(start_x, start_y):
    step_x, step_y = 120, 120
    return [
        (start_x, start_y),
        (start_x - step_x/2, start_y + step_y), (start_x + step_x/2, start_y + step_y),
        (start_x - step_x, start_y + 2*step_y), (start_x, start_y + 2*step_y), (start_x + step_x, start_y + 2*step_y),
        (start_x - 1.5*step_x, start_y + 3*step_y), (start_x - 0.5*step_x, start_y + 3*step_y),
        (start_x + 0.5*step_x, start_y + 3*step_y), (start_x + 1.5*step_x, start_y + 3*step_y)
    ]

coords = get_triangle_coords(400, 100)
r = 20

mst_edges = []
current_edge_idx = 0
total_weight = 0

lbl_info = Label(root, text="Натисніть 'Наступний крок', щоб почати алгоритм Краскала.", font=("Arial", 14), bg="white")
lbl_info.pack(pady=5)

def draw_graph():
    canvas.delete("all")
    
    # 1.Малюємо всі оригінальні ребра тонкими сірими лініями і пишемо їх вагу
    for weight, u, v in edges:
        x1, y1 = coords[u]; x2, y2 = coords[v]
        if (u, v) not in mst_edges and (v, u) not in mst_edges:
            canvas.create_line(x1, y1, x2, y2, fill="gray90")
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            canvas.create_text(mid_x, mid_y, text=str(weight), fill="gray70", font=("Arial", 8))

    # 2.Малюємо ребра кістяка (жирні червоні) і їх вагу
    for u, v, weight in mst_edges:
        x1, y1 = coords[u]; x2, y2 = coords[v]
        canvas.create_line(x1, y1, x2, y2, fill="red", width=4)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        # Робимо червоний фон для тексту, щоб вагу було добре видно
        canvas.create_rectangle(mid_x-10, mid_y-8, mid_x+10, mid_y+8, fill="white", outline="white")
        canvas.create_text(mid_x, mid_y, text=str(weight), fill="red", font=("Arial", 11, "bold"))

    # 3.Малюємо вершини
    for i in range(n):
        x, y = coords[i]
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue", outline="black", width=2)
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12, "bold"))

def next_step():
    global current_edge_idx, total_weight
    
    # Якщо ми вже знайшли 9 ребер (для 10 вершин кістяк має рівно n-1 ребер)
    if len(mst_edges) == n - 1:
        lbl_info.config(text=f"Кістяк побудовано! Загальна сума ваг: {total_weight}", fg="green")
        btn_next.config(state=DISABLED)
        return

    # Шукаємо наступне ребро, яке не утворює цикл
    while current_edge_idx < len(edges):
        weight, u, v = edges[current_edge_idx]
        current_edge_idx += 1
        
        # Перевірка на цикл (якщо корені різні - циклу немає)
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v, weight))
            total_weight += weight
            lbl_info.config(text=f"Додано ребро ({u+1} - {v+1}) з вагою {weight}. Поточна сума: {total_weight}", fg="blue")
            draw_graph()
            
            # Якщо після додавання ми досягли n-1 ребер, повідомляємо про фінал
            if len(mst_edges) == n - 1:
                lbl_info.config(text=f"Кістяк побудовано! ЗАГАЛЬНА СУМА ВАГ: {total_weight}", fg="green")
                btn_next.config(state=DISABLED)
            return
            
    lbl_info.config(text="Граф незв'язний, побудувати повний кістяк неможливо.")

# Панель кнопок
control_frame = Frame(root, bg="white")
control_frame.pack(pady=5)

btn_next = Button(control_frame, text="Наступний крок (Краскал)", command=next_step, font=("Arial", 12), bg="lightgreen", width=25)
btn_next.pack()

draw_graph()
root.mainloop()