import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import networkx as nx
from graph_loader import load_graph_from_file
from graph_algorithms import GraphAlgorithms


class GraphOperations:
    def __init__(self, canvas, output_text, graph_listbox, root):
        self.canvas = canvas
        self.output_text = output_text
        self.graph_listbox = graph_listbox
        self.root = root
        self.graphs = {}
        self.graph = nx.Graph()
        self.current_graph_name = None
        self.algorithms = None

        # Bind listbox selection
        self.graph_listbox.bind('<<ListboxSelect>>', self.switch_graph)

    def dijkstra_algorithm(self):
        try:
            start = simpledialog.askstring("Дейкстра", "Введите стартовую вершину:")
            end = simpledialog.askstring("Дейкстра", "Введите конечную вершину:")
            self.output(f"{self.current_graph_name}: результат алгоритма Дейкстры для пути из {start} в {end}:")
            if start and end:
                distances, previous = self.algorithms.dijkstra(start, end)
                if distances[end] == float('inf'):
                    self.output(f"Нет пути из {start} в {end}")
                    return

                path = []
                current = end
                while current:
                    path.append(current)
                    current = previous[current]
                path.reverse()

                self.output(f"Кратчайший путь из {start} в {end}:")
                self.output(f"Путь: {' -> '.join(path)}")
                self.output(f"Расстояние: {distances[end]}")

                # Highlight the path
                path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                self.canvas.draw_graph(self.graph, highlight_edges=path_edges)
            self.output_text.insert(tk.END, "-" * 40 + "\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def floyd_warshall_algorithm(self):
        try:
            dist, next_node, nodes = self.algorithms.floyd_warshall()
            self.output(f"{self.current_graph_name}: Все кратчайшие пути из всех вершин:")

            for i, u in enumerate(nodes):
                for j, v in enumerate(nodes):
                    if i != j:
                        if dist[i][j] == float('inf'):
                            self.output(f"Нет пути из {u} в {v}")
                        else:
                            self.output(f"{u} -> {v}: Расстояние = {dist[i][j]}")
            self.output_text.insert(tk.END, "-" * 40 + "\n")
        except ValueError as e:
            messagebox.showerror("Ошибка!!!", str(e))

    def bellman_ford_algorithm(self):
        try:
            start = simpledialog.askstring("Беллмана-Форда", "Введите стартовую вершину:")
            if start:
                distances, previous = self.algorithms.bellman_ford(start)
                self.output(f"{self.current_graph_name}: Крайтчайшие пути из {start}:")
                for node in self.graph.nodes():
                    if distances[node] == float('inf'):
                        self.output(f"Нет пути до {node}")
                    else:
                        self.output(f"В {node}: расстояние = {distances[node]}")
            self.output_text.insert(tk.END, "-" * 40 + "\n")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def max_flow_algorithm(self):
        try:
            source = simpledialog.askstring("Максимальный поток", "Введите исток:")
            sink = simpledialog.askstring("Максимальный поток", "Введите сток:")
            if source and sink:
                max_flow = self.algorithms.ford_fulkerson(source, sink)
                self.output(f"{self.current_graph_name}: Максимальный поток из {source} в {sink}: {max_flow}")
                self.output_text.insert(tk.END, "-" * 40 + "\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def load_graph(self):
        filename = filedialog.askopenfilename(
            title="Выбор графа из файлов",
            filetypes=[("Text Files", "*.txt")]
        )
        if not filename:
            return

        try:
            self.graph = load_graph_from_file(filename)
            graph_name = filename.split("/")[-1].split("\\")[-1]
            self.graphs[graph_name] = self.graph
            self.graph_listbox.insert(tk.END, graph_name)
            self.current_graph_name = graph_name
            self.algorithms = GraphAlgorithms(self.graph, self.canvas, self.root)

            self.canvas.draw_graph(self.graph)
            self.output(f"Граф '{graph_name}' успешно загружен!")
            self.output_text.insert(tk.END, "-" * 40 + "\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def switch_graph(self, event):
        selection = self.graph_listbox.curselection()
        if not selection:
            return

        graph_name = self.graph_listbox.get(selection[0])
        self.current_graph_name = graph_name
        self.graph = self.graphs[graph_name]
        self.algorithms = GraphAlgorithms(self.graph, self.canvas, self.root)
        self.canvas.draw_graph(self.graph)
        self.output(f"Переключились на граф {graph_name}")
        self.output_text.insert(tk.END, "-" * 40 + "\n")

    def add_vertex(self):
        vertex = simpledialog.askstring("Добавить вершину", "Введите название вершины:")
        if vertex:
            self.graph.add_node(vertex)
            self.canvas.draw_graph(self.graph)
            self.output(f"{self.current_graph_name}: Добавлена вершина: {vertex}")
            self.output_text.insert(tk.END, "-" * 40 + "\n")

    def add_edge(self):
        edge = simpledialog.askstring("Добавить ребро", "Добавьте ребро (формат ввода: u v [вес]):")
        if not edge:
            return

        parts = edge.split()
        if len(parts) < 2:
            messagebox.showerror("Ошибка", "Неправильный формат ввода!")
            return

        u, v = parts[0], parts[1]
        if len(parts) > 2:
            try:
                w = float(parts[2])
                self.graph.add_edge(u, v, weight=w)
            except ValueError:
                messagebox.showerror("Ошибка", "Неправильный формат веса ребра!")
                return
        else:
            self.graph.add_edge(u, v)

        self.canvas.draw_graph(self.graph)
        self.output(f"{self.current_graph_name}: Добавлено ребро: {edge}")
        self.output_text.insert(tk.END, "-" * 40 + "\n")

    def delete_vertex(self):
        vertex = simpledialog.askstring("Удаление вершины", "Введите название вершины:")
        if vertex and vertex in self.graph:
            self.graph.remove_node(vertex)
            self.canvas.draw_graph(self.graph)
            self.output(f"{self.current_graph_name}: Удалена вершина: {vertex}")
            self.output_text.insert(tk.END, "-" * 40 + "\n")
        else:
            messagebox.showerror("Ошибка", "Вершина не найдена!")

    def delete_edge(self):
        edge = simpledialog.askstring("Удаление ребра", "Введите ребро (формат ввода: u v):")
        if not edge:
            return

        parts = edge.split()
        if len(parts) != 2:
            messagebox.showerror("Ошибка", "Неправильный формат ввода!")
            return

        u, v = parts
        if self.graph.has_edge(u, v):
            self.graph.remove_edge(u, v)
            self.canvas.draw_graph(self.graph)
            self.output(f"{self.current_graph_name}: Удалено ребро: {edge}")
            self.output_text.insert(tk.END, "-" * 40 + "\n")
        else:
            messagebox.showerror("Ошибка", "Ребро не найдено!")

    def print_adjacency_list(self):
        self.output(f"{self.current_graph_name}: Список смежности:")
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            self.output(f"{node}: {neighbors}")
        self.output_text.insert(tk.END, "-" * 40 + "\n")

    def dfs_algorithm(self):
        try:
            start = simpledialog.askstring("DFS", "Введите стартовую вершину:")
            if start:
                visited, edges = self.algorithms.dfs(start)
                self.output(f"{self.current_graph_name}: DFS из {start}: {visited}")
                self.output_text.insert(tk.END, "-" * 40 + "\n")
                self.canvas.draw_graph(self.graph, highlight_nodes=visited)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def bfs_algorithm(self):
        try:
            start = simpledialog.askstring("BFS", "Введите стартовую вершину:")
            if start:
                visited, edges = self.algorithms.bfs(start)
                self.output(f"{self.current_graph_name}: BFS из {start}: {visited}")
                self.output_text.insert(tk.END, "-" * 40 + "\n")
                self.canvas.draw_graph(self.graph, highlight_nodes=visited)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))