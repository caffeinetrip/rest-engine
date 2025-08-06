from rest.misc.settings import Settings

settings = Settings(
    window_size = (800, 600),
    display_size = (340, 220),
    fps_cap = 60,
    tile_size = 16,
    camera_slowness = 0.3,
    caption = 'rest',
    
    screens = ['background', 'default', 'ui'],
    
    sound_path = 'content_data/sound_data',
    font_path = None,
    spritesheets_path = 'content_data/image_data/spritesheets',
    entities_path = 'content_data/image_data/entities',
    frag_path = 'content_data/shaders/shader.frag'
)