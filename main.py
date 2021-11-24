"""
Title: Electric Field Hockey

Citations:
    1. Python (https://www.python.org/) - Python is a dynamic, high-level, and object-oriented programming language
    2. Math (https://docs.python.org/3/library/math.html) - the math library is a built-in python library used for math functions
    3. Pygame (pygame.org) - the pygame library is an external python library used for 2D graphics

Collaborators: None. This program was developed alone, except for the libraries and tools used (as cited above).

Idea Credit:
    - Electric Field Hockey was conceived by Dr. Ruth Chabay.
    - I was introduced to this game in a PHET simulation (https://phet.colorado.edu/sims/cheerpj/electric-hockey/latest/electric-hockey.html?simulation=electric-hockey).
    - Note: While the idea is not my own, this implementation is entirely developed by me (apart from the libraries and tools cited above).

System Requirements:
    1. Python (version 3.7.7)
    2. pygame (version 2.0.0)
"""

# ----------------IMPORTING DEPENDENCIES----------------

# importing the math library to provide access to a multitude of mathematical functions
import math
# importing the pygame library to provide access to 2D graphics
import pygame
# importing the pygame.locals sub-module for effective event handling
from pygame.locals import *


# ----------------ABSTRACTIONS----------------


# show_text: a function to render text on the screen
# params:
#   - text (str): the text that needs to be rendered on the screen
#   - x (int): the x position of the text
#   - y (int): the y position of the text
#   - size (int): font size (defaults to 30)
#   - color (tuple): RGB color value (defaults to (255, 255, 255))
# returns -> None
def show_text(text: str, x: int, y: int, size: int = 30, color: tuple = (255, 255, 255)) -> None:
    font = pygame.font.SysFont('times', size)
    screen.blit(font.render(text, False, color), [x, y])


# Obstacle: a class to handle rectangular obstacles
# superclass: object
# subclass: Button
class Obstacle:

    # constructor
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple):
        self.position = [x, y]
        self.dimensions = [w, h]
        self.color = color

    # draw: a function to render the Obstacle on the screen
    # params:
    #   - self (Obstacle)
    # returns -> None
    def draw(self) -> None:
        pygame.draw.rect(screen, self.color, self.position + self.dimensions)


# Button: a class to handle rectangular buttons
# superclass: Obstacle
# subclass: none
class Button(Obstacle):

    # constructor
    def __init__(self, text: str, x: int, y: int, color: tuple):
        super().__init__(x, y, len(text) * 25, 50, color)
        self.text = text

    # draw: a function to render the Button on the screen
    # params:
    #   - self (Button)
    # returns -> None
    def draw(self) -> None:
        super().draw()
        show_text(self.text, self.position[0] + 10, self.position[1] + 10)

    # detect_click: a function to detect mouse clicks on the Button
    # params:
    #   - self (Button)
    #   - click_position (tuple): the coordinates of the mouse click
    # returns -> bool: a boolean value indicating if the Button is clicked
    def detect_click(self, click_position: tuple) -> bool:
        return ((self.position[0] <= click_position[0] <= self.position[0] + self.dimensions[0])
                and (self.position[1] <= click_position[1] <= self.position[1] + self.dimensions[1]))


