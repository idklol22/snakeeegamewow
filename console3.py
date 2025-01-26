import os
import time
import random
import keyboard 

WIDTH, HEIGHT = 40, 20

class Snake:
    def __init__(self):
        self.body = [[10, 10], [10, 9], [10, 8]]  
        self.direction = "RIGHT"

    def move(self):
        head = self.body[0][:]

        if self.direction == "UP":
            head[0] -= 1
        elif self.direction == "DOWN":
            head[0] += 1
        elif self.direction == "LEFT":
            head[1] -= 1
        elif self.direction == "RIGHT":
            head[1] += 1

        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:]
            or head[0] < 0
            or head[0] >= HEIGHT
            or head[1] < 0
            or head[1] >= WIDTH
        )

    def change_direction(self, new_direction):
        opposite = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposite[self.direction]:
            self.direction = new_direction

class Food:
    def __init__(self):
        self.position = []
        self.spawn()

    def spawn(self):
        self.position = [random.randint(0, HEIGHT - 5), random.randint(0, WIDTH - 5)]

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.score = 0
        self.last_update_time = 0
        self.game_speed = 0.2
        self.last_snake_positions = []

    def run(self):
        os.system("cls" )
        self.draw_border()
        self.draw_food()  

        while self.running:
            self.handle_input()
            self.update()

        print("\nGame Over! Your Score:", self.score)

    def handle_input(self):
        if keyboard.is_pressed("up"):
            self.snake.change_direction("UP")
        elif keyboard.is_pressed("down"):
            self.snake.change_direction("DOWN")
        elif keyboard.is_pressed("left"):
            self.snake.change_direction("LEFT")
        elif keyboard.is_pressed("right"):
            self.snake.change_direction("RIGHT")

    def update(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self.game_speed:
            self.last_snake_positions = self.snake.body[:]
            self.snake.move()
            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food.spawn()
                self.draw_food()  
                self.score += 1

            if self.snake.check_collision():
                self.running = False

            self.update_snake()
            self.last_update_time = current_time

    def draw_border(self):
       
        print("=" * (WIDTH + 2))
        for _ in range(HEIGHT):
            print("|" + " " * WIDTH + "|")
        print("=" * (WIDTH + 2))
        print(f"Score: {self.score}")

    def draw_food(self):
        
        self.move_cursor(self.food.position[0], self.food.position[1])
        print("$", end="", flush=True)

    def update_snake(self):
      
        tail = self.last_snake_positions[-1]
        self.move_cursor(tail[0], tail[1])
        print(" ", end="", flush=True)

        head = self.snake.body[0]
        self.move_cursor(head[0], head[1])
        print("O", end="", flush=True)
        self.move_cursor(HEIGHT + 1, 0)
        print(f"Score: {self.score}", end="", flush=True)

    def move_cursor(self, row, col):
        print(f"\033[{row + 1};{col + 2}H", end="")

if __name__ == "__main__":
    game = Game()
    game.run()  
