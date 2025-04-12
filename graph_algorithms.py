import networkx as nx
from tkinter import messagebox
import heapq
from collections import defaultdict
import math


class GraphAlgorithms:
    def __init__(self, graph, canvas, root):
        self.graph = graph
        self.canvas = canvas
        self.root = root
        self.INF = float('inf')

    def dfs(self, start_vertex):
        """Perform Depth-First Search."""
        if not self.graph.nodes():
            raise ValueError("Graph is empty!")

        if start_vertex not in self.graph:
            raise ValueError("Start vertex not found in graph!")

        visited = []
        visited_edges = set()
        self._dfs_helper(start_vertex, visited, visited_edges)
        return visited, visited_edges

    def _dfs_helper(self, node, visited, visited_edges):
        if node not in visited:
            visited.append(node)
            for neighbor in self.graph.neighbors(node):
                edge = (node, neighbor)
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    self.canvas.draw_graph(self.graph, highlight_edges=visited_edges)
                    self.root.update()
                    self.root.after(500)
                self._dfs_helper(neighbor, visited, visited_edges)

    def bfs(self, start_vertex):
        """Perform Breadth-First Search."""
        if not self.graph.nodes():
            raise ValueError("Graph is empty!")

        if start_vertex not in self.graph:
            raise ValueError("Start vertex not found in graph!")

        visited = []
        queue = [start_vertex]
        edges = set()

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in visited:
                        edge = (node, neighbor)
                        edges.add(edge)
                        self.canvas.draw_graph(self.graph, highlight_edges=edges)
                        self.root.update()
                        self.root.after(500)
                        queue.append(neighbor)

        return visited, edges

    def dijkstra(self, start, end=None):
        """Dijkstra's algorithm for shortest paths."""
        distances = {node: self.INF for node in self.graph.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes()}
        pq = [(0, start)]

        while pq:
            dist, current = heapq.heappop(pq)
            if current == end:
                break

            if dist > distances[current]:
                continue

            for neighbor in self.graph.neighbors(current):
                weight = self.graph[current][neighbor].get('weight', 1)
                new_dist = distances[current] + weight

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))

        return distances, previous

    def floyd_warshall(self):
        """Floyd-Warshall algorithm for all-pairs shortest paths."""
        nodes = list(self.graph.nodes())
        n = len(nodes)
        node_to_idx = {node: i for i, node in enumerate(nodes)}

        # Initialize distance matrix
        dist = [[self.INF] * n for _ in range(n)]
        next_node = [[None] * n for _ in range(n)]

        # Set diagonal to 0
        for i in range(n):
            dist[i][i] = 0

        # Initialize distances from graph
        for u, v, data in self.graph.edges(data=True):
            i, j = node_to_idx[u], node_to_idx[v]
            weight = data.get('weight', 1)
            dist[i][j] = weight
            next_node[i][j] = v
            if not self.graph.is_directed():
                dist[j][i] = weight
                next_node[j][i] = u

        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] != self.INF and dist[k][j] != self.INF:
                        if dist[i][j] > dist[i][k] + dist[k][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]
                            next_node[i][j] = next_node[i][k]

        return dist, next_node, nodes

    def bellman_ford(self, start):
        """Bellman-Ford algorithm for shortest paths with negative weights."""
        distances = {node: self.INF for node in self.graph.nodes()}
        distances[start] = 0
        previous = {node: None for node in self.graph.nodes()}

        # Relax edges |V| - 1 times
        for _ in range(len(self.graph.nodes()) - 1):
            for u, v, data in self.graph.edges(data=True):
                weight = data.get('weight', 1)
                if distances[u] != self.INF and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u

        # Check for negative cycles
        for u, v, data in self.graph.edges(data=True):
            weight = data.get('weight', 1)
            if distances[u] != self.INF and distances[u] + weight < distances[v]:
                raise ValueError("Graph contains a negative cycle!")

        return distances, previous

    def ford_fulkerson(self, source, sink):
        """Ford-Fulkerson algorithm for maximum flow."""

        def bfs(graph, s, t, parent):
            visited = {node: False for node in graph.nodes()}
            queue = [s]
            visited[s] = True

            while queue:
                u = queue.pop(0)
                for v in graph.neighbors(u):
                    if not visited[v] and graph[u][v].get('capacity', 0) > 0:
                        queue.append(v)
                        visited[v] = True
                        parent[v] = u

            return visited[t]

        # Create residual graph
        residual = nx.DiGraph()
        for u, v, data in self.graph.edges(data=True):
            capacity = data.get('weight', 1)  # Use weight as capacity
            residual.add_edge(u, v, capacity=capacity)
            residual.add_edge(v, u, capacity=0)  # Reverse edge

        parent = {node: None for node in residual.nodes()}
        max_flow = 0

        while bfs(residual, source, sink, parent):
            path_flow = self.INF
            s = sink
            while s != source:
                path_flow = min(path_flow, residual[parent[s]][s]['capacity'])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                residual[u][v]['capacity'] -= path_flow
                residual[v][u]['capacity'] += path_flow
                v = parent[v]

        return max_flow