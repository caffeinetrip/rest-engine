import math
import pygame
import random
from typing import List, Tuple, Union

from rest.utils.cms import CMSEntity

# List[state | mirror]
state_dict = {
    0: ['right', False],
    90: ['top', False],
    180: ['right', True],
    270: ['down', True]
}

degrees_dict = {
    ('top', False): 90,
    ('down', False): 270,
    ('right', True): 180,
    ('right', False): 0
}

def normalize(v: int, amt: int, target: int = 0) -> int:
    if v > target + amt:
        v -= amt
    elif v < target - amt:
        v += amt
    else:
        v = target
    return v

def rectify(p1: Tuple[int, int], p2: Tuple[int, int]) -> pygame.Rect:
    tl = (min(p1[0], p2[0]), min(p1[1], p2[1]))
    br = (max(p1[0], p2[0]), max(p1[1], p2[1]))
    return pygame.Rect(*tl, br[0] - tl[0] + 1, br[1] - tl[1] + 1)

def box_points(rect: pygame.Rect) -> List[Tuple[int, int]]:
    points = []
    for y in range(rect.height):
        for x in range(rect.width):
            points.append((rect.x + x, rect.y + y))
    return points

def advance(vec: List[float], angle: float, amt: float) -> List[float]:
    vec[0] += math.cos(angle) * amt
    vec[1] += math.sin(angle) * amt
    return vec

def distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def randint_excluding_ranges(start: int, end: int, forbidden_ranges: List[Tuple[int, int]]) -> int:
    while True:
        num = random.randint(start, end)
        if all(not (low <= num <= high) for low, high in forbidden_ranges):
            return num

def calculate_angle(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:

    mouse_x, mouse_y = [pos1[0], pos1[1]]
    screen_x, screen_y = pos2
    angle_rad = math.atan2((screen_y - mouse_y) * -1, (screen_x - mouse_x) * -1)
    return round(math.degrees(angle_rad))

def scale_mouse_pos(mouse_pos: Tuple[int, int], original_size: Tuple[int, int], target_size: Tuple[int, int]) -> Tuple[int, int]:
    mouse_x, mouse_y = mouse_pos
    orig_w, orig_h = original_size
    target_w, target_h = target_size

    scaled_x = mouse_x * (target_w / orig_w)
    scaled_y = mouse_y * (target_h / orig_h)

    return round(scaled_x), round(scaled_y)

def convert_string_to_list(string: str) -> List[Union[int, float]]:
    if not isinstance(string, str):
        raise TypeError("Input must be a string")

    parts = string.split(',')

    numbers = []
    for part in parts:
        try:
            number = float(part.strip())
            if number.is_integer():
                number = int(number)
            numbers.append(number)
        except ValueError:
            raise ValueError(f'Unable to convert "{part}" to a number')
    
    return numbers

def get_rotate(current_degrees: int, target_degrees: int, rotate_speed: int) -> int:
    
    if current_degrees == 0 and target_degrees == 270:
        return 359
        
    elif current_degrees >= 270 and target_degrees == 0:
        target_degrees = 360
    
    if target_degrees - rotate_speed * 2 < current_degrees < target_degrees + rotate_speed * 2:
        return target_degrees - current_degrees
    
    
    if target_degrees - current_degrees > 0: 
        return rotate_speed
    
    else:
        return rotate_speed * -1

def get_state(current_degrees: int) -> List[str | bool] | None:
    
    if current_degrees in state_dict.keys():
        return state_dict[current_degrees] # type: ignore
    
    elif current_degrees > 0 and current_degrees <= 90:
        return ['rotate/right_top', False]
    
    elif current_degrees > 90 and current_degrees <= 180:
        return ['rotate/right_top', True]
    
    elif current_degrees > 180 and current_degrees <= 270:
        return ['rotate/right_down', True]
    
    elif current_degrees > 270 and current_degrees <= 360:
        return ['rotate/right_down', False]
    
    return None

def get_state_in_diapasone(current_degrees: int) -> str:
    
    if current_degrees == 0 and current_degrees <= 90:
        return 'idle/top'
    
    elif current_degrees == 90 and current_degrees <= 180:
        return 'idle/right'
    
    elif current_degrees == 180 and current_degrees <= 270:
        return 'idle/down'
    
    elif current_degrees == 270 and current_degrees <= 360:
        return 'idle/right'
    
    return 'idle/right'