import os
import importlib

current_dir = os.path.dirname(os.path.abspath(__file__))
py_files = [f for f in os.listdir(current_dir) if f.endswith('.py') and f != '__init__.py']

for file in py_files:
    module_name = file[:-3]
    try:
        importlib.import_module(f".{module_name}", package=__name__)
    except ImportError as e:
        print(f"error - {module_name}: {e}")