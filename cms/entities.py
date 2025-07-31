from typing import Dict, Any
from dataclasses import dataclass

class Entity:
    def __init__(self, entity_id: int, components: Dict[str, Any]):
        self.entity_id = entity_id
        self.components = components

entities = {
    '1': Entity(1, {
        "TagEnergy": 10,
        "TagDamageOnTurn": 5,
        "test": True
    })
}
