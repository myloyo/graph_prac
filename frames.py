import tkinter as tk
from tkinter import ttk


class LeftFrame:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.frame, text="Хранилище графов").pack()
        self.graph_listbox = tk.Listbox(self.frame, height=20)
        self.graph_listbox.pack(fill=tk.BOTH, expand=True)


class BottomFrame:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_buttons(self, ops):
        # Create frames for button organization
        basic_frame = tk.Frame(self.frame)
        basic_frame.pack(side=tk.LEFT, padx=5)

        algorithm_frame = tk.Frame(self.frame)
        algorithm_frame.pack(side=tk.LEFT, padx=5)

        basic_buttons = [
            ("Load Graph", ops.load_graph),
            ("Add Vertex", ops.add_vertex),
            ("Add Edge", ops.add_edge),
            ("Delete Vertex", ops.delete_vertex),
            ("Delete Edge", ops.delete_edge),
            ("AdjList", ops.print_adjacency_list),
        ]

        for text, command in basic_buttons:
            tk.Button(basic_frame, text=text, command=command).pack(side=tk.LEFT)

        ttk.Separator(self.frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Algorithm buttons
        algorithm_buttons = [
            ("DFS", ops.dfs_algorithm),
            ("BFS", ops.bfs_algorithm),
            ("Task 8. Dijkstra", ops.dijkstra_algorithm),
            ("Task 9. Floyd-Warshall", ops.floyd_warshall_algorithm),
            ("Task 10. Bellman-Ford", ops.bellman_ford_algorithm),
            ("Task 11. Max Flow", ops.max_flow_algorithm),
        ]

        for text, command in algorithm_buttons:
            tk.Button(algorithm_frame, text=text, command=command).pack(side=tk.LEFT)

        tk.Button(self.frame, text="Exit", command=ops.root.quit).pack(side=tk.RIGHT)


class RightFrame:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.frame, text="Вывод результатов").pack()
        self.output_text = tk.Text(self.frame, wrap=tk.WORD, width=40)
        self.output_text.pack(fill=tk.BOTH, expand=True)
