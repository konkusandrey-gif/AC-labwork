import random
from tkinter import *


# параметри для генерації матриці

n1, n2, n3, n4 = 5, 1, 0, 4
seed_val = 5104
n = 10

# Новий коефіцієнт k = 1.0 - n3*0.01 - n4*0.005 - 0.15
k = 1.0 - 0 * 0.01 - 4 * 0.005 - 0.15 # Дорівнює 0.83

random.seed(seed_val)
A_dir = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        value = random.uniform(0, 2.0) * k
        if value >= 1.0:
            A_dir[i][j] = 1


# Алгоритм обходу (Генерація кроків)

# Ми заздалегідь генеруємо список кроків, щоб потім програвати їх по кнопці "Наступний крок"

def get_start_vertex(visited):
    # Шукаємо невідвідану вершину з найменшим номером, яка має хоча б 1 вихідну дугу
    for i in range(n):
        if not visited[i] and sum(A_dir[i]) > 0:
            return i
    # Якщо таких немає, беремо просто першу невідвідану
    for i in range(n):
        if not visited[i]:
            return i
    return -1

def generate_bfs_steps():
    visited = [False] * n
    steps = [] # Формат: ('тип_дії', вершина_1, вершина_2)
    
    while True:
        start_v = get_start_vertex(visited)
        if start_v == -1: break
        
        queue = [start_v]
        visited[start_v] = True
        steps.append(('visit', start_v, None)) # Відвідали (Жовтий)
        
        while queue:
            u = queue.pop(0)
            for v in range(n):
                if A_dir[u][v] == 1 and not visited[v]:
                    visited[v] = True
                    queue.append(v)
                    steps.append(('edge', u, v))   # Ребро дерева (Червоне)
                    steps.append(('visit', v, None)) # Відвідали (Жовтий)
            steps.append(('done', u, None)) # Повністю обробили (Зелений)
    return steps

def generate_dfs_steps():
    visited = [False] * n
    steps = []

    def dfs(u):
        visited[u] = True
        steps.append(('visit', u, None))
        for v in range(n):
            if A_dir[u][v] == 1 and not visited[v]:
                steps.append(('edge', u, v))
                dfs(v)
        steps.append(('done', u, None))

    while True:
        start_v = get_start_vertex(visited)
        if start_v == -1: break
        dfs(start_v)
    return steps

# матриці і нумерація 

def print_matrix(matrix, title):
    print(f"\n{title}:")
    for row in matrix:
        print(*row)

def print_vector_mapping(steps, title):
    # Збираємо порядок відвідування вершин (протокол)
    protocol = []
    for step in steps:
        if step[0] == 'visit' and step[1] not in protocol:
            protocol.append(step[1])
    
    # Формуємо вектор: індекс = стара вершина, значення = новий номер
    mapping = [0] * n
    for new_number, old_index in enumerate(protocol):
        mapping[old_index] = new_number + 1
        
    print(f"\n{title}:")
    for i in range(n):
        print(f"Стара вершина {i+1:2d}  ->  Новий номер {mapping[i]:2d}")

# 1. Оригінальна матриця
print_matrix(A_dir, "Матриця суміжності оригінального графа (k=0.83)")

# 2. Дані для BFS
bfs_steps = generate_bfs_steps()
bfs_tree_matrix = [[0 for _ in range(n)] for _ in range(n)]
for step in bfs_steps:
    if step[0] == 'edge':
        bfs_tree_matrix[step[1]][step[2]] = 1

print_matrix(bfs_tree_matrix, "Матриця дерева обходу в ширину (BFS Tree)")
print_vector_mapping(bfs_steps, "Вектор відповідності нумерації (BFS)")

# 3. Дані для DFS
dfs_steps = generate_dfs_steps()
dfs_tree_matrix = [[0 for _ in range(n)] for _ in range(n)]
for step in dfs_steps:
    if step[0] == 'edge':
        dfs_tree_matrix[step[1]][step[2]] = 1

print_matrix(dfs_tree_matrix, "Матриця дерева обходу в глибину (DFS Tree)")
print_vector_mapping(dfs_steps, "Вектор відповідності нумерації (DFS)")

# 3. Генеруємо матрицю для DFS
dfs_tree_matrix = [[0 for _ in range(n)] for _ in range(n)]
dfs_steps = generate_dfs_steps()
for step in dfs_steps:
    if step[0] == 'edge':
        u, v = step[1], step[2]
        dfs_tree_matrix[u][v] = 1

