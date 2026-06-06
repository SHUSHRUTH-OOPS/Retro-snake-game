import pygame
import random
import asyncio

pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Async Snake Game")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont(None, 36)


def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


async def main():

    # Snake setup
    snake = [(100, 100)]
    snake_dir = (CELL, 0)

    # Food setup
    food = (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )

    score = 0
    running = True

    while running:

        clock.tick(10)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and snake_dir != (0, CELL):
                    snake_dir = (0, -CELL)

                if event.key == pygame.K_DOWN and snake_dir != (0, -CELL):
                    snake_dir = (0, CELL)

                if event.key == pygame.K_LEFT and snake_dir != (CELL, 0):
                    snake_dir = (-CELL, 0)

                if event.key == pygame.K_RIGHT and snake_dir != (-CELL, 0):
                    snake_dir = (CELL, 0)

        # Move snake
        head_x = snake[0][0] + snake_dir[0]
        head_y = snake[0][1] + snake_dir[1]

        new_head = (head_x, head_y)

        # Wall collision
        if (
            head_x < 0 or
            head_x >= WIDTH or
            head_y < 0 or
            head_y >= HEIGHT
        ):
            running = False

        # Self collision
        if new_head in snake:
            running = False

        snake.insert(0, new_head)

        # Food collision
        if new_head == food:

            score += 1

            food = (
                random.randrange(0, WIDTH, CELL),
                random.randrange(0, HEIGHT, CELL)
            )

        else:
            snake.pop()

        # Draw
        screen.fill(BLACK)

        # Draw snake
        for segment in snake:

            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0], segment[1], CELL, CELL)
            )

        # Draw food
        pygame.draw.rect(
            screen,
            RED,
            (food[0], food[1], CELL, CELL)
        )

        # Draw score
        draw_text(f"Score: {score}", WHITE, 10, 10)

        pygame.display.flip()

        # Required for pygbag/browser async loop
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())