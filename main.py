import heapq
import random
from collections import defaultdict


class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.heuristic = {}
        self.cost = {}

    def add_edge(self, src, dest, cost):
        self.edges[src].append(dest)
        self.cost[(src, dest)] = cost

    def set_heuristic(self, node, value):
        self.heuristic[node] = value


def read_graph(filename):
    graph = Graph()
    with open(filename, "r") as file:
        lines = file.readlines()
        init = lines[0].strip().split(": ")[1]
        goal = lines[1].strip().split(": ")[1]
        for line in lines[2:]:
            parts = line.strip().split(" ")
            if len(parts) == 2:
                graph.set_heuristic(parts[0], float(parts[1]))
            elif len(parts) == 3:
                graph.add_edge(parts[0], parts[1], float(parts[2]))
    return graph, init, goal


def depth_first_search(graph, init, goal):
    stack = [(init, [init])]
    expanded_nodes = defaultdict(int)
    while stack:
        (node, path) = stack.pop()
        expanded_nodes[node] += 1
        successors = graph.edges[node]
        random.shuffle(successors)
        for neighbor in successors:
            if neighbor not in path:
                if neighbor == goal:
                    total_cost = sum(graph.cost[(path[i], path[i+1])] for i in range(len(path)-1)) + graph.cost[(node, neighbor)]
                    print(graph.cost[(node, neighbor)])
                    return path + [neighbor], total_cost, expanded_nodes
                stack.append((neighbor, path + [neighbor]))


def uniform_cost_search(graph, init, goal):
    queue = [(0, init, [init])]
    expanded_nodes = defaultdict(int)
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        expanded_nodes[node] += 1
        for neighbor in graph.edges[node]:
            if neighbor not in path:
                new_cost = cost + graph.cost[(node, neighbor)]
                if neighbor == goal:
                    return path + [neighbor], new_cost, expanded_nodes
                heapq.heappush(queue, (new_cost, neighbor, path + [neighbor]))


def greedy_search(graph, init, goal):
    queue = [(graph.heuristic[init], init, [init])]
    expanded_nodes = defaultdict(int)
    while queue:
        (_, node, path) = heapq.heappop(queue)
        expanded_nodes[node] += 1
        for neighbor in graph.edges[node]:
            if neighbor not in path:
                if neighbor == goal:
                    total_cost = sum(graph.cost[(path[i], path[i+1])] for i in range(len(path)-1)) + graph.cost[(node, neighbor)]
                    return path + [neighbor], total_cost, expanded_nodes
                heapq.heappush(queue, (graph.heuristic[neighbor], neighbor, path + [neighbor]))

def a_star_search(graph, init, goal):
    queue = [(graph.heuristic[init], 0, init, [init])]
    expanded_nodes = defaultdict(int)
    while queue:
        (priority, cost, node, path) = heapq.heappop(queue)
        expanded_nodes[node] += 1
        for neighbor in graph.edges[node]:
            if neighbor not in path:
                new_cost = cost + graph.cost[(node, neighbor)]
                if neighbor == goal:
                    return path + [neighbor], new_cost, expanded_nodes
                heapq.heappush(queue, (new_cost + graph.heuristic[neighbor], new_cost, neighbor, path + [neighbor]))


def print_results(method, path, cost, expanded_nodes):
    print(f"{method}:\n{' → '.join(path)}")
    print(f"Costo: {cost}")
    for node, count in expanded_nodes.items():
        print(f"{node}: Expandido {count} veces")
    print()


if __name__ == "__main__":
    graph, init, goal = read_graph("input.txt")

    dfs_path, dfs_cost, dfs_expanded_nodes = depth_first_search(graph, init, goal)
    print_results("Búsqueda en profundidad", dfs_path, dfs_cost, dfs_expanded_nodes)

    ucs_path, ucs_cost, ucs_expanded_nodes = uniform_cost_search(graph, init, goal)
    print_results("Búsqueda por costo uniforme", ucs_path, ucs_cost, ucs_expanded_nodes)

    greedy_path, greedy_cost, greedy_expanded_nodes = greedy_search(graph, init, goal)
    print_results("Búsqueda greedy", greedy_path, greedy_cost, greedy_expanded_nodes)

    a_star_path, a_star_cost, a_star_expanded_nodes = a_star_search(graph, init, goal)
    print_results("A*", a_star_path, a_star_cost, a_star_expanded_nodes)
