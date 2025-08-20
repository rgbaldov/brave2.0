import pygame
from control.motor_driver import MotorDriver

def remote_control():
    pygame.init()
    screen = pygame.display.set_mode((100,100))
    md = MotorDriver()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            md.set_motor_speed(0, 1.0)
        elif keys[pygame.K_DOWN]:
            md.set_motor_speed(0, -1.0)
        else:
            md.set_motor_speed(0, 0.0)

if __name__ == "__main__":
    remote_control()
