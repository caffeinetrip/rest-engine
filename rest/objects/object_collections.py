# File: object_collections.py
import pygame
from rest.objects.object_sectors import ObjectSectors
from rest import G
import logging

logging.basicConfig(level=logging.DEBUG)

class ObjectCollections:
    def __init__(self, sector_size=64, spatial_collections=[]):
        self.collections = {}
        self.processing = False
        self.pending_items = []
        self.spatial_collections = set(spatial_collections)
        self.object_sectors = ObjectSectors(sector_size=sector_size)

    def configure_spatial_collections(self, spatial_collections=[]):
        self.spatial_collections = set(spatial_collections)

    def register(self, game_object, collection):
        if self.processing:
            self.pending_items.append((game_object, collection))
        else:
            if collection in self.spatial_collections:
                self.object_sectors.register(game_object, collection_name=collection)
            else:
                if collection not in self.collections:
                    self.collections[collection] = []
                # Лимит частиц установлен в moving_object.py
                self.collections[collection].append(game_object)

    def update(self, collection=None, release_lock=True, view_area=pygame.Rect(0, 0, 100, 100)):
        time_delta = G.window.dt
        if len(self.spatial_collections) and not collection:
            self.object_sectors.refresh_visible(view_area)
            self.collections.update(self.object_sectors.visible_objects)
        self.processing = True
        if collection:
            if collection in self.collections:
                for game_object in self.collections[collection].copy():
                    # Check if object has get_component (for CMSEntity) or use direct update (for Particle)
                    if collection == 'particles':
                        should_remove = game_object.update(time_delta)
                    else:
                        should_remove = game_object.get_component('object').tick(time_delta)
                    if should_remove:
                        self.collections[collection].remove(game_object)
                        if collection in self.spatial_collections:
                            self.object_sectors.unregister(game_object)
        else:
            for coll in self.collections:
                self.update(coll, release_lock=False)
        if release_lock:
            self.processing = False
            if self.pending_items:
                for item in self.pending_items:
                    self.register(*item)
                self.pending_items = []

    def render(self, surface, collection=None, camera_offset=(0, 0)):
        if collection:
            if collection in self.collections:
                for game_object in self.collections[collection]:
                    game_object.render(surface, camera_offset=camera_offset)
        else:
            for coll in self.collections:
                self.render(surface, collection=coll, camera_offset=camera_offset)

    def renderz(self, collection=None, layer_group='main', camera_offset=(0, 0)):
        if collection:
            if collection in self.collections:
                sorted_objects = sorted(
                    self.collections[collection],
                    key=lambda go: go.z if hasattr(go, 'z') else go.get_component('object').get_component('z').val
                )
                for game_object in sorted_objects:
                    game_object.renderz(camera_offset=camera_offset, group=layer_group)
        else:
            all_objects = []
            for coll in self.collections:
                all_objects.extend(self.collections[coll])
            sorted_all = sorted(
                all_objects,
                key=lambda go: go.z if hasattr(go, 'z') else go.get_component('object').get_component('z').val
            )
            for game_object in sorted_all:
                game_object.renderz(camera_offset=camera_offset, group=layer_group)