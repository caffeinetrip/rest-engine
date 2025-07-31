# rest/G.py
from .mgl.mgl import MGL
from .misc.window import Window
from .utils.event_system import EventSystem
from .misc.game import Game

class G:
    mgl = None
    game = None
    event_system = None

    @classmethod
    def initialize(cls):
        cls.mgl = MGL()
        cls.event_system = EventSystem()
        cls.game = Game()
