import pygame
from rest import *
from rest.utils.hooks import gen_hook
from settings import settings
from content_data.entities_data import entities
from entities.player import PlayerEntity
from behavior import *

class MyGame(Game):
    def __init__(self):
        super().__init__()
        init(settings)
        
        self.camera = Camera(settings.display_size, slowness=settings.camera_slowness, pos=(5, 0))
        
        self.entities_data = entities

    def load(self):
        self.event_system = G.event_system
        
        self.tilemap = Tilemap()
        self.tilemap.load('content_data/maps/1.pmap', spawn_hook=gen_hook())
        
        self.player = PlayerEntity((100, 150))
        G.object_collections.register(self.player.get_component('object'), 'entities')

    def update(self):
        self.camera.set_target(self.player.get_component('object'))
        self.camera.update()

        if settings.fps_bar:
            G.text['small_font'].renderz((str(round(G.window.fps, 1))), (list(settings.display_size)[0]-20, 5), color=(200, 200, 200))

        G.object_collections.update(view_area=self.camera.visible_rect)
        
        self.player.get_component('object').physics_update(self.tilemap)
        
        self.tilemap.renderz(self.camera.visible_rect, offset=self.camera)
        G.object_collections.renderz(layer_group='game', camera_offset=self.camera)
        
        G.window.cycle()
        G.input.update(self)

if __name__ == "__main__":
    game = MyGame()
    game.run()