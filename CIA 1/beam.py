import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
import sys

graph = {}
heuristics = []
G = nx.Graph() 

def add_edge(from_node, to_node, cost):
    graph[from_node].append((to_node, cost))
    G.add_edge(get_node(from_node), get_node(to_node), weight=cost)

def get_index(c):
    return ord(c) - ord('A')

def get_node(index):
    return chr(index + ord('A'))

def beam_search(start, goal, beam_width):
    queue = [[start]]
    
    while queue:
        new_queue = []
        
        for path in queue:
            current_node = path[-1]
            
            if current_node == goal:
                return path  
            
            for next_node, _ in graph[current_node]:
                if next_node not in path:
                    new_queue.append(path + [next_node])
        
        new_queue.sort(key=lambda p: heuristics[p[-1]])
        queue = new_queue[:beam_width]

    return None  

# Visualization 
def draw_graph(path_to_highlight=None):
    plt.clf()  
    
    pos = nx.spring_layout(G) 
    
    node_labels = {node: f"{node}({heuristics[get_index(node)]})" for node in G.nodes()}
    
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightblue', font_weight='bold', node_size=500, font_size=10)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path_to_highlight:
        path_labels = [get_node(p) for p in path_to_highlight]
        edge_list = [(path_labels[i], path_labels[i + 1]) for i in range(len(path_labels) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='r', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=path_labels, node_color='red')  
    
    plt.show()  

def process_graph():
    global graph, heuristics, G
    graph.clear()
    G.clear()
    
    try:
        nodes = node_input.get().split()  
        graph = {i: [] for i in range(len(nodes))}
        heuristics_input = heuristics_input_entry.get().split()  
        heuristics = list(map(int, heuristics_input))  
        
        edges = edge_input.get("1.0", tk.END).strip().split("\n")  
        
        for edge in edges:
            from_node, to_node, cost = edge.split()
            from_idx = get_index(from_node)
            to_idx = get_index(to_node)
            add_edge(from_idx, to_idx, int(cost))

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
    beam_width = int(beam_width_entry.get()) 

    path = beam_search(start, goal, beam_width)
    
    if path:
        result_label.config(text="Path: " + " -> ".join(get_node(p) for p in path))
        
        draw_graph(path)  
    else:
        result_label.config(text="No path found")

# GUI Setup
root = tk.Tk()
root.title("Graph Search Visualization")
root.geometry("450x450")


tk.Label(root, text="Enter nodes (e.g. A B C D E):").pack()
node_input = tk.Entry(root)
node_input.pack()

tk.Label(root, text="Enter heuristics (e.g. 6 4 3 2 0):").pack()
heuristics_input_entry = tk.Entry(root)
heuristics_input_entry.pack()

tk.Label(root, text="Enter edges (e.g. A B 1, one per line):").pack()
edge_input = tk.Text(root, height=5, width=30)
edge_input.pack()

tk.Label(root, text="Enter beam width:").pack()
beam_width_entry = tk.Entry(root)
beam_width_entry.pack()

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
