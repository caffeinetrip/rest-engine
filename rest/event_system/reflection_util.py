import inspect
import sys
from typing import List, Type
from abc import ABC

class ReflectionUtil:
    @classmethod
    def find_subclasses_with_interface(cls,  base_class: Type,  interface: Type,  module_prefix: str = "behavior" ) -> List[Type]:
        
        subclasses = []
        for name, module in sys.modules.items():
            if not name.startswith(module_prefix):
                continue
            if not hasattr(module, '__dict__'):
                continue

            for obj in module.__dict__.values():
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, base_class)
                    and issubclass(obj, interface)
                    and obj not in (base_class, interface)
                    and not inspect.isabstract(obj)
                ):
                    subclasses.append(obj)

        return subclasses
