from rest.utils.cms import CMSComponentDefinition
from dataclasses import dataclass

@dataclass
class Health(CMSComponentDefinition):
    hp: int

@dataclass
class Energy(CMSComponentDefinition):
    value: int
    
@dataclass
class TestBehavior(CMSComponentDefinition):
    value: bool