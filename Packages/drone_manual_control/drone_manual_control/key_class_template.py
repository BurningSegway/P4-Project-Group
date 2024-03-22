import pygame
from pygame.locals import *
import time


class capture():
    def __init__(self):


        # Initialize Pygame
        pygame.init()

        # Set up the screen dimensions
        SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Key Capture")

        self.pitch = 0
        self.roll = 0
        self.throttle = 0
        self.yaw = 0

        self.run_window()

    def run_window(self):

        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.pitch = 0
                    self.roll = 0
                    self.throttle = 0
                    self.yaw = 0
                    running = False

                elif event.type == KEYDOWN:
                    # Check for specific key presses
                    if event.key == K_ESCAPE:
                        self.pitch = 0
                        self.roll = 0
                        self.throttle = 0
                        self.yaw = 0
                        running = False
                    if event.key == K_SPACE:
                        self.pitch = 0
                        self.roll = 0
                        self.throttle = 0
                        self.yaw = 0
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.throttle = self.throttle + 50
                if self.throttle > 1000:
                    self.throttle = 1000

            if keys[pygame.K_s]:
                self.throttle = self.throttle - 50
                if self.throttle < 0:
                    self.throttle = 0
            
            if keys[pygame.K_q]:
                self.yaw = -300

            if keys[pygame.K_e]:
                self.yaw = 300
            elif not keys[pygame.K_e] and not keys[pygame.K_q]:
                self.yaw = 0

            if keys[pygame.K_UP]:
                self.pitch = 300        

            if keys[pygame.K_DOWN]:
                self.pitch = -300

            elif not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self.pitch = 0
            
            if keys[pygame.K_LEFT]:
                self.roll = -300
            
            if keys[pygame.K_RIGHT]:
                self.roll = 300
            
            elif not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.roll = 0

            print(f"Control input:\nPitch: {self.pitch}\t Roll: {self.roll}\t Throttle: {self.throttle}\t Yaw: {self.yaw}")
            # Update the display
            pygame.display.flip()
            time.sleep(0.1)

        # Quit Pygame
        pygame.quit()


keycap = capture()
