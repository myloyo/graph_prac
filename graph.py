import tkinter as tk
from tkinter import ttk
from frames import LeftFrame, BottomFrame, RightFrame
from visualisation import GraphCanvas
from graph_operations import GraphOperations


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализатор графов")

        self.left_frame = LeftFrame(root)
        self.bottom_frame = BottomFrame(root)
        self.right_frame = RightFrame(root)
        self.canvas = GraphCanvas(root)

        self.graph_ops = GraphOperations(
            self.canvas,
            self.right_frame.output_text,
            self.left_frame.graph_listbox,
            self.root
        )

        # Connect buttons to operations
        self.bottom_frame.setup_buttons(self.graph_ops)