# Slider: a class to handle sliders
# superclass: object
# subclass: none
class Slider:

    # constructor
    def __init__(self, label: str, position: list, domain: range, width: int = 100):
        self.label = label
        self.position = position
        self.width = width
        self.current_position = self.position[0]
        self.domain = domain
        self.clicked = False
        self.radius = 10

    # get_val: a function to extract the numerical value of the Slider
    # params:
    #   - self (Slider)
    # returns -> int: an integer value of the Slider's position relative to its domain
    def get_val(self) -> int:
        return round((self.domain.stop - self.domain.start) * (
                self.current_position - self.position[0]) / self.width) + self.domain.start

    # draw: a function to render a Slider on the screen
    # params:
    #   - self (Slider)
    # returns -> None
    def draw(self) -> None:
        pygame.draw.line(screen, (0, 0, 0), self.position, [self.position[0] + self.width, self.position[1]], 2)
        pygame.draw.circle(screen, (0, 0, 0), [self.current_position, self.position[1]], self.radius)
        show_text(str(self.domain.start), self.position[0], self.position[1] - 10, color=(0, 0, 0))
        show_text(str(self.domain.stop), self.position[0] + self.width, self.position[1] - 10, color=(0, 0, 0))
        show_text(self.label + ': ' + str(self.get_val()), self.position[0], self.position[1] + 30, color=(0, 0, 0))

    # detect_click: a function to detect mouse clicks on the Slider
    # params:
    #   - self (Slider)
    #   - click_position (tuple): the coordinates of the mouse click
    # returns -> bool: a boolean value indicating if the Slider is clicked
    def detect_click(self, click_position: tuple) -> bool:
        return ((self.current_position - self.radius <= click_position[0] <= self.current_position + self.radius) and (
                self.position[1] - self.radius <= click_position[1] <= self.position[1] + self.radius))


