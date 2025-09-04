from abc import ABC, abstractmethod
from typing import Any
from content_data.priority_layers import PriorityLayers

class BaseInteraction(ABC):
    @abstractmethod
    def priority(self) -> PriorityLayers:
        return PriorityLayers.NORMAL

class IOnEncounterStart(ABC):
    @abstractmethod
    def on_encounter_start(self, context: dict, entity: Any = None) -> Any:
        pass

class IOnEncounerReady(ABC):
    @abstractmethod
    def on_encounter_ready(self, context: dict, entity: Any = None) -> Any:
        pass

class IOnLoadFolder(ABC):
    @abstractmethod
    def on_load_folder(self, context: dict, entity: Any = None) -> Any:
        pass

class IOnEntityMove(ABC):
    @abstractmethod
    def on_move(self, context: dict, entity: Any = None) -> Any:
        pass
    
class IOnClick(ABC):
    @abstractmethod
    def on_click(self, context: dict, entity: Any = None) -> Any:
        pass
