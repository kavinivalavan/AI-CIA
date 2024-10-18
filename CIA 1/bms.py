import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import sys

graph = {}
G = nx.Graph()  

def add_edge(from_node, to_node):
    graph[from_node].append((to_node))
    G.add_edge(get_node(from_node), get_node(to_node))

def get_index(c):
    return ord(c) - ord('A')

def get_node(index):
    return chr(index + ord('A'))

def british_museum_search(start, goal, path, all_paths):
    path.append(start)

    if start == goal:
        all_paths.append([get_node(p) for p in path])
        return

    for next_node in graph[start]:
        if next_node not in path:  
            british_museum_search(next_node, goal, path.copy(), all_paths)

# Visualization
def draw_graph(path_to_highlight=None):
    plt.clf()  
    
    pos = nx.spring_layout(G)  
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=500, font_size=10)
    
    if path_to_highlight:
        edge_list = [(path_to_highlight[i], path_to_highlight[i+1]) for i in range(len(path_to_highlight) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='r', width=2)
    
    plt.show() 

def process_graph():
    global graph, G
    graph.clear()
    G.clear()
    try:
        nodes = node_input.get().split()  
        graph = {i: [] for i in range(len(nodes))}
        edges = edge_input.get("1.0", tk.END).strip().split("\n")  
        
        for edge in edges:
            from_node, to_node = edge.split()
            from_idx = get_index(from_node)
            to_idx = get_index(to_node)
            add_edge(from_idx, to_idx)

        start_menu['menu'].delete(0, 'end')
        goal_menu['menu'].delete(0, 'end')
        
        for node in nodes:
            start_menu['menu'].add_command(label=node, command=tk._setit(start_var, node))
            goal_menu['menu'].add_command(label=node, command=tk._setit(goal_var, node))
        
        start_var.set(nodes[0])  
        goal_var.set(nodes[-1])  

        draw_graph()
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def run_search():
    start = get_index(start_var.get())
    goal = get_index(goal_var.get())
    
    all_paths = []
    british_museum_search(start, goal, [], all_paths)
    
    if all_paths:
        result_label.config(text="Paths: " + "\n".join(" -> ".join(path) for path in all_paths))
        
        draw_graph(all_paths[0])
    else:
        result_label.config(text="No path found")

# GUI Setup
root = tk.Tk()
root.title("Graph Search Visualization")
root.geometry("350x350")

tk.Label(root, text="Enter nodes (e.g. A B C D E):").pack()
node_input = tk.Entry(root)
node_input.pack()

tk.Label(root, text="Enter edges (e.g. A B, one per line):").pack()
edge_input = tk.Text(root, height=5, width=30)
edge_input.pack()

tk.Label(root, text="Select start node:").pack()
start_var = tk.StringVar()
start_menu = tk.OptionMenu(root, start_var, '')
start_menu.pack()

tk.Label(root, text="Select goal node:").pack()
goal_var = tk.StringVar()
goal_menu = tk.OptionMenu(root, goal_var, '')
goal_menu.pack()

process_button = tk.Button(root, text="Process Graph", command=process_graph)
process_button.pack()

run_button = tk.Button(root, text="Run Search", command=run_search)
run_button.pack()

result_label = tk.Label(root, text="Result will be displayed here")
result_label.pack()

root.mainloop()
