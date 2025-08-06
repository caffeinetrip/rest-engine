
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Settings:
    window_size: Tuple[int, int]
    display_size: Tuple[int, int]
    
    fps_cap: int
    tile_size: int
    
    camera_slowness: float
    
    caption: str | None
    
    screens: List[str]
    
    sound_path: str | None
    font_path: str | None
    spritesheets_path: str | None
    entities_path: str | None
    frag_path: str | None