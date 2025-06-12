import pygame
# pygame setup
pygame.init()
WIDTH, HEIGHT = 900, 900
margin = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if pygame.mouse.get_pressed()[0]:
        print(pygame.mouse.get_pos())
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    pygame.draw.line(screen, "black", (350, 150), (350,750), width = 3)
    pygame.draw.line(screen, "black", (550, 150), (550,750), width = 3)
    pygame.draw.line(screen, "black", (150, 350), (750, 350), width= 3)
    pygame.draw.line(screen, "black", (150, 550), (750, 550), width= 3)

    


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()