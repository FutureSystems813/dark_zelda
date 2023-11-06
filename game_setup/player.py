import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            'C:/Users/mweinzettl/PycharmProjects/dark_zelda/player_skull_sprite.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.player_hitbox = self.rect.inflate(-5, -30)

        self.direction = pygame.math.Vector2()
        self.speed = 7

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.player_hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.player_hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.player_hitbox.center

    # collisions

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.player_hitbox.colliderect(self.player_hitbox):
                    if self.direction.x > 0:
                        self.player_hitbox.right = sprite.player_hitbox.left
                    if self.direction.x < 0:
                        self.player_hitbox.left = sprite.player_hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.player_hitbox.colliderect(self.player_hitbox):  # move up
                    if self.direction.y < 0:
                        self.player_hitbox.top = sprite.player_hitbox.bottom
                    if self.direction.y > 0:
                        self.player_hitbox.bottom = sprite.player_hitbox.top

    def update(self):
        self.input()
        self.move(self.speed)
