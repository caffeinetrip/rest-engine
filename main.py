# main.py
from rest import init, Game, G
from behavior import *
from entities.test_guy import TestGuy

class MyGame(Game):
    def __init__(self):
        super().__init__()
        self.entities = []

    def load(self):
        self.event_system = G.event_system
        test_entity = TestGuy('e_testguy1')
        self.entities.append(test_entity)

    def update(self):
        self.process_events()

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
