# Name: Matthias Janßen
# Matr.-Nr.: 1871808
import tkinter as tk

# Colors for the bars
colors = ['red', 'yellow', 'pink', 'brown', 'purple', 'blue', 'green', 'orange']

scale = 10

def draw_pixel(canvas, x, y, color):
    canvas.create_rectangle(x * scale, y * scale, x * scale + scale, y * scale + scale, fill=color, outline=color)

def bresenham(x0, y0, x1, y1):
    """
    Implementiert den vollständigen Bresenham-Algorithmus für alle Oktanten.
    Gibt eine Liste von Pixeln (x, y) zurück.
    """
    pixels = []
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    
    if dx > dy:
        # 1. Oktant (und Spiegelungen)
        d = 2 * dy - dx
        x, y = x0, y0
        while x != x1:
            pixels.append((x, y))
            if d < 0:
                d += 2 * dy
            else:
                d += 2 * (dy - dx)
                y += sy
            x += sx
        pixels.append((x, y))
    else:
        # 2. Oktant (und Spiegelungen)
        d = 2 * dx - dy
        x, y = x0, y0
        while y != y1:
            pixels.append((x, y))
            if d < 0:
                d += 2 * dx
            else:
                d += 2 * (dx - dy)
                x += sx
            y += sy
        pixels.append((x, y))
        
    return pixels

# Set up the main window
root = tk.Tk()
root.title("Draw Pixels with Tkinter - Bresenham")

canvas_width = 500
canvas_height = 400
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Testfälle aus verschiedenen Oktanten
test_cases = [
    ((5, 5), (20, 10), colors[0]),   # 1. Oktant (0 < a < 1)
    ((5, 5), (10, 20), colors[1]),   # 2. Oktant (a > 1)
    ((20, 5), (5, 10), colors[2]),   # Spiegelung an y-Achse (-1 < a < 0)
    ((20, 5), (15, 20), colors[3]),  # a < -1
    ((5, 20), (20, 15), colors[4]),  # -1 < a < 0
    ((5, 20), (10, 5), colors[5]),   # a < -1
    ((20, 20), (5, 15), colors[6]),  # 0 < a < 1 (vertauscht)
    ((20, 20), (15, 5), colors[7]),  # a > 1 (vertauscht)
]

for (p0, p1, color) in test_cases:
    line_pixels = bresenham(p0[0], p0[1], p1[0], p1[1])
    for px, py in line_pixels:
        draw_pixel(canvas, px, py, color)

root.mainloop()