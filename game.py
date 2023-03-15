import sys
import pygame as pg
import neat
import os

from bird import Bird
from pipe import Pipe
from base import Base
from button import Button

pg.init()

# Determine path to configuration file. This path manipulation is
# here so that the script will run successfully regardless of the
# current working directory.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')

WIN_WIDTH, WIN_HEIGHT = 600, 700
SCREEN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bg.png")))
DRAW_LINES = False
pg.display.set_caption("Flappy Bird")

STAT_FONT = pg.font.SysFont("comicsans", 50)
MENU_FONT = pg.font.SysFont("comicsans", 35)
GEN = 0


def draw_window(birds, pipes, base, score, highscore = None, gen=None, pipe_ind=None, ai_button=None, player_button=None):
    """
        Draws everything we need on to the screen
        i.e. Flappy, pipes, base, score, etc

    """
    # blits background and makes it fits to window
    SCREEN.blit(pg.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT)), (0, 0))

    for pipe in pipes:
        pipe.draw(SCREEN)

    # checks if birds is iterable, used for Bots
    if hasattr(birds, '__iter__'):
        for bird in birds:
            # draw lines from bird to pipe
            if DRAW_LINES:
                try:
                    pg.draw.line(SCREEN, (255, 0, 0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height(
                    )/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                    pg.draw.line(SCREEN, (255, 0, 0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height(
                    )/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
                except:
                    pass
            # draw AI birds
            bird.draw(SCREEN)
    else:
        # draws player bird
        birds.draw(SCREEN)

    if gen is not None:

        gen_label = STAT_FONT.render("Gens: " + str(gen-1), 1, (255, 255, 255))
        SCREEN.blit(gen_label, (10, 10))
        # alive
        alive_label = STAT_FONT.render(
            "Alive: " + str(len(birds)), 1, (255, 255, 255))
        SCREEN.blit(alive_label, (10, 50))

    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    SCREEN.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    base.draw(SCREEN)

    if highscore is not None:
        hscore_label = STAT_FONT.render("Highscore: " + str(highscore), 1, (255, 255, 255))
        SCREEN.blit(hscore_label, (0, 10))

    if ai_button is not None:
        ai_button.draw(SCREEN)
        player_button.draw(SCREEN)

    pg.display.update()


def ai_controlled(genomes, config):
    global GEN
    GEN += 1
    networks = []  # track neural network that controls each bird
    genome = []  # track genome for each bird for their fitness
    birds = []

    for _, g in genomes:
        g.fitness = 0
        # set up neural network for each bird, give it a genome and config file to know how to set up
        network = neat.nn.FeedForwardNetwork.create(g, config)
        networks.append(network)
        birds.append(Bird(130, 200))
        # track fitness and change it when desired
        genome.append(g)

    base = Base(630)
    pipes = [Pipe(600)]
    clock = pg.time.Clock()

    score = 0
    paused = False
    run = True

    while run:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        paused = not paused
                        while paused:
                            paused = pause(runs, config_path)

        # there will always be at most 2 sets of pipes on the screen at all given times
        # set pipe index to 0, this determines which set of pipes the birds will focus on
        pipe_index = 0
        if len(birds) > 0:
            # if a bird moves past the first set of pipes focus on the next set
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_index = 1
        else:
            # if there are no more birds in current gen end it
            run = False
            break

        # pass values for bird neural network
        for x, bird in enumerate(birds):
            # encourage bird to keep moving forward every frame
            genome[x].fitness += 0.1
            bird.move()

            output = networks[x].activate((bird.y, abs(
                bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5:
                bird.jump()

        base.move()
        add_pipe = False
        remove = []

        # check if every bird collides with every pipe
        for pipe in pipes:
            pipe.move()

            for x, bird in enumerate(birds):
                if pipe.collide(bird):

                    # every time a bird hits a pipe give it a penalty
                    # that way we dont favor birds who made it far but by ramming into the pipe
                    # this encourages birds to go thru the pipe
                    genome[birds.index(bird)].fitness -= 1

                    # remove the bird as well as its neural network and its genome associated w/ it

                    genome.pop(birds.index(bird))
                    networks.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            # by looking at the pipes x pos and its width
            # if pipe is completely off the screen, then remove it
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            # check if we have passed the pipe and if so generate a new pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # any bird that successfully goes thru the gap between pipes will be rewarded
            for g in genome:
                g.fitness += 5
            pipes.append(Pipe(600))

        for rem in remove:
            pipes.remove(rem)

        # if a bird hits the ground remove it entirely or flies to far up the screen
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 630 or bird.y < 0:
                networks.pop(x)
                genome.pop(x)
                birds.pop(birds.index(bird))

        draw_window(birds, pipes, base, score = score, gen=GEN, pipe_ind= pipe_index)


def player_controlled():
    """
        Classic game mode where the player sees how far they can go in a single run before resetting
        no gimmicks whatsoever
    """

    try:
        with open("highscore.txt", "r") as file:
            hscore = int(file.read())

    except FileNotFoundError:
        with open("highscore.txt", "w") as file:
            hscore = 0
            file.write(str(hscore))
    base = Base(630)
    pipes = [Pipe(600)]
    clock = pg.time.Clock()
    player = Bird(130, 200)
    score = 0

    paused = False

    run = True
    while run:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    player.jump()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    paused = not paused
                    while paused:
                        paused = pause(player_controlled)

        player.move()
        base.move()
        add_pipe = False
        remove = []

        # check if every bird collides with every pipe
        for pipe in pipes:
            pipe.move()
            if pipe.collide(player):
                player_controlled()

            # by looking at the pipes x pos and its width
            # if pipe is completely off the screen, then remove it
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            # check if we have passed the pipe and if so generate a new pipe
            if not pipe.passed and pipe.x < player.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for rem in remove:
            pipes.remove(rem)

        # if a bird hits the ground remove it entirely or flies to far up the screen
        if player.y + player.img.get_height() >= 630 or player.y < 0:
            player_controlled()

        if score > hscore:
            hscore = score
            with open("highscore.txt", "w") as file:
                file.write(str(hscore))

        draw_window(player, pipes, base, score = score, highscore = hscore)
        pg.display.update()


def pause(func, config=None):
    """
        Pause menu for the game
        Can be used in both Classic and Bots, activated by pressing 'p' in either mode
        3 functionalities: unpause, restart and return to main menu
            Press 'p' again to unpause
            Press 'r' to restart the run
            Press 'm' to return to the main menu

    Args:
        func (function): game mode to be executed when restarting respective game mode
        config (_type_, optional): used to restart Bots instance. Defaults to None.

    """
    run = True
    while run:
        # Text for functionalities
        unpause = STAT_FONT.render("Press p to unpause ", 1, (0, 0, 0))
        SCREEN.blit(unpause, (100, 200))

        main_menu = MENU_FONT.render("Press m to return to the menu ", 1, (0, 0, 0))
        SCREEN.blit(main_menu, (75, 300))

        restart = STAT_FONT.render("Press r to restart ", 1, (0, 0, 0))
        SCREEN.blit(restart, (100, 375))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    return False
                if event.key == pg.K_m:
                    menu()
                if event.key == pg.K_r:
                    if config == None:
                        func()
                    else:
                        func(config)

        pg.display.update()

    return True


def menu():
    """
        Main menu for the game
        Showcases Flappy in its flying animation and 2 buttons:
            Classic: Player controlled, resets upon hitting a pipe or the ground
            Bots: Watch AI quickly figure out how to play the game and see how far they go
    """
    base = Base(630)
    pipes = [Pipe(600)]
    player = Bird(130, 200)
    score = 0
    clock = pg.time.Clock()
    while True:
        clock.tick(30)

        MENU_MOUSE_POS = pg.mouse.get_pos()

        AI_BUTTON = Button(500, "Bots", (0, 0, 255))
        PLAYER_BUTTON = Button(300, "Classic", (255, 0, 0))

        draw_window(player, pipes, base, score,
                    ai_button=AI_BUTTON, player_button=PLAYER_BUTTON)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if AI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    runs(config_path)
                if PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_controlled()
        pg.display.update()


def runs(config_path):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(ai_controlled, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    menu()
