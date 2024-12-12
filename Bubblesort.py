import tkinter as tk
import time


def draw_bars(canvas, data, colors):
    canvas.delete("all")
    canvas_height = 400
    canvas_width = 600
    bar_width = canvas_width / len(data)
    for i, value in enumerate(data):
        x0 = i * bar_width
        y0 = canvas_height - value
        x1 = (i + 1) * bar_width
        y1 = canvas_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i])
    canvas.update()


def bubble_sort_visual(canvas, data):
    n = len(data)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):

            colors = ['blue' for _ in range(len(data))]
            colors[j] = 'red'
            colors[j+1] = 'red'
            draw_bars(canvas, data, colors)
            time.sleep(0.5)

            if data[j] > data[j+1]:

                data[j], data[j+1] = data[j+1], data[j]
                swapped = True


        if not swapped:
            break


    draw_bars(canvas, data, ['green' for _ in range(len(data))])


root = tk.Tk()
root.title("Sortare prin metoda bulelor")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()


data = [64, 34, 25, 12, 22, 11, 90]


bubble_sort_visual(canvas, data)

root.mainloop()
