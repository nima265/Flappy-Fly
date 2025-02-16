import pygame
import random
import os
import neat
import time

pygame.font.init()  # Initialize font

# Window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
GROUND_LEVEL = 730

# Fonts
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 70)

# Display settings
DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
ICON = pygame.image.load(os.path.join("images", "title.png"))
pygame.display.set_caption("Flappy Fly")
pygame.display.set_icon(ICON)

# Load images
FLY_SWEEPER_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "Fly_Sweeper.png")).convert_alpha())
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "bg.png")).convert_alpha(), (600, 900))
FLY_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "fly.png")).convert_alpha())
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")).convert_alpha())
TITLE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "title.png")).convert_alpha(), (250, 250))
PLAY_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "play_button.png")).convert_alpha(), (120, 120))
PLAY_YOURSELF_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "play_button.png")).convert_alpha(), (120, 120))
PLAY_AI_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "play_button.png")).convert_alpha(), (120, 120))

generation = 0

class Fly:
    """
    Class representing the Fly
    """
    MAX_TILT = 25
    IMAGE = FLY_IMAGE
    ROTATION_VELOCITY = 20

    def __init__(self, x, y):
        """
        Initialize the fly
        :param x: starting x position
        :param y: starting y position
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image = self.IMAGE

    def jump(self):
        """
        Make the fly jump
        """
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        Move the fly
        """
        self.tick_count += 1
        displacement = self.velocity * self.tick_count + 0.5 * 3 * self.tick_count ** 2

        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2

        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_TILT:
                self.tilt = self.MAX_TILT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, window):
        """
        Draw the fly
        :param window: Pygame window or surface
        """
        blit_rotate_center(window, self.image, (self.x, self.y), self.tilt)

    def get_mask(self):
        """
        Get the mask for the current image of the fly
        """
        return pygame.mask.from_surface(self.image)


class FlySweeper:
    """
    Class representing a fly sweeper
    """
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        """
        Initialize the fly sweeper
        :param x: x position
        """
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.FLY_SWEEPER_TOP = pygame.transform.flip(FLY_SWEEPER_IMAGE, False, True)
        self.FLY_SWEEPER_BOTTOM = FLY_SWEEPER_IMAGE
        self.passed = False
        self.set_height()

    def set_height(self):
        """
        Set the height of the fly sweeper
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.FLY_SWEEPER_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        Move the fly sweeper
        """
        self.x -= self.VELOCITY

    def draw(self, window):
        """
        Draw the fly sweeper
        :param window: Pygame window or surface
        """
        window.blit(self.FLY_SWEEPER_TOP, (self.x, self.top))
        window.blit(self.FLY_SWEEPER_BOTTOM, (self.x, self.bottom))

    def collide(self, fly, window):
        """
        Check if the fly sweeper collides with the fly
        :param fly: Fly object
        :param window: Pygame window or surface
        :return: Boolean
        """
        fly_mask = fly.get_mask()
        top_mask = pygame.mask.from_surface(self.FLY_SWEEPER_TOP)
        bottom_mask = pygame.mask.from_surface(self.FLY_SWEEPER_BOTTOM)
        top_offset = (self.x - fly.x, self.top - round(fly.y))
        bottom_offset = (self.x - fly.x, self.bottom - round(fly.y))

        b_point = fly_mask.overlap(bottom_mask, bottom_offset)
        t_point = fly_mask.overlap(top_mask, top_offset)

        return b_point or t_point


class Ground:
    """
    Class representing the moving ground
    """
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        """
        Initialize the ground
        :param y: y position
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        Move the ground
        """
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        """
        Draw the ground
        :param window: Pygame window or surface
        """
        window.blit(self.IMAGE, (self.x1, self.y))
        window.blit(self.IMAGE, (self.x2, self.y))


