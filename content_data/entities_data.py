from entities.test_guy import TestGuy
from rest import CMSEntity
from typing import List, Optional, Dict

class EntityData:
    def __init__(self, entities: List[CMSEntity]):
        self.entities_dict: Dict[str, CMSEntity] = {entity.entity_id: entity for entity in entities if hasattr(entity, 'entity_id')}
    
    def get_entity(self, id: str) -> Optional[CMSEntity]:
        return self.entities_dict.get(id)
    
    def get_entity_ids_group(self, entity_id: str) -> List[str]:
        return [id for id in self.entities_dict.keys() if entity_id in id]
    
    def get_entity_objects_group(self, entity_id: str) -> List[CMSEntity]:
        return [entity for id, entity in self.entities_dict.items() if entity_id in id]
    
    def add_entity(self, entity: CMSEntity) -> None:
        if hasattr(entity, 'entity_id'):
            self.entities_dict[entity.entity_id] = entity
    
    def remove_entity(self, entity_id: str) -> bool:
        if entity_id in self.entities_dict:
            del self.entities_dict[entity_id]
            return True
        return False

entities = EntityData([
    TestGuy('e_testguy1'),
    TestGuy('e_testguy2'),
])
