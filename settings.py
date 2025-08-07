from rest.misc.settings import Settings

settings = Settings(
    
    # window settings
    window_size = (1280, 960),
    display_size = (320, 240),
    screens = ['background', 'default', 'ui'],
    fps_cap = 60,
    tile_size = 16,
    camera_slowness = 0.3,
    caption = 'rest',
    
    # paths
    sound_path = 'content_data/sound_data',
    font_path = None,
    spritesheets_path = 'content_data/image_data/spritesheets',
    entities_path = 'content_data/image_data/entities',
    frag_path = 'content_data/shaders/shader.frag',
    
    # vidgets
    fps_bar = True
)