def blit_rotate_center(surface, image, topleft, angle):
    """
    Rotate an image and blit it to the window
    :param surface: Pygame surface
    :param image: Image surface to rotate
    :param topleft: Top left position of the image
    :param angle: Angle to rotate
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surface.blit(rotated_image, new_rect.topleft)


def draw_window(window, flies, fly_sweepers, ground, score, generation, fly_sweeper_index):
    """
    Draw the game window
    :param window: Pygame window surface
    :param flies: List of fly objects
    :param fly_sweepers: List of fly sweeper objects
    :param ground: Ground object
    :param score: Current score
    :param generation: Current generation
    :param fly_sweeper_index: Index of the closest fly sweeper
    """
    if generation == 0:
        generation = 1

    window.blit(BACKGROUND_IMAGE, (0, 0))

    for fly_sweeper in fly_sweepers:
        fly_sweeper.draw(window)

    ground.draw(window)

    for fly in flies:
        fly.draw(window)

    score_label = SCORE_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    window.blit(score_label, (WINDOW_WIDTH - score_label.get_width() - 15, 10))

    generation_label = SCORE_FONT.render(f"Gens: {generation - 1}", 1, (255, 255, 255))
    window.blit(generation_label, (10, 10))

    alive_label = SCORE_FONT.render(f"Alive: {len(flies)}", 1, (255, 255, 255))
    window.blit(alive_label, (10, 50))

    pygame.display.update()


def evaluate_genomes(genomes, config):
    """
    Evaluate the genomes
    :param genomes: List of genomes
    :param config: NEAT configuration
    """
    global DISPLAY, generation
    generation += 1

    networks = []
    flies = []
    genome_list = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        flies.append(Fly(230, 350))
        genome_list.append(genome)

    ground = Ground(GROUND_LEVEL)
    fly_sweepers = [FlySweeper(700)]
    score = 0

    clock = pygame.time.Clock()
    run = True

    while run and len(flies) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        fly_sweeper_index = 0
        if len(flies) > 0 and len(fly_sweepers) > 1 and flies[0].x > fly_sweepers[0].x + fly_sweepers[0].FLY_SWEEPER_TOP.get_width():
            fly_sweeper_index = 1

        for i, fly in enumerate(flies):
            genome_list[i].fitness += 0.1
            fly.move()

            output = networks[i].activate((fly.y, abs(fly.y - fly_sweepers[fly_sweeper_index].height), abs(fly.y - fly_sweepers[fly_sweeper_index].bottom)))

            if output[0] > 0.5:
                fly.jump()

        ground.move()

        remove_fly_sweepers = []
        add_fly_sweeper = False

        for fly_sweeper in fly_sweepers:
            fly_sweeper.move()

            for fly in flies:
                if fly_sweeper.collide(fly, DISPLAY):
                    genome_list[flies.index(fly)].fitness -= 1
                    networks.pop(flies.index(fly))
                    genome_list.pop(flies.index(fly))
                    flies.pop(flies.index(fly))

            if fly_sweeper.x + fly_sweeper.FLY_SWEEPER_TOP.get_width() < 0:
                remove_fly_sweepers.append(fly_sweeper)

            if not fly_sweeper.passed and fly_sweeper.x < fly.x:
                fly_sweeper.passed = True
                add_fly_sweeper = True

        if add_fly_sweeper:
            score += 1
            for genome in genome_list:
                genome.fitness += 5
            fly_sweepers.append(FlySweeper(WINDOW_WIDTH))

        for fly_sweeper in remove_fly_sweepers:
            fly_sweepers.remove(fly_sweeper)

        for fly in flies:
            if fly.y + fly.image.get_height() - 10 >= GROUND_LEVEL or fly.y < -50:
                networks.pop(flies.index(fly))
                genome_list.pop(flies.index(fly))
                flies.pop(flies.index(fly))

        draw_window(DISPLAY, flies, fly_sweepers, ground, score, generation, fly_sweeper_index)


def run_neat(config_file):
    """
    Run the NEAT algorithm to train a neural network to play Flappy Bird
    :param config_file: Path to the configuration file
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(evaluate_genomes, 50)

    print(f'\nBest genome:\n{winner}')


