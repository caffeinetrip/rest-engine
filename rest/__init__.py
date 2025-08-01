from .misc.game import Game
from .misc.window import Window
from .mgl.mgl import MGL
from .mgl.render_object import RenderObject
from .event_system.event_system import EventSystem
from .G import G
from .misc.input import Input
from .renderer.renderer import Renderer
from .objects.asset_library import AssetLibrary
from .assets.assets import Assets
from .objects.object_collections import ObjectCollections
from .misc.tilemap import Tilemap
from .misc.camera import Camera

def init(dimensions=(640, 480), caption='window', sound_data_path=None, spritesheet_path=None,
         font_path=None, flags=0, fps_cap=60, dt_cap=1, frag_path=None, sound_filetype='wav', entities_path=None):
    
    # initialize window with G
    
    window = Window(
        dimensions=dimensions,
        caption=caption,
        flags=flags,
        fps_cap=fps_cap,
        dt_cap=dt_cap,
        frag_path=frag_path
    )

    G.initialize()
    
    G.window = window
    window.mgl = G.mgl
    
    G.assets = Assets(spritesheet_path)
    G.asset_library = AssetLibrary(entities_path)
    G.asset_library.assets
    G.object_collections = ObjectCollections(spatial_collections=['entities'])

    G.renderer = Renderer()
    G.input = Input()
    
    
    if not window.frag_path:
        window.render_object = G.mgl.default_ro()
        
    else:
        window.render_object = G.mgl.render_object(window.frag_path)
