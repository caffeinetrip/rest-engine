from typing import Dict

class CMSComponentDefinition:
    pass

class CMSEntity:
    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self.components: Dict[str, CMSComponentDefinition] = {}
    
    def add_component(self, name: str, component: CMSComponentDefinition):
        self.components[name] = component
    
    def get_component(self, name: str) -> None | CMSComponentDefinition:
        return self.components.get(name)