def play_game():
    """
    Function to play the game manually
    """
    fly = Fly(230, 350)
    ground = Ground(GROUND_LEVEL)
    fly_sweepers = [FlySweeper(700)]
    score = 0

    clock = pygame.time.Clock()
    run = True

    # Countdown before starting the game
    for i in range(3, 0, -1):
        DISPLAY.blit(BACKGROUND_IMAGE, (0, 0))
        countdown_label = GAME_OVER_FONT.render(str(i), 1, (255, 255, 255))
        DISPLAY.blit(countdown_label, (WINDOW_WIDTH // 2 - countdown_label.get_width() // 2, WINDOW_HEIGHT // 2 - countdown_label.get_height() // 2))
        pygame.display.update()
        time.sleep(1)

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fly.jump()

        fly.move()
        ground.move()

        add_fly_sweeper = False
        remove_fly_sweepers = []

        for fly_sweeper in fly_sweepers:
            fly_sweeper.move()
            if fly_sweeper.collide(fly, DISPLAY):
                run = False

            if fly_sweeper.x + fly_sweeper.FLY_SWEEPER_TOP.get_width() < 0:
                remove_fly_sweepers.append(fly_sweeper)

            if not fly_sweeper.passed and fly_sweeper.x < fly.x:
                fly_sweeper.passed = True
                add_fly_sweeper = True

        if add_fly_sweeper:
            score += 1
            fly_sweepers.append(FlySweeper(WINDOW_WIDTH))

        for fly_sweeper in remove_fly_sweepers:
            fly_sweepers.remove(fly_sweeper)

        if fly.y + fly.image.get_height() - 10 >= GROUND_LEVEL or fly.y < -50:
            run = False

        draw_window(DISPLAY, [fly], fly_sweepers, ground, score, 0, 0)

    # Display "YOU LOST" message
    DISPLAY.blit(BACKGROUND_IMAGE, (0, 0))
    lost_label = GAME_OVER_FONT.render("YOU LOST", 1, (255, 0, 0))
    DISPLAY.blit(lost_label, (WINDOW_WIDTH // 2 - lost_label.get_width() // 2, WINDOW_HEIGHT // 2 - lost_label.get_height() // 2))
    pygame.display.update()
    time.sleep(5)
    
    # Return to the main menu
    show_menu()
    show_mode_selection()


def show_menu():
    """
    Display the game menu with a title and play button
    """
    menu_run = True
    while menu_run:
        DISPLAY.blit(BACKGROUND_IMAGE, (0, 0))
        DISPLAY.blit(TITLE_IMAGE, (WINDOW_WIDTH // 2 - TITLE_IMAGE.get_width() // 2, 100))
        play_button_rect = DISPLAY.blit(PLAY_BUTTON_IMAGE, (WINDOW_WIDTH // 2 - PLAY_BUTTON_IMAGE.get_width() // 2, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_run = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    menu_run = False

        pygame.display.update()


def show_mode_selection():
    """
    Display the mode selection menu with two buttons: Play Yourself and Play AI
    """
    mode_selection_run = True
    while mode_selection_run:
        DISPLAY.blit(BACKGROUND_IMAGE, (0, 0))
        DISPLAY.blit(TITLE_IMAGE, (WINDOW_WIDTH // 2 - TITLE_IMAGE.get_width() // 2, 20))
        
        # Play Yourself button and label
        play_yourself_label = SCORE_FONT.render("Play Yourself", 1, (255, 255, 255))
        DISPLAY.blit(play_yourself_label, (WINDOW_WIDTH // 2 - play_yourself_label.get_width() // 2 - 140, 290))
        play_yourself_button_rect = DISPLAY.blit(PLAY_YOURSELF_BUTTON_IMAGE, (WINDOW_WIDTH // 2 - PLAY_YOURSELF_BUTTON_IMAGE.get_width() // 2 - 150, 350))
        
        # Play AI button and label
        play_ai_label = SCORE_FONT.render("Play AI", 1, (255, 255, 255))
        DISPLAY.blit(play_ai_label, (WINDOW_WIDTH // 2 - play_ai_label.get_width() // 2 + 160, 290))
        play_ai_button_rect = DISPLAY.blit(PLAY_AI_BUTTON_IMAGE, (WINDOW_WIDTH // 2 - PLAY_AI_BUTTON_IMAGE.get_width() // 2 + 150, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode_selection_run = False
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_yourself_button_rect.collidepoint(event.pos):
                    mode_selection_run = False
                    play_game()
                elif play_ai_button_rect.collidepoint(event.pos):
                    mode_selection_run = False
                    local_directory = os.path.dirname(__file__)
                    config_path = os.path.join(local_directory, 'Flappy_Fly_Config.txt')
                    run_neat(config_path)

        pygame.display.update()


if __name__ == '__main__':
    show_menu()  # Show the menu before starting the game
    show_mode_selection()  # Show the mode selection menu