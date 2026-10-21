import tkinter as tk
import math

data = {
    'Apples': 30,
    'Bananas': 15,
    'Cherries': 25,
    'Dates': 10,
    'Eldenberries': 20
}

colors = ['red', 'yellow', 'pink', 'brown', 'purple']

def draw_pie_chart(canvas, data, colors, width, height):
    total_value = 0
    x0 = 100
    y0 = 100

    x1 = 400
    y1 = 400

    for i, (label, value) in enumerate(data.items()):
        total_value += value

    total_angle = 0

    for i, (label, value) in enumerate(data.items()):
        angle = (value / total_value) * 360

        canvas.create_arc(x0, y0, x1, y1, start=total_angle, extent=angle, fill=colors[i % len(colors)], outline="black")

        total_angle += angle

root = tk.Tk()
root.title("Simple Pi Chart with Tkinter")

canvas_width = 500
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

draw_pie_chart(canvas, data, colors, width=canvas_width, height=canvas_height)

root.mainloop()