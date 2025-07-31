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
    def add_event(self, event_type: str, context: dict):
        self.event_queue.append((event_type, context))
    
    # do event
    def process_all_events(self):
        results = []
        
        while self.event_queue:
            event_type, context = self.event_queue.popleft()
            event_results = self.event_system.trigger_event(event_type, context, self)
            results.extend(event_results)
            
        return results
    
    def update(self):
        pass
    
    def run(self):
        self.load()
        self.add_event('encounter_ready', {})
        
        while True:
            self.update()
    
    def end(self):
        pygame.quit()
        sys.exit()

    # def run(self):
    #     clock = pygame.time.Clock()
    #     running = True
        
    #     while running:
            
    #         if not self.encounter_ready:
    #             self.queue_event('encounter_ready', {})
    #             self.encounter_ready = True
            
    #         running = self.handle_input()
            
    #         results = self.process_events()
    #         for result in results:
    #             print(result)
            
    #         self.screen.fill((0, 0, 0))
    #         pygame.display.flip()
    #         clock.tick(60)
        
    #     pygame.quit()
    #     sys.exit()
