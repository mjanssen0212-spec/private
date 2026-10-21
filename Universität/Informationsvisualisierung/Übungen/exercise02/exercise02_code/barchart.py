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


def draw_bar_chart(canvas, data, colors, width, height, padding=40):
    max_value = max(data.values())
    bar_width = (width - 2 * padding) / len(data)

    for i, (label, value) in enumerate(data.items()):
        # Calculate bar height
        bar_height = (value / max_value) * (height - 2 * padding)

        # Coordinates
        x0 = padding + i * bar_width
        y0 = height - padding - bar_height
        x1 = x0 + bar_width * 0.8
        y1 = height - padding

        # Draw bar
        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i % len(colors)], outline="black")

        # Draw value label above the bar
        canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(value), fill="black")

        # Draw category label below the bar
        canvas.create_text((x0 + x1) / 2, y1 + 10, text=label, fill="black")


# Set up the main window
root = tk.Tk()
root.title("Simple Bar Chart with Tkinter")

canvas_width = 500
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

draw_bar_chart(canvas, data, colors, width=canvas_width, height=canvas_height)

root.mainloop()