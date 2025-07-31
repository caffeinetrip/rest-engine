from rest import *
from content_data.entities_data import entities

# import all interactions
from behavior import *

class MyGame(Game):
    def __init__(self):
        super().__init__()
        self.entities = entities

    def load(self):
        self.event_system = G.event_system

    def update(self):
        self.process_all_events()

        G.window.cycle(uniforms={'surface': G.window.screen, 'time': G.window.dt})

if __name__ == "__main__":
    
    engine = init(
        dimensions=(800, 600),
        caption='soma try 1',
        fps_cap=60,
        sound_data_path='content_data/sound_data',
        spritesheet_path='content_data/image_data'
    )
    
    game = MyGame()
    game.run()
