from rest import *
from content_data.entities_data import entities
from rest.utils.gfx import smooth_approach

# import all interactions
from behavior import *

class MyGame(Game):
    def __init__(self):
        super().__init__()
        
        self.entities = entities

    def load(self):
        self.event_system = G.event_system

    def update(self):
        
        G.input.update()
        
        if G.input.pressed('space'):
            self.add_event('space', {'guys': self.entities.get_entity_objects_group('e_testguy')})
            
        self.process_all_events()

        G.window.cycle(uniforms={'surface': G.window.screen, 'time': G.window.dt})


if __name__ == "__main__":
    
    engine = init(
        dimensions=(800, 600),
        caption='soma try 1',
        fps_cap=60,
        sound_data_path='content_data/sound_data',
        spritesheet_path='content_data/image_data',
        input_path='content_data/input_configs.json'
    )
    
    game = MyGame()
    game.run()
