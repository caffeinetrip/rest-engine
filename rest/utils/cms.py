from typing import Dict
from dataclasses import dataclass, is_dataclass

class SlottedDataclassMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        if not namespace.get('_is_base_class', False) and not is_dataclass(namespace) and '__slots__' not in namespace:
            cls = dataclass(slots=True)(type.__new__(mcs, name, bases, namespace))
            return cls
        return super().__new__(mcs, name, bases, namespace)

class CMSComponentDefinition(metaclass=SlottedDataclassMeta):
    _is_base_class = True
class CMSEntity:
    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self.components: Dict[str, CMSComponentDefinition] = {}
    
    def add_component(self, name: str, component: CMSComponentDefinition):
        self.components[name] = component
    
    def get_component(self, name: str) -> None | CMSComponentDefinition:
        return self.components.get(name)
