import sys
import pygame
from collections import deque

class Game:
    def __init__(self):
        self.event_queue = deque()
        self.add_event('encounter_start', {})
    
    def load(self):
        pass
    
    # add event
    def add_event(self, event_type: str, context: dict, entity=None):
        self.event_queue.append((event_type, context, entity))
    
    # do event
    def process_all_events(self):
        results = []

        while self.event_queue:
            event_type, context, entity = self.event_queue.popleft()
            event_results = self.event_system.trigger_event(event_type, context, entity)
            results.extend(event_results)
            
        return results
    
    def update(self):
        pass
    
    def run(self):
        self.load()
        self.add_event('encounter_ready', {})
        
        while True:
            self.process_all_events()
            self.update()
    
    def end(self):
        pygame.quit()
        sys.exit()
