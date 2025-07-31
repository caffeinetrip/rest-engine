from typing import Dict, List, Any
from collections import defaultdict
from components.base_components import *
from rest.event_system.reflection_util import ReflectionUtil

class EventSystem:
    _instance = None # type: ignore
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        if not self._initialized: # type: ignore
            
            self.handlers: Dict[str, List[BaseInteraction]] = defaultdict(list)
            self._register_handlers()
            self._initialized = True
    
    # ADD NEW INTERACTIONS
    def _register_handlers(self):
        
        interface_map = {
            IOnEncounterStart: 'encounter_start',
            IOnEncounerReady: 'encounter_ready',
            IOnPressSpaceButton: 'space'
        }
        
        for interface, event_type in interface_map.items():
            
            classes = ReflectionUtil.find_subclasses_with_interface(BaseInteraction, interface)
            
            instances = [cls() for cls in classes]
            instances.sort(key=lambda x: x.priority().value)
            self.handlers[event_type] = instances
    
    def trigger_event(self, event_type: str, context: dict, game: Any = None) -> List[Any]:
        results = []
        
        for handler in self.handlers.get(event_type, []):
            method_name = f'on_{event_type}'
            
            if hasattr(handler, method_name):
                result = getattr(handler, method_name)(context, game)
                
                if result is not None:
                    results.append(result)
                    
        return results
