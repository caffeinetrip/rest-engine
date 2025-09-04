# File: game.py
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
        G.object_collections.configure_spatial_collections(['entities', 'particles'])
        
        asset_path = 'content_data/image_data/assets'
        G.asset_library.initialize(asset_path)

    def update(self):
        
        self.camera.set_target(self.player.get_component('object'))
        self.camera.update()
        
        if settings.fps_bar:
            G.text['small_font'].renderz((str(round(G.window.fps, 1))), (list(settings.display_size)[0]-20, 5), color=(145, 145, 145))
        
        if G.input.mouse_pressed(1):
            self.add_event('click', {'position': G.input.get_mouse_position()})
            
        G.object_collections.update(view_area=self.camera.visible_rect)
        
        self.player.get_component('object').physics_update(self.tilemap)
        
        if hasattr(G, 'sparks'):
            dt = G.window.dt 
            for spark in G.sparks[:]:
                if spark.update(dt):
                    G.sparks.remove(spark)
                else:
                    G.window.renderf(spark.render, offset=(0, 0), z=spark.z, group='ui')
        
        renderable_items = self.tilemap.get_renderable_items(
            self.camera.visible_rect, 
            self.player.get_component('object').get_component('object').hitbox, 
            offset=self.camera.pos,
            group='default',
            objects_collection=G.object_collections
        )
        
        sorted_items = sorted(renderable_items, key=lambda item: item.z)
        
        for item in sorted_items:
            item.render()
            
        G.object_collections.renderz(collection='particles', camera_offset=self.camera.pos)
        G.window.cycle()
        
        G.input.update(self)

if __name__ == "__main__":
    game = MyGame()
    game.run()