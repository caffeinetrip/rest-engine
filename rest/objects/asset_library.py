import os
import pygame
import json

from rest.assets.asset_utils import load_img_directory
from rest.utils.io import read_json, write_json
from rest.assets.animation import Animation


class ObjectData:
    def __init__(self, settings, resources=None):
        self.specs = settings
        self.settings = settings
        self.resources = resources or {}
        self.sequences = {}

        for sequence_name, sequence_config in self.specs.get('sequences', {}).items():
            sequence_images = []

            sequence_parts = sequence_name.split('/')
            current_dict = self.resources

            for i, part in enumerate(sequence_parts):
                if isinstance(current_dict, dict) and part in current_dict:
                    current_dict = current_dict[part]
                else:
                    current_dict = None
                    break

            if current_dict and isinstance(current_dict, dict):
                sorted_items = []
                for key, value in current_dict.items():
                    if isinstance(value, pygame.Surface):
                        try:
                            num = int(key.split('_')[-1])
                            sorted_items.append((num, value))
                        except ValueError:
                            sorted_items.append((0, value))

                sorted_items.sort(key=lambda x: x[0])
                sequence_images = [item[1] for item in sorted_items]

            if sequence_images:
                self.sequences[sequence_name] = Animation(
                    sequence_images,
                    config=sequence_config
                )

class AssetLibrary:
    def __init__(self, directory=None):
        
        self.directory = directory
        self.assets = {}
        if directory:
            self.initialize(directory)
            

    def initialize(self, directory):
        self.directory = directory
        self.build_asset_registry()

    def __getitem__(self, key):
        return self.assets.get(key, None)

    def build_asset_registry(self):
        if not os.path.exists(self.directory):
            return

        for object_dir in os.listdir(self.directory):
            object_path = os.path.join(self.directory, object_dir)
            if not os.path.isdir(object_path):
                continue

            settings = {
                'uid': object_dir,
                'size': [16, 16],
                'offset': [0, 0],
                'transparency': [0, 0, 0],
                'centered': False,
                'category': 'object',
                'images': {},
                'sequences': {},
                'initial': None,
                'resource_path': object_path
            }

            config_path = os.path.join(object_path, 'config.json')
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        loaded_settings = json.load(f)
                        settings.update(loaded_settings)
                except Exception as e:
                    print(f"Error loading config for {object_dir}: {e}")
            else:

                settings['sequences'] = {}
                settings['initial'] = 'idle/down'
                settings['category'] = 'entity' if object_dir == 'player' else 'object'
                settings['centered'] = True if object_dir == 'player' else False

                for root, dirs, files in os.walk(object_path):
                    rel_path = os.path.relpath(root, object_path).replace(os.sep, '/')
                    if rel_path == '.' or not files:
                        continue

                    png_files = sorted([f for f in files if f.endswith('.png') and f.startswith('img_')],
                                    key=lambda x: int(x.split('_')[-1].split('.')[0]))
                    if png_files:
                        sequence_name = rel_path
                        num_frames = len(png_files)

                        durations = [0.15] * num_frames if 'idle' in sequence_name else [0.05] * num_frames
                        settings['sequences'][sequence_name] = {
                            'offset': [0, 0],
                            'rate': 1.0,
                            'repeat': True,
                            'frozen': False,
                            'durations': durations
                        }

                if settings['sequences']:
                    try:
                        with open(config_path, 'w') as f:
                            json.dump(settings, f, indent=4)
                        print(f"Generated config.json for {object_dir}")
                    except Exception as e:
                        print(f"Error writing config for {object_dir}: {e}")

            resources = load_img_directory(object_path, colorkey=settings.get('transparency', [0, 0, 0]))
            self.assets[settings['uid']] = ObjectData(settings, resources)
