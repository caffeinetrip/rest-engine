from components.base_components import BaseInteraction, IOnEncounterStart, IOnEncounerReady, IOnPressSpaceButton
from rest.priority_layers import PriorityLayers
from typing import Any

# TEST INTERACTORS
class EncounerStartInteractor(BaseInteraction, IOnEncounterStart):
    def priority(self) -> PriorityLayers:
        return PriorityLayers.NORMAL
    
    def on_encounter_start(self, context: dict, game: Any = None) -> Any:
        print('Start')
        return None

class EncounterReadyInteractor(BaseInteraction, IOnEncounerReady):
    def priority(self) -> PriorityLayers:
        return PriorityLayers.LAST
    
    def on_encounter_ready(self, context: dict, game: Any = None) -> Any:
        print('Ready')
        return None

class PressSpaceButtonInteractor(BaseInteraction, IOnPressSpaceButton):
    def priority(self) -> PriorityLayers:
        return PriorityLayers.LAST
    
    def on_space(self, context: dict, game: Any = None) -> Any:
        entity_id = context.get('entity_id')
        
        print("I'm on click")
        
        if game.entities.get(entity_id).components.get('test'):
            print('ENTITY WITH ID 1 TEST IS TRUE')
        
        return None
