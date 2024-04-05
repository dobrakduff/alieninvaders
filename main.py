import pygame
from random import choice
import sys
from player import Player
import obstacles
from alien import Alien
from laser import Laser

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        player_sprite = Player((self.screen_width / 2, self.screen_height), self.screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives=3
        self.life_surf=pygame.image.load('images/player.png').convert_alpha()
        self.life_x_pos=screen_width-(self.life_surf.get_size()[0]*2+20)

        self.shape = obstacles.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obst_amount = 4
        self.obst_x_pos = [num * (screen_width / self.obst_amount) for num in range(self.obst_amount)]
        self.create_milty_obs(*self.obst_x_pos, x_start=screen_width / 15, y_start=480)

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index in range(rows):
            for col_index in range(cols):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_pos_check(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= self.screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, self.screen_height)
            self.alien_lasers.add(laser_sprite)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacles.Block(self.block_size, (241, 65, 65), x, y)
                    self.blocks.add(block)

    def create_milty_obs(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def collision_checks(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.aliens, True):
                    laser.kill()
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives-=1
                    if self.lives<=0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()
    def display_lives(self):
        for live in range(self.lives-1):
            x=self.life_x_pos+(live*self.life_surf.get_size()[0]+10)
            screen.blit(self.life_surf,(x,8))


    def run(self, screen):
        ALIENLASER = pygame.USEREVENT + 1  # Define ALIENLASER event
        pygame.time.set_timer(ALIENLASER, 800)  # Set timer for the ALIENLASER event
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ALIENLASER:
                    self.alien_shoot()  # Call alien_shoot method when ALIENLASER event occurs

            screen.fill((30, 30, 30))

            # Update player sprite
            self.player.sprite.update()
            self.aliens.update(self.alien_direction)
            self.alien_pos_check()
            self.alien_lasers.update()
            self.collision_checks()  # Check for collisions
            self.player.sprite.lasers.draw(screen)
            # Draw player sprite
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.display_lives()
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run(screen)
