from rest.misc.game import Game


class MyGame(Game):
    pass


if __name__ == "__main__":
    from behavior import *
    MyGame().run()