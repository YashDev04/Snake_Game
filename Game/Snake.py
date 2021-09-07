from pygame.math import Vector2
import pygame, random, sys

pygame.init()
WIDTH = 400
HEIGHT = 800
CELL_SIZE = 30
CELL_NUM = 25
WINDOW = pygame.display.set_mode((CELL_SIZE * CELL_NUM, CELL_SIZE * CELL_NUM))  # surface
pygame.display.set_caption("Snake is back")
WHITE = (235, 235, 245)
FPS = 120

grass = pygame.image.load('Graphics/grass field.jpg').convert_alpha()
grass = pygame.transform.scale(grass, (800, 800))

apple = pygame.image.load('Graphics/apple.png').convert_alpha()  # import image
apple = pygame.transform.scale(apple, (33, 35))  # scale image



# OBJECTS
class SNAKE:
    def __init__(self):
        self.x = 12
        self.y = 12
        self.body = [Vector2(self.x, self.y), Vector2(self.x, self.y + 1),
                     Vector2(self.x, self.y + 2)]
        self.direction = Vector2(0, -1)

        self.snake_head_up = pygame.image.load('Graphics/Head-up.png').convert_alpha()
        self.snake_head_down = pygame.image.load('Graphics/Head-down.png').convert_alpha()
        self.snake_head_right = pygame.image.load('Graphics/Head-right.png').convert_alpha()
        self.snake_head_left = pygame.image.load('Graphics/Head-left.png').convert_alpha()

        self.snake_tail_up = pygame.image.load('Graphics/Tail-up.png').convert_alpha()
        self.snake_tail_down = pygame.image.load('Graphics/Tail-down.png').convert_alpha()
        self.snake_tail_left = pygame.image.load('Graphics/Tail-left.png').convert_alpha()
        self.snake_tail_right = pygame.image.load('Graphics/Tail-right.png').convert_alpha()

        self.snake_body = pygame.image.load('Graphics/body.png').convert_alpha()


    def print_snake(self):
        self.head_update()
        self.tail_update()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                WINDOW.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                WINDOW.blit(self.tail, block_rect)
            else:
                WINDOW.blit(self.snake_body, block_rect)

    def head_update(self):
        head_dir = self.body[1] - self.body[0]  # gives a vector of the direction in which the head is moving
        if head_dir == Vector2(0, 1):
            self.head = self.snake_head_up
        elif head_dir == Vector2(0, -1):
            self.head = self.snake_head_down
        elif head_dir == Vector2(1, 0):
            self.head = self.snake_head_left
        elif head_dir == Vector2(-1, 0):
            self.head = self.snake_head_right

    def tail_update(self):
        tail_dir = self.body[-2] - self.body[-1]  # gives a vector of the direction in which the tail is moving
        if tail_dir == Vector2(0, -1):
            self.tail = self.snake_tail_up
        elif tail_dir == Vector2(0, 1):
            self.tail = self.snake_tail_down
        elif tail_dir == Vector2(-1, 0):
            self.tail = self.snake_tail_left
        elif tail_dir == Vector2(1, 0):
            self.tail = self.snake_tail_right

    def move_snake(self):
        body_copy = self.body[:-1]  # grabs 1st two elements from the body list
        body_copy.insert(0, body_copy[
            0] + self.direction)  # add element(acts as head of snake) at the beginning of the list
        self.body = body_copy[:]

    def add_block(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[
            0] + self.direction)  # add element(acts as head of snake) at the beginning of the list
        self.body = body_copy[:]

class FRUIT:
    def __init__(self):
        self.random_pos()

    def print_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        WINDOW.blit(apple, fruit_rect)

    def random_pos(self):  # repositions the fruit
        self.x = random.randint(0, CELL_NUM - 2)
        self.y = random.randint(0, CELL_NUM - 2)
        self.pos = Vector2(self.x, self.y)


