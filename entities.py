import pygame
import random

class Base_Entity:
    def __init__(self, name, pos, render_surface, spawn_new, speed, health, attack, defense, experience, mana, saturation, color, attr_color, defl_color):
        print('new ent')
        self.render_surface = render_surface
        self.name = name
        self.pos = pos
        self.speed = speed
        self.moveAmount = 0
        self.health = health
        self.attack = attack
        self.defense = defense
        self.experience = experience
        self.mana = mana
        self.saturation = saturation
        self.color = tuple(map(int, color.split(',')))
        self.attr_color = tuple(map(int, attr_color.split(',')))
        self.defl_color = tuple(map(int, defl_color.split(',')))
        self.spawn_new = spawn_new

    def get_surrounding_colors(self):
        colors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = self.pos[0] + dx, self.pos[1] + dy
                if 0 <= nx < self.render_surface.get_width() and 0 <= ny < self.render_surface.get_height():
                    color = self.render_surface.get_at((nx, ny))[:3]  # Get RGB values only
                    colors.append(color)
        return colors

    def move(self):
        print('moving', self.name, self.pos)
        print(self.moveAmount)
        print(self.speed)
        

        # if moveamount is less than speed threshold
        if self.moveAmount < self.speed:
            self.moveAmount += self.speed / 10
        else:
            # move and reset amount
            self.moveAmount = 0
            # check surrounding pixels
            colors = self.get_surrounding_colors()
            movePercents = [0] * len(colors)

            # loop through surrounding colors
            for surr_index, surr_color in enumerate(colors):

                # loop through channels of surrounding colors
                for chan_index, chan_value in enumerate(surr_color):

                    # check map color channel
                    if chan_value > 0:
                        
                         # if map color matches entity's color
                        if self.color[chan_index] > 0:
                            # calculate the adjustment based on the difference between entity's color and surrounding color
                            adjustment = (self.color[chan_index] - chan_value) / 255
                            # apply the adjustment to movePercents for this specific surr_index
                            movePercents[surr_index] += adjustment

                    # check attr_color
                    if self.attr_color[chan_index] > 0:
                        # calculate the adjustment based on the similarity between attr_color and surrounding color
                        adjustment = (self.attr_color[chan_index] - chan_value) / 255
                        # apply the adjustment to movePercents for this specific surr_index
                        movePercents[surr_index] += adjustment

                    # check defl_color
                    if self.defl_color[chan_index] > 0:
                        # calculate the adjustment based on the difference between entity's color and surrounding color
                        adjustment = (self.defl_color[chan_index] - chan_value) / 255
                        # apply the adjustment to movePercents for this specific surr_index
                        movePercents[surr_index] -= adjustment

            # Prefer moving towards colors similar to attr_color
            top_three_indices = sorted(range(len(movePercents)), key=lambda k: movePercents[k], reverse=True)[:3]

            # Normalize the top three values to add up to 100
            total_top_values = sum(movePercents[i] for i in top_three_indices)
            normalized_values = [movePercents[i] / total_top_values * 100 for i in top_three_indices]

            # Randomly choose one based on the normalized values
            chosen_index = random.choices(top_three_indices, weights=normalized_values)[0]

            # Move in a more random direction
            dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

            # Check if the new position is within bounds
            new_x, new_y = self.pos[0] + dx, self.pos[1] + dy
            if 0 <= new_x < self.render_surface.get_width() and 0 <= new_y < self.render_surface.get_height():
                self.pos = (new_x, new_y)
            

        # look at pixels around

        # move

        # update drawing

        # add move amount

    def update(self, render_surface):
        self.render_surface = render_surface
        self.move()
