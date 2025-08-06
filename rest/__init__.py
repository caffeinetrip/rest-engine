from .misc.game import Game
from .misc.window import Window
from .mgl.mgl import MGL
from .mgl.render_object import RenderObject
from .event_system.event_system import EventSystem
from .G import G
from .misc.input import Input
from .objects.asset_library import AssetLibrary
from .assets.assets import Assets
from .objects.object_collections import ObjectCollections
from .misc.tilemap import Tilemap
from .misc.camera import Camera

def init(settings):
    window = Window(
        dimensions=settings.window_size,
        display_size=settings.display_size,
        caption=settings.caption,
        fps_cap=settings.fps_cap,
        frag_path=settings.frag_path,
        screens=settings.screens
    )

    G.initialize()
    
    G.window = window
    G.window.mgl = G.mgl
    
    G.assets = Assets(settings.spritesheets_path)
    G.asset_library = AssetLibrary(settings.entities_path)
    G.asset_library.assets
    G.object_collections = ObjectCollections(spatial_collections=['entities'])

    G.input = Input()
    
    if not window.frag_path:
        window.render_object = G.mgl.default_ro()
    else:
        window.render_object = G.mgl.render_object(window.frag_path)