import sys
import pygame
from cms.entities import entities
from rest.event_system import EventSystem
from collections import deque

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.entities = entities.copy()
        self.event_system = EventSystem()
        self.event_queue = deque()
        
        self.encounter_ready = False
        
        self.queue_event('encounter_start', {})
    
    def queue_event(self, event_type: str, context: dict):
        self.event_queue.append((event_type, context))
    
    def process_events(self):
        results = []
        while self.event_queue:
            event_type, context = self.event_queue.popleft()
            event_results = self.event_system.trigger_event(event_type, context, self)
            results.extend(event_results)
        return results
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.queue_event('space', {'entity_id': '1'})
        return True
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            
            if not self.encounter_ready:
                self.queue_event('encounter_ready', {})
                self.encounter_ready = True
            
            running = self.handle_input()
            
            results = self.process_events()
            for result in results:
                print(result)
            
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    import content.test_interactor
    Game().run()