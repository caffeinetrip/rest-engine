from components.interaction_interfaces import BaseInteraction, IOnClick
from content_data.priority_layers import PriorityLayers
from rest import G
from rest.vfx.sparks import Spark
from rest.utils.game_math import scale_mouse_pos
import random
import math

class ClickInteractor(BaseInteraction, IOnClick):
    def priority(self):
        return PriorityLayers.NORMAL

    def on_click(self, context, entity=None):
            position = scale_mouse_pos(list(context['position']), G.window.dimensions, G.window.display_size)

            num_sparks = 20
            for _ in range(num_sparks):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(100, 300)
                decay = random.uniform(2.0, 4.0)
                color1 = (random.randint(25, 30), random.randint(25, 30), random.randint(25, 30))
                color2 = (random.randint(240, 245), random.randint(240, 245), random.randint(240, 245))
                color3 = (random.randint(150, 160), random.randint(150, 160), random.randint(150, 160))
                
                spark = Spark(
                    pos=position,
                    angle=angle,
                    size=(random.uniform(4, 8), random.uniform(0.5, 2)),
                    speed=speed,
                    decay=decay,
                    color=random.choice([color1, color2, color3]),
                    z=500000
                )

                if not hasattr(G, 'sparks'):
                    G.sparks = []
                G.sparks.append(spark)

                G.window.renderf(spark.render, offset=(0, 0), z=spark.z, group='default')