import sys
import time
import pygame
from .. import G
from ..utils.io import read_json

class InputState:
    def __init__(self):
        self.pressed = False
        self.just_pressed = False
        self.just_released = False
        self.held_since = 0

    def update(self):
        self.just_pressed = False
        self.just_released = False

    def press(self):
        self.pressed = True
        self.just_pressed = True
        self.held_since = time.time()

    def unpress(self):
        self.pressed = False
        self.just_released = True

class Mouse:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.ui_pos = pygame.Vector2(0, 0)
        self.movement = pygame.Vector2(0, 0)

    def update(self):
        mpos = pygame.mouse.get_pos()
        self.movement = pygame.Vector2(mpos) - self.pos
        self.pos = pygame.Vector2(mpos)
        self.ui_pos = self.pos // 2

class Input:
    def __init__(self, path=None):
        self.state = 'main'
        self.text_buffer = None
        self.path = path
        self.config = self._load_config(path)
        self.config['__backspace'] = ['button', pygame.K_BACKSPACE]
        self.input_states = {key: InputState() for key in self.config}
        self.hidden_keys = ['__backspace']
        self.repeat_rate = 0.02
        self.repeat_delay = 0.5
        self.repeat_timers = {key: 0 for key in self.config}
        self.shift = False
        self.mouse = Mouse()

    def _load_config(self, path):
        if not path:
            return {}
        try:
            return read_json(path)
        except (IOError, ValueError) as e:
            print(f"Failed to load input config from {path}: {e}")
            return {}

    def _get_char_from_key(self, key, shift):
        if key == pygame.K_SPACE:
            return ' '
        name = pygame.key.name(key)
        if len(name) == 1:
            char = name
            if shift:
                char = char.upper() if char.isalpha() else self._get_shifted_char(char)
            return char
        return None

    def _get_shifted_char(self, char):
        shift_mappings = {
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '-': '_', '=': '+', '[': '{', ']': '}', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?', '\\': '|'
        }
        return shift_mappings.get(char, char)

    def pressed(self, key):
        return self.input_states.get(key, InputState()).just_pressed

    def holding(self, key):
        return self.input_states.get(key, InputState()).pressed

    def released(self, key):
        return self.input_states.get(key, InputState()).just_released

    def set_text_buffer(self, text_buffer=None):
        self.text_buffer = text_buffer

    def update(self):
        for state in self.input_states.values():
            state.update()
        self.mouse.update()
        current_time = G.window.time if G.window else time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                G.game.end()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_press(event.button)
                G.event_system.trigger_event('mouse_press', {'button': event.button})
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_release(event.button)
                G.event_system.trigger_event('mouse_release', {'button': event.button})
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event, current_time)
                if event.key != pygame.K_BACKSPACE:
                    G.event_system.trigger_event('key_press', {'key': event.key})
            elif event.type == pygame.KEYUP:
                self._handle_key_release(event)
                G.event_system.trigger_event('key_release', {'key': event.key})

        if self.text_buffer and self.holding('__backspace'):
            if current_time > self.repeat_timers['__backspace'] + self.repeat_delay:
                if current_time > self.repeat_timers['__backspace'] + self.repeat_rate:
                    self.repeat_timers['__backspace'] = current_time
                    self.text_buffer.delete()

    def _handle_mouse_press(self, button):
        for key, (input_type, value) in self.config.items():
            if input_type == 'mouse' and value == button:
                self.input_states[key].press()

    def _handle_mouse_release(self, button):
        for key, (input_type, value) in self.config.items():
            if input_type == 'mouse' and value == button:
                self.input_states[key].unpress()

    def _handle_key_press(self, event, current_time):
        if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.shift = True
            return
        if self.text_buffer:
            if event.key == pygame.K_BACKSPACE:
                self.input_states['__backspace'].press()
                self.repeat_timers['__backspace'] = current_time
                self.text_buffer.delete()
            elif event.key == pygame.K_RETURN:
                self.text_buffer.enter()
            else:
                char = self._get_char_from_key(event.key, self.shift)
                if char:
                    self.text_buffer.insert(char)
        else:
            for key, (input_type, value) in self.config.items():
                if input_type == 'button' and value == event.key:
                    self.input_states[key].press()

    def _handle_key_release(self, event):
        if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
            self.shift = False
        for key, (input_type, value) in self.config.items():
            if input_type == 'button' and value == event.key:
                self.input_states[key].unpress()
