import pygame
import random
import colors as c
from entities import Base_Entity
import json

class Simulation:

    # initialize app with parameters
    def __init__(self, WIN_SIZE):
        pygame.init()
        self.running = True
        self.WIN_SIZE = WIN_SIZE
        self.screen = pygame.display.set_mode(WIN_SIZE)
        self.black_surf = pygame.Surface(WIN_SIZE, pygame.SRCALPHA, 32)
        self.black_surf.fill((0, 0, 0, 1))
        self.clock = pygame.time.Clock()
        self.fps = 120

        self.render_surface = pygame.Surface(WIN_SIZE)
        self.screen.blit(self.render_surface, (0,0))

        self.paint_square = pygame.Surface((1,1)) 
        self.paint_square.fill(c.black)

        self.NUM_OPTION = 1
        self.entities = []

        with open('entities.json') as f:
            self.jsonData = json.load(f)

    def get_random_pixel_pos(self):
        x = random.randint(0, self.WIN_SIZE[0])
        y = random.randint(0, self.WIN_SIZE[1])
        return (x, y)

    def paint_pixel(self, pixel_pos, new_color):
        self.paint_square.fill(new_color)
        self.render_surface.blit(self.paint_square, pixel_pos)

    def spawn_entity(self, spawn_pos):
        if self.NUM_OPTION in self.jsonData['entities']:
            print('spawning new ent')
            entity_data = self.jsonData['entities'][self.NUM_OPTION]
            name = entity_data.pop('name', None)  # Remove 'name' from entity_data
            new_entity = Base_Entity(name, spawn_pos, self.render_surface, self.spawn_entity, **entity_data)
            self.entities.append(new_entity)

    # called every frame
    def update(self):

        self.clock.tick(self.fps)

        for event in pygame.event.get():

            # When user presses 'x' button on application
            if event.type == pygame.QUIT:
                self.running = False 
                pygame.quit()

            # When user presses 'Escape' on keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    pygame.quit()

            # When user presses number buttons
            if event.type == pygame.KEYDOWN:
                # 48 - 57
                if event.key == 48:
                    self.NUM_OPTION = 'Bot'
                if event.key == 49:
                    self.NUM_OPTION = 'Apple'
                if event.key == 50:
                    self.NUM_OPTION = 'Flank'
                if event.key == 51:
                    self.NUM_OPTION = 3
                if event.key == 52:
                    self.NUM_OPTION = 4
                if event.key == 53:
                    self.NUM_OPTION = 5
                if event.key == 54:
                    self.NUM_OPTION = 6
                if event.key == 55:
                    self.NUM_OPTION = 7
                if event.key == 56:
                    self.NUM_OPTION = 8
                if event.key == 57:
                    self.NUM_OPTION = 9

                print(self.NUM_OPTION)

            # When user clicks on screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.NUM_OPTION:
                    self.spawn_entity(pygame.mouse.get_pos())

        for entity in self.entities:
            entity.update(self.render_surface)
            self.paint_pixel(entity.pos, entity.color)

        self.render_surface.blit(self.black_surf,(0,0))
        self.screen.blit(self.render_surface, (0, 0))    
        pygame.display.flip()


    # run app
    def run(self):
        while self.running:
            self.update()



