import tkinter as tk
import random
import numpy as np

# see Page 72ff in
# Kaufmann, M., & Wagner, D. (Eds.). (2003). Drawing graphs: methods and models. Springer.

natural_length=60
delta_init = 0.5

c_rho=(natural_length**3)/2;
c_sigma=natural_length*5;

canvas_width = 800
canvas_height = 800

current_iteration = 0

def vec(x,y): return np.array([x,y])

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

class Node:
    def __init__(self, label):
        self.label = label
        # Layout Information
        self.x = 50+random.random()*(canvas_width-100)
        self.y = 50+random.random()*(canvas_height-100)
        # data for step of the simulation
        self._force = vec(0.0,0.0) # sum of all forces acting on the node


# Data
(a,b,c,d,e) = ( Node("A"), Node("B"), Node("C"), Node("D"), Node("E") )
graph = Graph(  [a,b,c,d,e],
                [  (b,a), (c,a), (b,c), (b,e),
                        (b,d), (c,d), (c,e), (d,e) ] )

def create_random_graph(n,m):
    nodes=[Node(str(i+1)) for i in range(n)]
    edges = []
    for j in range(m):
        src = nodes[int(random.random()*len(nodes))]
        trgt = nodes[int(random.random() * len(nodes))]
        if (src!=trgt) and not (src,trgt) in edges and not (trgt,src) in edges:
            edges.append((src,trgt))
    return Graph(nodes, edges)

graph = create_random_graph(15,20)

helv12 = font=("Helvetica", 12, "bold")

def vec_length(vec):
    return np.sqrt(vec_length_squared(vec))

def vec_length_squared(vec):
    return sum(x ** 2 for x in vec)

def unit_length_vector_from_to(v1, v2):
    v = v2-v1
    len = vec_length(v)
    if len==0:
        return vec(0,0)
    else:
        return v/len



def anneal(d, i, maxi):
    # Select one of the following annealing schemes
    #return 0 if i>maxi else np.pow(d,(i*12)/maxi+1) # EXPONENTIAL
    #return 0 if i>maxi else  d-(i*d/maxi) # LINEAR
    return d/np.log(i+2) # LOGARITHMIC
    #return d # CONSTANT

def compute_forces_for_each_node(graph):
    # computes the values of _force for each node
   pass

def compute_new_position_for_each_node(graph, delta):
    # computes new x and y values for each node
    pass

def compute_layout(graph, iterations):
        global current_iteration
        if current_iteration == iterations: return
        delta = anneal(delta_init, current_iteration, iterations)
        current_iteration += 1
        compute_forces_for_each_node(graph)
        compute_new_position_for_each_node(graph, delta)

def  draw_nodes_and_edges(graph):
    for edge in graph.edges:
        canvas.create_line(edge[0].x, edge[0].y, edge[1].x, edge[1].y)
    for node in graph.nodes:
        canvas.create_oval(node.x-15, node.y-15, node.x+15, node.y+15, fill="#bcf60c", outline='black') #fill=next_color()
        canvas.create_text(node.x, node.y, text=node.label, font=helv12, fill="blue")


def draw_graph(canvas, graph):
    compute_layout(graph,100)
    draw_nodes_and_edges(graph)

def animate_graph():
    iterations=100
    global current_iteration
    compute_layout(graph, iterations)
    canvas.delete("all")
    draw_nodes_and_edges(graph)
    if current_iteration<iterations:
        root.after(50, animate_graph)  # call this function again after 50ms
    else:
        current_iteration=0


# Tkinter Window
root = tk.Tk()
root.title("Force-Directed Graph Layout (Eades, 1984)")

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Draw or animate graph

#draw_graph(canvas, graph)
animate_graph()

root.mainloop()
