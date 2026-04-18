import random

#  Параметри (по варіанту=5104)
n1, n2, n3, n4 = 5, 1, 0, 4
seed_val = 5104
n = 10

# Нова формула для коефіцієнта k (
# k = 1.0 - n3*0.01 - n4*0.01 - 0.3
k = 1.0 - 0*0.01 - 4*0.01 - 0.3 # Дорівнює 0.66

random.seed(seed_val)

# Генерація матриць
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
        if A_dir[i][j] == 1:
            A_undir[i][j] = 1
            A_undir[j][i] = 1

# Розрахунок характеристик 

print("ЛАБОРАТОРНА РОБОТА 4 ")
print(f"Новий коефіцієнт k: {k:.2f}\n")

# Напівстепені напрямленого графа
out_degrees = [0] * n # Виходу (скільки стрілок виходить)
in_degrees = [0] * n  # Заходу (скільки стрілок заходить)

for i in range(n):
    for j in range(n):
        if A_dir[i][j] == 1:
            out_degrees[i] += 1 # З вершини i виходить стрілка
            in_degrees[j] += 1  # У вершину j заходить стрілка

print(" Напрямлений граф ")
for i in range(n):
    print(f"Вершина {i+1}: напівстепінь виходу = {out_degrees[i]}, напівстепінь заходу = {in_degrees[i]}")

# Степені ненапрямленого графа
undir_degrees = [0] * n
for i in range(n):
    for j in range(n):
        if A_undir[i][j] == 1:
            # У ненапрямленому графі петля (i == j) зазвичай дає +2 до степеня, 
            # але базовий підрахунок - це просто сума одиниць у рядку.
            undir_degrees[i] += 1 

print("\nНенапрямлений граф ")
for i in range(n):
    print(f"Вершина {i+1}: степінь = {undir_degrees[i]}")

# Перевірка на однорідність (регулярність)
# Граф однорідний, якщо всі його вершини мають однаковий степінь.
is_regular = True
first_degree = undir_degrees[0]
for deg in undir_degrees:
    if deg != first_degree:
        is_regular = False
        break

if is_regular:
    print(f"\nГраф є однорідним. Степінь однорідності: {first_degree}")
else:
    print("\nГраф не є однорідним (вершини мають різні степені).")

# Ізольовані та висячі вершини (для ненапрямленого графа)
isolated = []
pendant = []

for i in range(n):
    if undir_degrees[i] == 0:
        isolated.append(i + 1)
    elif undir_degrees[i] == 1:
        pendant.append(i + 1)

print("\nОсобливі вершини")
print(f"Ізольовані вершини (степінь 0): {isolated if isolated else 'Немає'}")
print(f"Висячі вершини (степінь 1): {pendant if pendant else 'Немає'}")


# Новий граф  та його матриця 

print("\n" + "="*40)
print("="*40)

# Новий коефіцієнт k = 1.0 - n3*0.005 - n4*0.005 - 0.27
k_new = 1.0 - 0 * 0.005 - 4 * 0.005 - 0.27 # Дорівнює 0.71
print(f"Оновлений коефіцієнт k: {k_new:.2f}")

# Обов'язково скидаємо seed генератора, щоб матриця формувалася з початку
random.seed(seed_val)

# Генеруємо нову напрямлену матрицю
A_new = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        value = random.uniform(0, 2.0) * k_new
        if value >= 1.0:
            A_new[i][j] = 1

print("\nМатриця суміжності НОВОГО напрямленого графа:")
for row in A_new:
    print(*row)

# Шляхи довжиною 2 і 3 (з проміжними вершинами)
paths_2 = []
paths_3 = []

for i in range(n):
    for j in range(n):
        for m in range(n):
            # Шлях довжиною 2: i -> m -> j
            if A_new[i][m] == 1 and A_new[m][j] == 1:
                paths_2.append(f"{i+1}-{m+1}-{j+1}")
            
            # Шлях довжиною 3: i -> m -> p -> j
            if A_new[i][m] == 1:
                for p in range(n):
                    if A_new[m][p] == 1 and A_new[p][j] == 1:
                        paths_3.append(f"{i+1}-{m+1}-{p+1}-{j+1}")

print(f"\nШляхів довжиною 2 знайдено: {len(paths_2)}")
# Виводимо перші 10 шляхів для прикладу, щоб не засмічувати консоль (можеш прибрати [:10], щоб вивести всі)
print("Приклади (перші 10):", ", ".join(paths_2[:10])) 

