import rclpy
import sys
import pygame
from pygame.locals import *

from rclpy.node import Node

from drone_msgs.msg import Control

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('keyboard_publisher')
        self.publisher_ = self.create_publisher(Control, 'control_input', 10)

        time_msg = 0.1  # seconds
        time_key = 0.05
        self.timer = self.create_timer(time_msg, self.msg_callback)
        self.timer_key = self.create_timer(time_key, self.key_capture)

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

    def key_capture(self):

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
            self.throttle = self.throttle + 5 # husk at ændre den her tilbage til self.throttle + 5
            if self.throttle > 1000:
                self.throttle = 1000

        if keys[pygame.K_s]:
            self.throttle = self.throttle - 10
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

        #print(f"Control input:\nPitch: {self.pitch}\t Roll: {self.roll}\t Throttle: {self.throttle}\t Yaw: {self.yaw}")
        # Update the display
        pygame.display.flip()

    def msg_callback(self):
        msg = Control()
        temp = self.get_clock().now()
        msg.stamp = temp.nanoseconds
        msg.roll = float(self.roll)
        msg.pitch = float(self.pitch)
        msg.throttle = float(self.throttle)
        msg.yaw = float(self.yaw)
        self.publisher_.publish(msg)
        self.get_logger().info(f"Control input: \n Roll: {self.roll}\t Pitch: {self.pitch}\t Throttle: {self.throttle}\t Yaw: {self.yaw}")

def main(args=None):
    rclpy.init(args=args)

    keyboard_publisher = MinimalPublisher()

    rclpy.spin(keyboard_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pygame.quit()
    keyboard_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
