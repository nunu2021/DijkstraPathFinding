import pygame

pygame.init()
screen = pygame.display.set_mode([500, 500])

BLACK = (0, 0, 0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
pink = (255,192,203)
orange = (255, 165, 0)
purple = (128,0,128)
white = (255, 255, 255)
maroon = (128,0,0)
darkgreen = 	(0,100,0)
gray = (211,211,211)
cyan = (0,255,255)
WINDOW_WIDTH = 400

screen.fill(white)


def drawGrid(x1, y1, array):
    blockSize = (WINDOW_WIDTH - 50)/x1  # Set the size of the grid block
    for x in range(x1):
        for y in range(y1):
            rect = pygame.Rect(y * blockSize, x * blockSize,
                               blockSize, blockSize)
            if array[x][y] == 0: #
                pygame.draw.rect(screen, BLACK, rect)

            elif array[x][y] == 1: #
                pygame.draw.rect(screen, red, rect)
            elif array[x][y] == 2: #
                pygame.draw.rect(screen, green, rect)
            elif array[x][y] == 3: #
                pygame.draw.rect(screen, blue, rect)
            elif array[x][y] == 4: #
                pygame.draw.rect(screen, yellow, rect)
            elif array[x][y] == 5: #
                pygame.draw.rect(screen, pink, rect)
            elif array[x][y] == 6: #
                pygame.draw.rect(screen, orange, rect)
            elif array[x][y] == 7: #
                pygame.draw.rect(screen, purple, rect)
            elif array[x][y] == 8: #
                pygame.draw.rect(screen, white, rect)
            elif array[x][y] == 9: #
                pygame.draw.rect(screen, maroon, rect)
            elif array[x][y] == 10: #
                pygame.draw.rect(screen, darkgreen, rect)
            elif array[x][y] == 11: #
                pygame.draw.rect(screen, gray, rect)
            elif array[x][y] == 12: #
                pygame.draw.rect(screen, cyan, rect)

            else:
                pygame.draw.rect(screen, BLACK, rect)



# Run until the user asks to quit
def mainRun():
    running = True
    while True:
        flow = [[1, 0, 2, 0, 4],
                [0, 0, 3, 0, 6],
                [0, 0, 0, 0, 0],
                [0, 2, 0, 4, 0],
                [0, 1, 3, 6, 0]]

        drawGrid(len(flow), len(flow[0]), flow)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    # Done! Time to quit.

    pygame.quit()

mainRun()

