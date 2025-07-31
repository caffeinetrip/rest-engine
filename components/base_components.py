from abc import ABC, abstractmethod
from typing import Any
from content_data.priority_layers import PriorityLayers

class BaseInteraction(ABC):
    @abstractmethod
    def priority(self) -> PriorityLayers:
        return PriorityLayers.NORMAL

class IOnEncounterStart(ABC):
    @abstractmethod
    def on_encounter_start(self, context: dict, game: Any = None) -> Any:
        pass

class IOnEncounerReady(ABC):
    @abstractmethod
    def on_encounter_ready(self, context: dict, game: Any = None) -> Any:
        pass
    
class IOnPressSpaceButton(ABC):
    @abstractmethod
    def on_space(self, context: dict, game: Any = None) -> Any:
        pass
