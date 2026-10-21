

import tkinter as tk
import tkinter.font as tkfont
import random
import math

# Sample data for the word cloud
data = {
    "Emilia": 4.2,
    "Noah": 3.8,
    "Sophia": 3.5,
    "Matteo": 3.3,
    "Emma": 3.1,
    "Liam": 2.9,
    "Mia": 2.8,
    "Elias": 2.7,
    "Hannah": 2.5,
    "Leon": 2.4,
    "Lina": 2.3,
    "Ben": 2.2,
    "Ella": 2.1,
    "Paul": 2.0,
    "Marie": 1.9,
    "Felix": 1.8,
    "Anna": 1.7,
    "Lukas": 1.6,
    "Lea": 1.5,
    "Maximilian": 1.4,
}

# Colors for the words
colors = ['red', 'orange', 'pink', 'brown', 'purple', 'blue', 'grey']
font_families = ["Arial", "Helvetica", "Times", "Courier"]

class WordBox:

    def __init__(self, word: str, weight: float, x: int, y: int, width: int, height: int, font_family: str, font_size: int, color: str):
        self.word = word
        self.weight = weight
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_family = font_family
        self.font_size = font_size
        self.color = color

    def draw_box(self, canvas: tk.Canvas, framed=False):
        # we set anchor="nw" such that x,y are the coordinates of the upper left corner of the box
        canvas.create_text(self.x, self.y, anchor="nw", text=self.word,
                           font=(self.font_family, self.font_size), fill=self.color)
        if framed:
            canvas.create_rectangle(self.x, self.y,self.x + self.width, self.y + self.height, outline="red")

    def check_collision(self, boxes):
        for box in boxes:
            if self.x+self.width < box.x or box.x+box.width < self.x:
                continue
            if self.y+self.height < box.y or box.y+box.height < self.y:
                continue
            return True
        return False

def compute_boxes(data):
    max_value = max(data.values())
    max_font_size = 32
    boxes = []

    for i, (text, value) in enumerate(data.items()):
        font_size = round( math.log(value,10) / math.log(max_value,10) * max_font_size)
        font_family = random.choice(font_families)
        color = random.choice(colors)
        font = tkfont.Font(family=font_family, size=font_size)
        box_height = font.metrics("linespace")
        box_width = font.measure(text)
        boxes.append( WordBox(text, value,0,0, box_width, box_height, font_family, font_size, color))
    return boxes

def draw_wordcloud(canvas, data):
    placed_boxes = []
    boxes = compute_boxes(data)
    boxes.sort(reverse=True, key=lambda box: box.weight)
    for box in boxes:
        if place_box(box, placed_boxes):
                box.draw_box(canvas)


def place_box(box, placed_boxes):
    return True
    # 1. Move the box along the Archimedian Spiral until
    #    there is no collision with already placed boxes
    #    Note: Spiral starts at center of canvas
    # 2. Add box to placed_boxes and return True
    # 3. If box could not be placed return False

# Set up the main window
root = tk.Tk()
root.title("Simple Word Cloud with Tkinter")

canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

draw_wordcloud(canvas, data)

root.mainloop()