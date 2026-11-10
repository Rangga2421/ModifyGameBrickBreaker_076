
import tkinter as tk
import random


# 1. GAME OBJECT (PARENT CLASS)

class GameObject:
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)



# 2. class bola
class Ball(GameObject):
    def __init__(self, canvas, x, y, speed=6):
        self.radius = 9
        self.speed = speed

        self.dx = random.choice([-1, 1]) * speed
        self.dy = -speed

        item = canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill="#ffffff",
            outline="#38bdf8",
            width=2
        )

        super().__init__(canvas, item)

    def update(self):
        self.move(self.dx, self.dy)

        coords = self.get_position()
        width = self.canvas.winfo_width()

        # Pantulan dinding kiri dan kanan
        if coords[0] <= 0:
            self.dx = abs(self.dx)

        elif coords[2] >= width:
            self.dx = -abs(self.dx)

        # Pantulan dinding atas
        if coords[1] <= 0:
            self.dy = abs(self.dy)



# 3. class paddle

class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 100
        self.height = 14

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill="#38bdf8",
            outline="#7dd3fc",
            width=2
        )

        super().__init__(canvas, item)

    def move_paddle(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            self.move(offset, 0)



# 4. class baloknya


class Brick(GameObject):

    COLORS = {
        1: "#22c55e",
        2: "#f59e0b",
        3: "#ef4444"
    }

    def __init__(self, canvas, x, y, hits):
        self.width = 70
        self.height = 22
        self.hits = hits

        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill=self.COLORS[hits],
            outline="#ffffff",
            width=1,
            tags="brick"
        )

        super().__init__(canvas, item)

    def hit(self):
        self.hits -= 1

        if self.hits <= 0:
            self.delete()
            return True

        self.canvas.itemconfig(
            self.item,
            fill=self.COLORS[self.hits]
        )

        return False
