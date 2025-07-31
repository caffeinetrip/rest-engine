import inspect
import sys
from typing import List, Type, Set
from abc import ABC

class ReflectionUtil:
    @classmethod
    def find_subclasses_with_interface(cls, base_class: Type, interface: Type) -> List[Type]:
        subclasses = []
        for module in sys.modules.values():
            if not hasattr(module, '__dict__'):
                continue
            
            for obj in module.__dict__.values():
                if (inspect.isclass(obj) and 
                    issubclass(obj, base_class) and 
                    issubclass(obj, interface) and
                    obj not in (base_class, interface) and 
                    not inspect.isabstract(obj)):
                    subclasses.append(obj)
        
        return subclasses