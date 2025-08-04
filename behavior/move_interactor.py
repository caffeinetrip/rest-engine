from components.interaction_interfaces import BaseInteraction, IOnEntityMove
from content_data.priority_layers import PriorityLayers
from rest import G

class MoveInteractor(BaseInteraction, IOnEntityMove):
    def priority(self):
        return PriorityLayers.NORMAL

    def on_move(self, context, entity=None):
        if not entity:
            return

        x = context.get('x', 0)
        y = context.get('y', 0)

        if entity.get_component('move_x').value == 0 and entity.get_component('move_y').value == 0:
            direction = context.get('direction', entity.get_component('direction').value)
            mirror = context.get('mirror', entity.get_component('object').get_component('mirror').flip_x)
        else:
            direction = entity.get_component('direction').value
            mirror = entity.get_component('object').get_component('mirror').flip_x

        max_speed = context.get('max_speed', [entity.get_component('max_speed').x, entity.get_component('max_speed').y])

        entity.get_component('move_x').value += x
        entity.get_component('move_y').value += y
        entity.get_component('direction').value = direction
        entity.get_component('object').get_component('mirror').flip_x = mirror
        entity.get_component('max_speed').x = max_speed[0]
        entity.get_component('max_speed').y = max_speed[1]

        entity.get_component('move_x').value = max(min(entity.get_component('move_x').value, 1), -1)
        entity.get_component('move_y').value = max(min(entity.get_component('move_y').value, 1), -1)

        if entity.get_component('move_x').value != 0 and entity.get_component('move_y').value != 0:
            entity.get_component('max_speed').x = 35
        else:
            entity.get_component('max_speed').x = max_speed[0]

        entity.get_component('speed').x = entity.get_component('move_x').value * entity.get_component('max_speed').x
        entity.get_component('speed').y = entity.get_component('move_y').value * entity.get_component('max_speed').y

        entity.get_component('moving').value = entity.get_component('move_x').value != 0 or entity.get_component('move_y').value != 0

        state = f'walk/{entity.get_component("direction").value}' if entity.get_component('moving').value else f'idle/{entity.get_component("direction").value}'
        
        if state == 'walk/top' or state == 'walk/down':
            entity.get_component('last_vertical_state').state = state
        
        if G.input.holded_keys_count > 2:
            if state == 'idle/down' or state == 'idle/right' or state == 'walk/right':
                state = entity.get_component('last_vertical_state').state

        entity.get_component('object').set_state(state)