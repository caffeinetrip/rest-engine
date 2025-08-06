from entities.test_guy import TestGuy

from rest.components.camera import Camera
from rest.utils.cms import CMSEntity
from typing import List, Optional, Dict

class EntityData:
    def __init__(self):
        self.entities_dict: Dict[str, CMSEntity] = {} # type: ignore
        self._initialized = False

    def initialize(self):
        if not self._initialized:
            entities = [
                Camera('e_camera', size=(800, 600), pos=(0, 0), slowness=5)
            ]
            self.entities_dict = {entity.entity_id: entity for entity in entities if hasattr(entity, 'entity_id')}
            self._initialized = True

    def get_entity(self, id: str) -> Optional[CMSEntity]:
        self.initialize()
        return self.entities_dict.get(id)

    def get_entity_ids_group(self, entity_id: str) -> List[str]:
        self.initialize()
        return [id for id in self.entities_dict.keys() if entity_id in id]

    def get_entity_objects_group(self, entity_id: str) -> List[CMSEntity]:
        self.initialize()
        return [entity for id, entity in self.entities_dict.items() if entity_id in id]

    def add_entity(self, entity: CMSEntity) -> None:
        self.initialize()
        if hasattr(entity, 'entity_id'):
            self.entities_dict[entity.entity_id] = entity

    def remove_entity(self, entity_id: str) -> bool:
        self.initialize()
        if entity_id in self.entities_dict:
            del self.entities_dict[entity_id]
            return True
        return False

entities = EntityData()