from rest.utils.cms import CMSEntity
from components.cms_components import Health, Energy, TestBehavior

class TestGuy(CMSEntity):
    def __init__(self, entity_id):
        super().__init__(entity_id)
        
        self.components = {
            'health': Health(hp=10),
            'energy': Energy(value=5),
            'test_beh': TestBehavior(value=True)
        }
