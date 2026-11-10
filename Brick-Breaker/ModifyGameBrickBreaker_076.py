
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

# 5. MAIN GAME CLASS

class Game(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.width = 700
        self.height = 500

        # Game information
        self.score = 0
        self.lives = 3
        self.level = 1

        self.running = False
        self.paused = False
        self.game_over = False

        self.after_id = None

        self.configure(bg="#0f172a")

        # Game canvas
        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg="#0f172a",
            highlightthickness=0
        )

        self.canvas.pack(padx=10, pady=10)
        self.pack()

        # Game objects
        self.bricks = {}
        self.ball = None

        self.create_hud()

        self.paddle = Paddle(
            self.canvas,
            self.width / 2,
            self.height - 40
        )

        self.create_bricks()
        self.create_ball()

        self.show_message(
            "BRICK BREAKER",
            "Press SPACE to Start"
        )

        # Keyboard controls
        self.canvas.focus_set()

        self.canvas.bind(
            "<Left>",
            lambda event: self.paddle.move_paddle(-25)
        )

        self.canvas.bind(
            "<Right>",
            lambda event: self.paddle.move_paddle(25)
        )

        self.canvas.bind(
            "<space>",
            self.toggle_game
        )

        self.canvas.bind(
            "r",
            self.restart_game
        )

        self.canvas.bind(
            "R",
            self.restart_game
        )

 
    # Display score nya


    def create_hud(self):
        self.hud = self.canvas.create_text(
            self.width / 2,
            20,
            text="",
            fill="#ffffff",
            font=("Arial", 14, "bold"),
            tags="hud"
        )

        self.update_hud()

    def update_hud(self):
        self.canvas.itemconfig(
            self.hud,
            text=(
                f"SCORE: {self.score}     "
                f"LIVES: {self.lives}     "
                f"LEVEL: {self.level}"
            )
        )

   
    # ngebuat batanya
    

    def create_bricks(self):
        self.canvas.delete("brick")
        self.bricks = {}

        rows = min(3 + self.level, 6)
        columns = 8

        for row in range(rows):
            for col in range(columns):

                x = 65 + col * 82
                y = 75 + row * 32

                hits = min(
                    1 + row // 2 + (self.level - 1) // 2,
                    3
                )

                brick = Brick(
                    self.canvas,
                    x,
                    y,
                    hits
                )

                self.bricks[brick.item] = brick

    # membuat bolanya

    def create_ball(self):
        if self.ball is not None:
            self.ball.delete()

        self.ball = Ball(
            self.canvas,
            self.width / 2,
            self.height - 65,
            speed=5 + self.level
        )

    # display pesannya


    def show_message(self, title, subtitle):
        self.canvas.delete("message")

        self.canvas.create_text(
            self.width / 2,
            self.height / 2 - 25,
            text=title,
            fill="#38bdf8",
            font=("Arial", 30, "bold"),
            tags="message"
        )

        self.canvas.create_text(
            self.width / 2,
            self.height / 2 + 20,
            text=subtitle,
            fill="#ffffff",
            font=("Arial", 15),
            tags="message"
        )

    # start,pause,resume
   
    def toggle_game(self, event=None):

        if self.game_over:
            return

        if self.running:
            self.running = False
            self.paused = True

            self.show_message(
                "PAUSED",
                "Press SPACE to Resume"
            )

        else:
            self.running = True
            self.paused = False

            self.canvas.delete("message")
            self.game_loop()

    # loop game

    def game_loop(self):

        self.after_id = None

        if not self.running or self.paused:
            return

        # Save ball position before moving
        previous_coords = self.ball.get_position()

        self.ball.update()

        self.check_collisions(previous_coords)
        self.check_game_status()

        if self.running and not self.paused:
            self.after_id = self.after(
                16,
                self.game_loop
            )