print_matrix(dfs_tree_matrix, "Матриця дерева обходу в глибину (DFS Tree)")



# графічний інтерфейс (Tkinter)
root = Tk()
root.title("Лабораторна робота 5 - Обхід графа")

# Панель з кнопками
control_frame = Frame(root)
control_frame.pack(pady=10)

canvas = Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Координати трикутника (як у ЛР 3)
def get_triangle_coords(start_x, start_y):
    step_x, step_y = 100, 100
    return [
        (start_x, start_y),
        (start_x - step_x/2, start_y + step_y), (start_x + step_x/2, start_y + step_y),
        (start_x - step_x, start_y + 2*step_y), (start_x, start_y + 2*step_y), (start_x + step_x, start_y + 2*step_y),
        (start_x - 1.5*step_x, start_y + 3*step_y), (start_x - 0.5*step_x, start_y + 3*step_y),
        (start_x + 0.5*step_x, start_y + 3*step_y), (start_x + 1.5*step_x, start_y + 3*step_y)
    ]
coords = get_triangle_coords(400, 100)
r = 20

# Глобальні змінні для стану візуалізації
current_steps = []
step_index = 0
v_states = [0] * n # 0-Білий, 1-Жовтий, 2-Зелений
tree_edges = []
protocol = []

def draw_graph():
    canvas.delete("all")
    
    # 1. Малюємо всі звичайні ребра (тонкі, чорні)
    for i in range(n):
        for j in range(n):
            if A_dir[i][j] == 1 and (i, j) not in tree_edges:
                x1, y1 = coords[i]; x2, y2 = coords[j]
                canvas.create_line(x1, y1, x2, y2, arrow=LAST, fill="gray80") # Робимо їх світлішими, щоб дерево виділялося

    # 2. Малюємо ребра дерева обходу (товсті, червоні)
    for (u, v) in tree_edges:
        x1, y1 = coords[u]; x2, y2 = coords[v]
        canvas.create_line(x1, y1, x2, y2, arrow=LAST, fill="red", width=3, arrowshape=(15, 20, 6))

    # 3. Малюємо вершини
    colors = ["white", "yellow", "lightgreen"]
    for i in range(n):
        x, y = coords[i]
        c = colors[v_states[i]]
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline="black", width=2)
        canvas.create_text(x, y, text=str(i + 1), font=("Arial", 12, "bold"))
        
    # 4. Виводимо протокол обходу знизу
    protocol_text = "Протокол обходу: " + " -> ".join([str(v + 1) for v in protocol])
    canvas.create_text(400, 550, text=protocol_text, font=("Arial", 14, "bold"), fill="blue")

def next_step():
    global step_index
    if step_index < len(current_steps):
        action, u, v = current_steps[step_index]
        if action == 'visit':
            v_states[u] = 1
            protocol.append(u)
        elif action == 'edge':
            tree_edges.append((u, v))
        elif action == 'done':
            v_states[u] = 2
        step_index += 1
        draw_graph()

def start_bfs():
    reset()
    global current_steps
    current_steps = generate_bfs_steps()
    btn_next.config(state=NORMAL)
    canvas.create_text(400, 30, text="Режим: Обхід в ширину (BFS)", font=("Arial", 14), tags="mode")

def start_dfs():
    reset()
    global current_steps
    current_steps = generate_dfs_steps()
    btn_next.config(state=NORMAL)
    canvas.create_text(400, 30, text="Режим: Обхід в глибину (DFS)", font=("Arial", 14), tags="mode")

def reset():
    global current_steps, step_index, v_states, tree_edges, protocol
    current_steps = []
    step_index = 0
    v_states = [0] * n
    tree_edges = []
    protocol = []
    btn_next.config(state=DISABLED)
    draw_graph()

# Кнопки
Button(control_frame, text="1. Підготувати BFS", command=start_bfs, width=20, bg="lightblue").pack(side=LEFT, padx=10)
Button(control_frame, text="1. Підготувати DFS", command=start_dfs, width=20, bg="lightpink").pack(side=LEFT, padx=10)
btn_next = Button(control_frame, text="2. Наступний крок", command=next_step, width=20, bg="lightgreen", state=DISABLED)
btn_next.pack(side=LEFT, padx=10)
Button(control_frame, text="Скинути", command=reset, width=10).pack(side=LEFT, padx=10)

# Початкова відрисовка
draw_graph()
root.mainloop()