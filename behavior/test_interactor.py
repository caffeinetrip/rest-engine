from components.base_components import BaseInteraction, IOnEncounterStart, IOnEncounerReady, IOnPressSpaceButton
from content_data.priority_layers import PriorityLayers
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
        print("I'm on click")
        
        for guy in context['guys']:
            if guy.get_component('test_beh').value:
                print(guy.entity_id, 'is ready!')
        
        
        
        return None