# StationaryCharge: a class to handle stationary charged particles
# superclass: object
# subclass: DynamicCharge
class StationaryCharge:

    # constructor
    def __init__(self, charge_val: int, position: list):
        self.position = position
        self.charge = charge_val
        self.mass = 1
        self.radius = 10
        self.clicked = True
        if self.charge > 0:
            self.color = (255, 0, 0)
        elif self.charge < 0:
            self.color = (0, 0, 255)

    # draw: a function to render the StationaryCharge on the screen
    # params:
    #   - self (StationaryCharge)
    # returns -> None
    def draw(self) -> None:
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        if self.charge > 0:
            show_text('+', self.position[0] - self.radius * 3 // 4, self.position[1] - self.radius * 3 // 2)
        elif self.charge < 0:
            show_text('-', self.position[0] - self.radius * 3 // 4, self.position[1] - self.radius * 3 // 2)

    # detect_click: a function to detect mouse clicks on the StationaryCharge
    # params
    #   - self (StationaryCharge)
    #   - click_position (tuple): the coordinates of the mouse click
    # returns -> bool: a boolean indicating if the StationaryCharge is clicked
    def detect_click(self, click_position: tuple) -> bool:
        return ((self.position[0] - self.radius <= click_position[0] <= self.position[0] + self.radius)
                and (self.position[1] - self.radius <= click_position[1] <= self.position[1] + self.radius))


# DynamicCharge: a class to handle dynamic charged particles
# superclass: StationaryCharge
# subclass: none
class DynamicCharge(StationaryCharge):

    # constructor
    def __init__(self):
        super().__init__(1, [50, SCREEN_SIZE[1] // 2])
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.color = (0, 0, 0)

    # move: a function to handle the kinematic motion of the DynamicCharge
    # params:
    #   - self (DynamicCharge)
    #   - force (list): a list containing the instantaneous force on the DynamicCharge
    # returns -> None
    def move(self, force: list) -> None:
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        self.acceleration[0] = force[0] / self.mass
        self.acceleration[1] = force[1] / self.mass

    # detect_collision: a function to detect collisions against Obstacles
    # params:
    #   - self (Dynamic Charge)
    #   - obstacle (Obstacle)
    # returns -> bool: a boolean indicating if the DynamicCharge collides with the specified obstacle
    def detect_collision(self, obstacle: Obstacle) -> bool:
        return ((self.position[0] + self.radius >= obstacle.position[0] and self.position[0] - self.radius <=
                 obstacle.position[0] + obstacle.dimensions[0]) and
                (self.position[1] + self.radius >= obstacle.position[1] and self.position[1] - self.radius <=
                 obstacle.position[1] + obstacle.dimensions[1]))

    # reset: a function to reset all kinematic vectors
    # params:
    #   - self (DynamicCharge)
    # returns -> None
    def reset(self) -> None:
        self.position = [50, SCREEN_SIZE[1] // 2]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]


# hyp_calc: a function to calculate the hypotenuse of a vector
# params:
#   - vector1 (list): the first vector with [x, y] components
#   - vector2 (list): the second vector with [x, y] components
# returns -> float: the total length of the hypotenuse connecting vector1 and vector2
def hyp_calc(vector1: list, vector2: list) -> float:
    return ((vector1[0] - vector2[0]) ** 2 + (vector1[1] - vector2[1]) ** 2) ** 0.5


# angle_calc: a function to calculate the angle (with respect to the horizontal) formed by two vectors
# params:
#   - vector1 (list): the first vector with [x, y] components
#   - vector2 (list): the second vector with [x, y] components
# returns -> float: the angle enclosed by vector1 and vector2
def angle_calc(vector1: list, vector2: list) -> float:
    return math.asin((vector1[1] - vector2[1]) / hyp_calc(vector1, vector2))


# electrostatic_force_calc: a function to calculate the electrostatic force between two StationaryCharge (or its subclass DynamicCharge) objects
# params:
#   - particle1 (StationaryCharge): the first StationaryCharge
#   - particle2 (StationaryCharge): the second StationaryCharge
# returns -> float: the magnitude of electrostatic force between the two StationaryCharge (or DynamicCharge) objects
def electrostatic_force_calc(particle1: StationaryCharge, particle2: StationaryCharge) -> float:
    k = 20
    proximity = 4
    charge_squared = k * abs(particle1.charge) * abs(particle2.charge)
    distance = hyp_calc(particle1.position, particle2.position)
    if distance < proximity * particle1.radius:
        return charge_squared / ((proximity * particle1.radius) ** 2)
    else:
        return charge_squared / (distance ** 2)


# gravitational_force_calc: a function to calculate the gravitational force between two StationaryCharge (or its subclass DynamicCharge) objects
#   - particle1 (StationaryCharge): the first StationaryCharge
#   - particle2 (StationaryCharge): the second StationaryCharge
# returns -> float: the magnitude of gravitational force between the two StationaryCharge (or DynamicCharge) objects
def gravitational_force_calc(particle1: StationaryCharge, particle2: StationaryCharge) -> float:
    g = 0.02
    proximity = 4
    mass_squared = g * particle1.mass * particle2.mass
    distance = hyp_calc(particle1.position, particle2.position)
    if distance < proximity * particle1.radius:
        return mass_squared / ((proximity * particle1.radius) ** 2)
    else:
        return mass_squared / (distance ** 2)


# net_force_calc: a function to calculate the net force on primary_charge
# params:
#   - force_type (str): specifies what type of force is being calculated (gravitational or electrostatic)
# returns -> list: represents the net force vector
def net_force_calc(force_type: str) -> list:
    total = [0, 0]
    for charge in charges:
        angle = angle_calc(primary_charge.position, charge.position)
        attraction = False
        magnitude = 0
        if force_type == 'gravitational':
            magnitude = gravitational_force_calc(primary_charge, charge)
            attraction = True
        elif force_type == 'electrostatic':
            magnitude = electrostatic_force_calc(primary_charge, charge)
            attraction = not ((primary_charge.charge > 0 and charge.charge > 0) or (primary_charge.charge < 0 and charge.charge < 0))
        point = primary_charge.position.copy()
        if attraction:
            if primary_charge.position[0] > charge.position[0]:
                total[0] -= abs(math.cos(angle) * magnitude)
                point[0] -= 25000 * abs(math.cos(angle) * magnitude)
            else:
                total[0] += abs(math.cos(angle) * magnitude)
                point[0] += 25000 * abs(math.cos(angle) * magnitude)
            if primary_charge.position[1] > charge.position[1]:
                total[1] -= abs(math.sin(angle) * magnitude)
                point[1] -= 25000 * abs(math.sin(angle) * magnitude)
            else:
                total[1] += abs(math.sin(angle) * magnitude)
                point[1] += 25000 * abs(math.sin(angle) * magnitude)
        else:
            if primary_charge.position[0] > charge.position[0]:
                total[0] += abs(math.cos(angle) * magnitude)
                point[0] += 25000 * abs(math.cos(angle) * magnitude)
            else:
                total[0] -= abs(math.cos(angle) * magnitude)
                point[0] -= 25000 * abs(math.cos(angle) * magnitude)
            if primary_charge.position[1] > charge.position[1]:
                total[1] += abs(math.sin(angle) * magnitude)
                point[1] += 25000 * abs(math.sin(angle) * magnitude)
            else:
                total[1] -= abs(math.sin(angle) * magnitude)
                point[1] -= 25000 * abs(math.sin(angle) * magnitude)
        pygame.draw.line(screen, charge.color, primary_charge.position, point, 2)
    return total


# ----------------VARIABLES AND SETUP----------------

# graphics variables
SCREEN_SIZE = [1200, 600]   # contains the screen dimensions
pygame.init()   # graphics initialization
screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1] + 120))    # contains the pygame window's object
pygame.display.set_caption('electric field hockey')     # captions the app

# UI object variables
play_button = Button('play', SCREEN_SIZE[0] // 2 - 70, 300, (0, 0, 255))    # contains the play Button on the home screen
quit_button = Button('quit', SCREEN_SIZE[0] // 2 - 70, 500, (255, 0, 0))    # contains the quit Button on the home screen
add_positive_charges = Button('+', 50, SCREEN_SIZE[1] + 50, (255, 0, 0))    # Button to add positive charges on the game screen
add_negative_charge = Button('-', 100, SCREEN_SIZE[1] + 50, (0, 0, 255))    # Button to add negative charges on the game screen
run_button = Button('run', 650, SCREEN_SIZE[1] + 50, (0, 0, 0))     # Button to run the simulation on the game screen
reset_button = Button('reset', 750, SCREEN_SIZE[1] + 50, (0, 0, 0))     # Button to reset the simulation on the game screen
home_button = Button('home', 1050, SCREEN_SIZE[1] + 50, (0, 0, 0))    # Button to return to the home screen
clear_button = Button('clear', 900, SCREEN_SIZE[1] + 50, (0, 0, 0))     # Button to clear all charges on the game screen
level_slider = Slider('level', [SCREEN_SIZE[0] // 2 - 75, 200], range(0, 3))    # Slider to set the level on the home screen
mass_slider = Slider('mass', [315, SCREEN_SIZE[1] + 50], range(1, 100, 1))    # Slider to control the primary_charge mass attribute
charge_slider = Slider('charge', [500, SCREEN_SIZE[1] + 50], range(-25, 25, 1))     # Slider to control the primary_charge charge attribute

# game variables
play = False    # boolean representing if the user is playing (or on the home screen)
run = False     # boolean representing if the user is running the simulation
charges = []    # list to store StationaryCharge objects
primary_charge = DynamicCharge()    # stores the main game object of type DynamicCharge
goal = Obstacle(SCREEN_SIZE[0] - 50, SCREEN_SIZE[1] // 2 - 30, 20, 60, (150, 0, 150))   # contains the goal on the game screen
g_force = []    # stores the net gravitational force vector to calculate the force on the primary_charge
e_force = []    # stores the net electrostatic force vector to calculate the force on the primary_charge
# contains the obstacles at each level of the game
levels = [
    [],
    [Obstacle(300, SCREEN_SIZE[1] // 2 - 75, 20, 150, (0, 0, 0))],
    [Obstacle(SCREEN_SIZE[0] // 3, SCREEN_SIZE[1] // 4 - 75, 20, 150, (0, 0, 0)),
     Obstacle(2 * SCREEN_SIZE[0] // 3, SCREEN_SIZE[1] // 2 - 75, 20, 150, (0, 0, 0))],
    [Obstacle(SCREEN_SIZE[0] // 5, SCREEN_SIZE[1] // 3, 20, 2 * SCREEN_SIZE[1] // 3, (0, 0, 0)),
     Obstacle(3 * SCREEN_SIZE[0] // 7, 0, 20, SCREEN_SIZE[1] // 2, (0, 0, 0)),
     Obstacle(3 * SCREEN_SIZE[0] // 4, SCREEN_SIZE[1] // 3, 20, 2 * SCREEN_SIZE[1] // 3, (0, 0, 0))]
]
active_level = 0    # represents the current level


# ----------------GAME LOOP----------------
while True:

    screen.fill((125, 125, 125))

    # home_screen
    if not play:

        # graphics rendering
        play_button.draw()
        quit_button.draw()
        level_slider.draw()
        show_text('Objective: Get the charge into the goal. Avoid the obstacles.', 150, 50, color=(0, 0, 0))
        show_text('Pro Tip: Opposite charges attract, while like charges repel.', 150, 100, color=(0, 0, 0))

        # event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if play_button.detect_click(event.pos):
                    active_level = level_slider.get_val()
                    play = True
                elif quit_button.detect_click(event.pos):
                    pygame.quit()
                    exit()
                elif level_slider.detect_click(event.pos):
                    level_slider.clicked = True
            elif event.type == MOUSEBUTTONUP:
                level_slider.clicked = False
            elif event.type == MOUSEMOTION:
                if level_slider.clicked and level_slider.position[0] <= event.pos[0] <= level_slider.position[0] + level_slider.width:
                    level_slider.current_position = event.pos[0]

    # game screen
    else:

        # graphics rendering
        pygame.draw.line(screen, (0, 0, 0), (0, SCREEN_SIZE[1]), SCREEN_SIZE, 1)
        add_positive_charges.draw()
        add_negative_charge.draw()
        home_button.draw()
        run_button.draw()
        reset_button.draw()
        mass_slider.draw()
        charge_slider.draw()
        clear_button.draw()
        show_text('charges: ' + str(len(charges)), 150, SCREEN_SIZE[1] + 50, color=(0, 0, 0))

        for obs in levels[active_level]:
            obs.draw()
            if primary_charge.detect_collision(obs):
                run = False
        goal.draw()

        for charge in charges:
            charge.draw()
            if charge.position[1] > SCREEN_SIZE[1] and not charge.clicked:
                charges.remove(charge)

        if run:
            g_force = net_force_calc(force_type='gravitational')
            e_force = net_force_calc(force_type='electrostatic')
            primary_charge.move([g_force[0] + e_force[0], g_force[1] + e_force[1]])
        else:
            for obs in levels[active_level]:
                if primary_charge.detect_collision(obs):
                    show_text('CRASHED!', 300, 200, color=(150, 0, 150), size=150)
            if primary_charge.detect_collision(goal):
                show_text('GOAL!', 300, 200, color=(150, 0, 150), size=150)

        primary_charge.draw()
        primary_charge.mass = mass_slider.get_val()
        primary_charge.charge = charge_slider.get_val()

        if primary_charge.detect_collision(goal):
            run = False

        # event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                for charge in charges:
                    if charge.detect_click(event.pos):
                        charge.clicked = True
                if add_positive_charges.detect_click(event.pos):
                    charges.append(StationaryCharge(1, list(event.pos).copy()))
                if add_negative_charge.detect_click(event.pos):
                    charges.append(StationaryCharge(-1, list(event.pos).copy()))
                if run_button.detect_click(event.pos):
                    run = True
                if mass_slider.detect_click(event.pos):
                    mass_slider.clicked = True
                if charge_slider.detect_click(event.pos):
                    charge_slider.clicked = True
                if home_button.detect_click(event.pos):
                    primary_charge.reset()
                    run = False
                    play = False
                if reset_button.detect_click(event.pos):
                    primary_charge.reset()
                    run = False
                if clear_button.detect_click(event.pos):
                    charges = []
            elif event.type == MOUSEBUTTONUP:
                for charge in charges:
                    charge.clicked = False
                mass_slider.clicked = False
                charge_slider.clicked = False
            elif event.type == MOUSEMOTION:
                for charge in charges:
                    if charge.clicked:
                        charge.position = list(event.pos).copy()
                if mass_slider.clicked and mass_slider.position[0] <= event.pos[0] <= mass_slider.position[0] + mass_slider.width:
                    mass_slider.current_position = event.pos[0]
                if charge_slider.clicked and charge_slider.position[0] <= event.pos[0] <= charge_slider.position[0] + charge_slider.width:
                    charge_slider.current_position = event.pos[0]

    # graphics update
    pygame.display.update()
