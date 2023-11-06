import pygame

import settings
from game_setup.tile import *
from game_setup.player import *
from debug.debug_file import debug


class Level:
    def __init__(self):

        # sprite group
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(settings.world_map):
            for col_index, col in enumerate(row):
                x = col_index * settings.TILE_SIZE
                y = row_index * settings.TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):

        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)


# Camera_setting
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # get disaply surface
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surface = pygame.image.load('C:/Users/mweinzettl/PycharmProjects/dark_zelda/all_tiles_map/floo_test_3.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
    def custom_draw(self, player):
        # getting the offset

        self.offset.x = player.rect.x - self.half_width
        self.offset.y = player.rect.y - self.half_height

        #render floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.center - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
