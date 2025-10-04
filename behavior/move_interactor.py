from components.interaction_interfaces import BaseInteraction, IOnEntityMove
from content_data.priority_layers import PriorityLayers
from rest import G
from rest.utils.game_math import get_rotate, get_state, state_dict, degrees_dict 

class MoveInteractor(BaseInteraction, IOnEntityMove):
    def priority(self):
        return PriorityLayers.NORMAL

    def on_move(self, context, entity=None):
        if not entity:
            return

        x = context.get('x', 0)
        y = context.get('y', 0)

        if entity.get_component('move_x').value == 0 and entity.get_component('move_y').value == 0:
            direction = context.get('direction', entity.get_component('target_direction').value)
            mirror = context.get('mirror', entity.get_component('target_mirror').value)
        else:
            direction = entity.get_component('target_direction').value
            mirror = entity.get_component('target_mirror').value

        max_speed = context.get('max_speed', [entity.get_component('max_speed').x, entity.get_component('max_speed').y])

        entity.get_component('move_x').value += x
        entity.get_component('move_y').value += y
        entity.get_component('target_direction').value = direction
        entity.get_component('target_mirror').value = mirror

        entity.get_component('max_speed').x = max_speed[0]
        entity.get_component('max_speed').y = max_speed[1]

        entity.get_component('move_x').value = max(min(entity.get_component('move_x').value, 1), -1)
        entity.get_component('move_y').value = max(min(entity.get_component('move_y').value, 1), -1)

        entity.get_component('speed').x = entity.get_component('move_x').value * entity.get_component('max_speed').x
        entity.get_component('speed').y = entity.get_component('move_y').value * entity.get_component('max_speed').y

        entity.get_component('moving').value = entity.get_component('move_x').value != 0 or entity.get_component('move_y').value != 0
                        
        entity.get_component('target_degrees').value = degrees_dict.get((entity.get_component('target_direction').value, entity.get_component('target_mirror').value))
        change_degrees = get_rotate(entity.get_component('degrees').value, entity.get_component('target_degrees').value, entity.get_component('rotate_speed').value)
        entity.get_component('degrees').value += change_degrees
        
        x = get_state(entity.get_component('degrees').value)
        if not ('rotate' in x[0]):
            state = f'walk/{x[0]}' if entity.get_component('moving').value else f'idle/{x[0]}'
            entity.get_component('direction').value = entity.get_component('target_direction').value 
            entity.get_component('object').get_component('mirror').flip_x = x[1]
            
        else:
            state = x[0]
            entity.get_component('object').get_component('mirror').flip_x = x[1]

        if state == 'walk/top' or state == 'walk/down':
            entity.get_component('last_vertical_state').state = state
        
        if state == 'rotate/right_down':
            entity.get_component('last_vertical_state').state = 'walk/down'
        
        if state == 'rotate/right_top':
            entity.get_component('last_vertical_state').state = 'walk/top'
        
        if G.input.holded_keys_count > 2:
            if state == 'idle/down' or state == 'idle/right' or state == 'walk/right' or state == 'rotate/right_down' or state == 'rotate/right_top':
                state = entity.get_component('last_vertical_state').state

        entity.get_component('object').set_state(state)