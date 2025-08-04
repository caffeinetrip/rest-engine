from rest.utils.cms import CMSComponentDefinition

# other components
# -------------------------------------------------------------------------------------------------------------
class Health(CMSComponentDefinition):
    hp: int

class Energy(CMSComponentDefinition):
    value: int
    
class TestBehavior(CMSComponentDefinition):
    value: bool