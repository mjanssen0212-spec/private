import tkinter as tk

# Sample data for the bar chart
data = {
    'Apples': 30,
    'Bananas': 15,
    'Cherries': 25,
    'Dates': 10,
    'Elderberries': 20
}

# Colors for the bars
colors = ['red', 'yellow', 'pink', 'brown', 'purple']


def draw_waffle_chart(canvas, data, colors, width, height, padding=40):
    waffle_size = 10
    x0 = 0
    y0 = 0

    for i, (label, value) in enumerate(data.items()):
        
        for j in range(value):
            x1 = x0 + waffle_size
            y1 = x0 + waffle_size
            y0 = y1
            if y0 == 100:
                y0=0
            print(j)
            canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i % len(colors)], outline="black")
    

# Set up the main window
root = tk.Tk()
root.title("Simple Bar Chart with Tkinter")

canvas_width = 500
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

draw_waffle_chart(canvas, data, colors, width=canvas_width, height=canvas_height)

root.mainloop()