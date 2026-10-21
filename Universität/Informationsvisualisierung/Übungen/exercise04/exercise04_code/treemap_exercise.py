import tkinter as tk

class Node:
    def __init__(self, name, children=[], size=0, ratio=1.0):
        self.name = name
        self.children = children
        self.size = size
        self.ratio = ratio

    def __str__(self):
        cs=""
        for node in self.children:
            cs= cs+(f"{node}" if cs=="" else f",{node}")
        return f"{self.name}(size={self.size}, ratio={self.ratio}, children=[{cs}])"

# Data
tree =  Node('A',[
                Node( 'B', size=5),
                Node( 'C', [ Node('D', size=2), Node('E', size=3) ]),
                Node( 'F', [ Node('G', size=2), Node('H', size=4),
                             Node('I', [ Node('J', size=1), Node('K', size=3) ]) ])
            ])


colors = [
    "#e6194b",  # Red
    "#3cb44b",  # Green
    "#ffe119",  # Yellow
    "#4363d8",  # Blue
    "#f58231",  # Orange
    "#911eb4",  # Purple
    "#46f0f0",  # Cyan
    "#f032e6",  # Magenta
    "#bcf60c",  # Lime
    "#fabebe",   # Pink
    "#008080"   # Teal
]

helv36 = font=("Helvetica", 36, "bold")

color_counter=0
def next_color():
    global color_counter
    color=colors[color_counter % len(colors)]
    color_counter += 1
    return color


def draw_something(canvas,x, y, width,height,text):
    canvas.create_rectangle(x, y, x+width, y+height, fill=next_color(), outline='white')
    canvas.create_text(x + width / 2, y + height / 2, text=text, font=helv36, fill="white")


def draw_treemap(tree):
    ratio = tree.ratio
    total_size = tree.total_size
    if tree.children==[]:
        return ratio, total_size
    else:
        for node in enumerate(tree.children):
            draw_treemap(node)


# Tkinter Window
root = tk.Tk()
root.title("Treemap")

canvas_width = 600
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Draw a rectangle with a label
# draw_something(canvas, 20, 10, 200, 60, "Example")
# draw_something(canvas, 50, 90, 400, 60, "Another Example")

draw_treemap(tree)

print(tree)

root.mainloop()

"""
A(size=0, total_size=10, ratio=1.0, 
  children=[ 
     B(size=5, total_size=5, ratio=0.5, children=[]),
     C(size=0, total_size=5, ratio=0.5, 
       children=[
          D(size=2, total_size=2, ratio=0.4, children=[]),
          E(size=3, total_size=3, ratio=0.6, children=[])])])

"""