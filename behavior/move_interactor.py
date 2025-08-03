from components.interaction_interfaces import BaseInteraction, IOnEntityMove
from content_data.priority_layers import PriorityLayers
from typing import Any

class MoveInteractor(BaseInteraction, IOnEntityMove):
    def priority(self) -> PriorityLayers:
        return PriorityLayers.NORMAL

    def on_move(self, context: dict, entity: Any = None) -> Any:
        if not entity:
            return

        x = context.get('x', 0)
        y = context.get('y', 0)

        if entity.move_x == 0 and entity.move_y == 0:
            direction = context.get('direction', entity.direction)
            mirror = context.get('mirror', entity.mirror[0])
        else:
            direction = entity.direction
            mirror = entity.mirror[0]

        max_speed = context.get('max_speed', entity.max_speed)

        entity.move_x += x
        entity.move_y += y
        entity.direction = direction
        entity.mirror[0] = mirror
        entity.max_speed = max_speed

        entity.move_x = max(min(entity.move_x, 1), -1)
        entity.move_y = max(min(entity.move_y, 1), -1)

        if entity.move_x != 0 and entity.move_y != 0:
            entity.max_speed[0] = 35
        else:
            entity.max_speed[1] = max_speed[1]

        entity.speed[0] = entity.move_x * entity.max_speed[0]
        entity.speed[1] = entity.move_y * entity.max_speed[1]

        entity.moving = entity.move_x != 0 or entity.move_y != 0

        state = f'walk/{entity.direction}' if entity.moving else f'idle/{entity.direction}'
        entity.set_state(state)