class MAIN:  # controls game logic
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.paused = False
        self.dead = False
    def updates(self):
        if not self.paused and not self.dead:
            self.snake.move_snake()
            self.eats()
            self.death()

    def print_elements(self):
        self.fruit.print_fruit()
        self.snake.print_snake()
        self.score()
        self.print_text("Press P to Pause the game", "Times New Roman", 20, (0,0,0),110,20)
        if self.paused:
            self.game_paused()
        elif self.dead:
            self.game_over()


    def eats(self):  # CHECKS IF THE FRUIT IS EATEN
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.random_pos()
            self.snake.add_block()

        for blk in self.snake.body[1:]:  # ensures that fruit is not on snake's body when randomized
            if blk == self.fruit.pos:
                self.fruit.random_pos()

    def death(self):
        # CHECKS IF THE SNAKE TOUCHES THE SIDES OF THE SCREEN

        if self.snake.body[0].x >= CELL_NUM or self.snake.body[0].x < 0:
            self.dead = not self.dead
            self.game_over()

        if self.snake.body[0].y >= CELL_NUM or self.snake.body[0].y < 0:
            self.dead = not self.dead
            self.game_over()

        #    CHECKS IF THE SNAKE TOUCHES ITSELF
        for block in self.snake.body[1:]:  # checks the whole list except for the 1st element (head)
            if block == self.snake.body[0]:
                self.dead = not self.dead
                self.game_over()

    def score(self):
        font = pygame.font.Font(None, 25)
        score_t = str(len(self.snake.body) - 3)
        score_board = font.render(score_t, True, (56, 74, 12))
        score_x = int(CELL_SIZE * CELL_NUM - 25)

        score_rect = score_board.get_rect()
        score_rect.center = (score_x, 20)

        # apple on scoreboard
        apple = pygame.image.load('Graphics/apple.png').convert_alpha()  # import image
        apple = pygame.transform.scale(apple, (18, 20))
        apple_rect = apple.get_rect()
        apple_rect.center = (score_x - 23, 19)

        # scoreboard_bg
        scr_bg = pygame.Rect(apple_rect.left - 4, apple_rect.top - 4, apple_rect.width + 35, apple_rect.height + 8)

        pygame.draw.rect(WINDOW, (10, 250, 100), scr_bg)
        WINDOW.blit(score_board, score_rect)
        WINDOW.blit(apple, apple_rect)
        pygame.draw.rect(WINDOW, (0, 0, 0), scr_bg, 2)

        if self.fruit.pos == apple_rect or self.fruit.pos == score_rect:  # ensures fruit does not spawn behind scoreboard
            self.fruit.random_pos()

    def print_text(self, text, font_name, size, color,x,y):
        font = pygame.font.SysFont(font_name, size)
        txt = font.render(text, True, color)
        txt_rect = txt.get_rect()
        txt_rect.center = (x,y)
        WINDOW.blit(txt, txt_rect)

    def game_paused(self):
        self.print_text("Paused", "Times New Roman", 180, (240,240,240), (CELL_SIZE * CELL_NUM)/2, (CELL_SIZE * CELL_NUM)/2.5)
        self.print_text("Press P to continue", "Times New Roman", 30, (240,240,240), (CELL_SIZE * CELL_NUM)/2, (CELL_SIZE * CELL_NUM)/1.9)
        self.print_text("Press R to restart", "Times New Roman", 30, (240,240,240), (CELL_SIZE * CELL_NUM)/2, (CELL_SIZE * CELL_NUM)/1.75)

    def game_over(self):
        self.print_text("GAME OVER", "Times New Roman", 120, (240,240,240), (CELL_SIZE * CELL_NUM)/2, (CELL_SIZE * CELL_NUM)/2.2)
        self.print_text("Press Esc to quit", "Times New Roman", 30, (240,240,240), (CELL_SIZE * CELL_NUM)/2, (CELL_SIZE * CELL_NUM)/1.8)
        self.print_text("Press R to restart", "Times New Roman", 30, (240,240,240), (CELL_SIZE * CELL_NUM)/2, (CELL_SIZE * CELL_NUM)/1.65)


main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT  # event triggered by user
pygame.time.set_timer(SCREEN_UPDATE, 115)  # event triggered every 115 ms
clock = pygame.time.Clock()
running = True
while running:

    for event in pygame.event.get():  # check for event
        if event.type == pygame.QUIT:  # type of event (quit in this case)
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.updates()
        if event.type == pygame.KEYDOWN:  # check for keys being pressed
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:  # if snake not going down, then up button is accepted
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:  # if snake not going up, then down button is accepted
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:  # if snake not going right, then left button is accepted
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:  # if snake not going left, then right button is accepted
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_p:
                main_game.paused = not main_game.paused
            if event.key == pygame.K_r:
                main_game.__init__()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    WINDOW.blit(grass, [0, 0])
    main_game.print_elements()
    pygame.display.update()
    clock.tick(FPS)