print(f"\nШляхів довжиною 3 знайдено: {len(paths_3)}")
print("Приклади (перші 10):", ", ".join(paths_3[:10]))


# Матриця досяжності (Алгоритм Воршелла)
R = [[A_new[i][j] for j in range(n)] for i in range(n)]

# Кожна вершина досяжна сама з себе (діагональ = 1)
for i in range(n):
    R[i][i] = 1

# Суть алгоритму Воршелла: якщо можна дійти з i в k, і з k в j, то можна дійти з i в j
for k in range(n):
    for i in range(n):
        for j in range(n):
            R[i][j] = R[i][j] or (R[i][k] and R[k][j])

print("\nМатриця досяжності:")
for row in R:
    print(*row)


# Матриця сильної зв'язності (S)
# Формула: S[i][j] = R[i][j] AND R[j][i]. Тобто можна дійти з i в j, І повернутися з j в i.
S = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        S[i][j] = R[i][j] & R[j][i]

print("\nМатриця сильної зв'язності:")
for row in S:
    print(*row)


# Компоненти сильної зв'язності
components = []
visited = [False] * n

for i in range(n):
    if not visited[i]:
        # Створюємо нову компоненту і додаємо туди поточну вершину
        comp = []
        for j in range(n):
            if S[i][j] == 1:
                comp.append(j + 1)
                visited[j] = True
        components.append(comp)

print("\nПерелік компонент сильної зв'язності:")
for idx, comp in enumerate(components):
    print(f"Компонента K{idx+1}: вершини {comp}")


# граф. частина

import math
from tkinter import *

print("\nБудуємо граф конденсації...")

# Знаходимо матрицю суміжності для графа конденсації (K_matrix)
num_comp = len(components)
K_matrix = [[0] * num_comp for _ in range(num_comp)]

for i in range(num_comp):
    for j in range(num_comp):
        if i != j:
            # Перевіряємо, чи є хоча б одна стрілка з компоненти i в компоненту j
            edge_exists = False
            for u in components[i]:
                for v in components[j]:
                    if A_new[u-1][v-1] == 1: # -1 бо індекси масиву починаються з 0
                        edge_exists = True
                        break
                if edge_exists: 
                    break
            if edge_exists:
                K_matrix[i][j] = 1

#Малюємо граф конденсації за допомогою Tkinter
root = Tk()
root.title("Лабораторна робота 4 - Граф конденсації")
canvas = Canvas(root, width=600, height=600, bg="white")
canvas.pack()

canvas.create_text(300, 50, text="Граф конденсації", font=("Arial", 16, "bold"))

center_x, center_y = 300, 300
radius_layout = 150 # Радіус кола, по якому б розставлялися компоненти, якби їх було багато
node_r = 40         # Радіус самої вершини-компоненти

comp_coords = []

# Розраховуємо координати для кожної компоненти (по колу)
for i in range(num_comp):
    if num_comp > 1:
        angle = 2 * math.pi * i / num_comp
        x = center_x + radius_layout * math.cos(angle)
        y = center_y + radius_layout * math.sin(angle)
    else:
        # Якщо компонента лише одна (як у твоєму випадку), ставимо її рівно по центру
        x, y = center_x, center_y
    comp_coords.append((x, y))

# Спочатку малюємо ребра між компонентами (якщо вони існують)
for i in range(num_comp):
    for j in range(num_comp):
        if K_matrix[i][j] == 1:
            x1, y1 = comp_coords[i]
            x2, y2 = comp_coords[j]
            # Додаємо велику стрілочку, щоб її було добре видно
            canvas.create_line(x1, y1, x2, y2, arrow=LAST, fill="black", width=2, arrowshape=(20, 30, 8))

# Потім малюємо самі вершини-компоненти поверх ребер
for i in range(num_comp):
    x, y = comp_coords[i]
    # Малюємо велике зелене коло
    canvas.create_oval(x - node_r, y - node_r, x + node_r, y + node_r, fill="lightgreen", outline="black", width=2)
    # Пишемо назву компоненти (K1, K2 і т.д.)
    canvas.create_text(x, y, text=f"K{i+1}", font=("Arial", 16, "bold"))
    
    # Знизу підписуємо, які саме вершини з оригінального графа сховалися всередині
    verts_str = "{" + ", ".join(map(str, components[i])) + "}"
    canvas.create_text(x, y + node_r + 20, text=verts_str, font=("Arial", 10))

root.mainloop()
