import pygame
import pymunk
import math
from random import randint
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading


class Ball:
    def __init__(self, x, y, size):
        self.size = size
        mass = self.size**2
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        angle = randint(0, 359)
        coeff = 40000 / mass
        self.body = pymunk.Body(mass)
        self.body.position = (x, y)
        self.body.velocity = (
            coeff * math.cos(angle * math.pi / 180),
            coeff * math.sin(angle * math.pi / 180),
        )
        self.shape = pymunk.Circle(self.body, self.size)
        self.shape.elasticity = 1
        self.shape.density = 1
        space.add(self.body, self.shape)

    def draw(self):
        x = int(self.body.position.x)
        y = int(self.body.position.y)
        pygame.draw.circle(wn, self.color, (x, y), self.size)


def create_segment(pos1, pos2):
    segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    segment_shape = pymunk.Segment(segment_body, pos1, pos2, 10)
    segment_shape.elasticity = 1
    space.add(segment_body, segment_shape)


def collision_handler(arbiter, space, data):
    global collision_count
    collision_count += 1
    return True


pygame.init()
wn = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()

FPS = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
collision_count = 0
start_time = time.time()

balls = [Ball(randint(0, 600), randint(0, 600), randint(10, 20)) for i in range(50)]
pos_tl = (0, 0)
pos_tr = (600, 0)
pos_bl = (0, 600)
pos_br = (600, 600)
segment1 = create_segment(pos_tl, pos_tr)
segment2 = create_segment(pos_tr, pos_br)
segment3 = create_segment(pos_br, pos_bl)
segment4 = create_segment(pos_bl, pos_tl)

# Add collision handler
handler = space.add_default_collision_handler()
handler.begin = collision_handler

# Data for plotting
times = []
collisions = []
avg_collisions_per_second_list = []

# Set up the matplotlib figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
(line1,) = ax1.plot([], [], label="Collisions")
(line2,) = ax2.plot([], [], label="Avg Collisions/Sec", color="red")


def init():
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 50)
    ax1.set_xlabel("Time (seconds)")
    ax1.set_ylabel("Number of Collisions")
    ax1.set_title("Collisions with Respect to Time Elapsed")
    ax1.legend()
    ax1.grid(True)

    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("Average Collisions per Second")
    ax2.set_title("Average Collisions per Second with Respect to Time Elapsed")
    ax2.legend()
    ax2.grid(True)
    return line1, line2


def update(frame):
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        avg_collisions_per_second = collision_count / elapsed_time
    else:
        avg_collisions_per_second = 0

    times.append(elapsed_time)
    collisions.append(collision_count)
    avg_collisions_per_second_list.append(avg_collisions_per_second)

    line1.set_data(times, collisions)
    line2.set_data(times, avg_collisions_per_second_list)

    ax1.set_xlim(0, max(10, elapsed_time))
    ax1.set_ylim(0, max(50, collision_count + 10))
    ax2.set_xlim(0, max(10, elapsed_time))
    ax2.set_ylim(0, max(1, avg_collisions_per_second + 0.1))

    return line1, line2


ani = FuncAnimation(fig, update, init_func=init, interval=1000, cache_frame_data=False)


def run_pygame():
    global running
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        wn.fill(WHITE)
        [ball.draw() for ball in balls]
        pygame.draw.line(wn, BLACK, pos_tl, pos_tr, 10)
        pygame.draw.line(wn, BLACK, pos_tr, pos_br, 10)
        pygame.draw.line(wn, BLACK, pos_br, pos_bl, 10)
        pygame.draw.line(wn, BLACK, pos_bl, pos_tl, 10)

        # Calculate average collisions per second, per minute, and per hour
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            avg_collisions_per_second = collision_count / elapsed_time
            avg_collisions_per_minute = collision_count / (elapsed_time * 60)
            avg_collisions_per_hour = collision_count / (elapsed_time * 3600)
        else:
            avg_collisions_per_second = 0
            avg_collisions_per_minute = 0
            avg_collisions_per_hour = 0

        # Display collision counter
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Collisions: {collision_count}", True, BLACK)
        wn.blit(text, (400, 10))

        # Display average collision counters
        avg_text_sec = font.render(
            f"Avg Collisions/Sec: {avg_collisions_per_second:.2f}", True, RED
        )
        avg_text_min = font.render(
            f"Avg Collisions/Min: {avg_collisions_per_minute:.2f}", True, RED
        )
        avg_text_hour = font.render(
            f"Avg Collisions/Hour: {avg_collisions_per_hour:.2f}", True, RED
        )
        wn.blit(avg_text_sec, (10, 10))
        wn.blit(avg_text_min, (10, 50))
        wn.blit(avg_text_hour, (10, 90))

        pygame.display.flip()
        clock.tick(FPS)
        space.step(1 / FPS)

    pygame.quit()


# Run Pygame in a separate thread
pygame_thread = threading.Thread(target=run_pygame)
pygame_thread.start()

# Show the Matplotlib plot
plt.show()

# Ensure the Pygame thread is properly joined
pygame_thread.join()
