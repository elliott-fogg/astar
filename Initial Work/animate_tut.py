import pygame
pygame.init()

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
RED   = (255,  0,  0)
PI = 3.141592653

C0 = ( 50, 50, 50)
C1 = (100,100,100)
C2 = (150,150,150)

size = (700,500)
screen = pygame.display.set_mode(size)
done = False
pygame.display.set_caption("Animation Tutorial")
clock = pygame.time.Clock()

# initialise variables
rect_x = 50
rect_y = 50
rect_h = 50
rect_w = 50
v_x = 8
v_y = 5
ghosts = [[rect_x,rect_y]]*25

# Main Program Loop
while not done:
	# Main Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Game Logic
	rect_x += v_x
	rect_y += v_y

	ghosts[24] = [rect_x,rect_y]
	for i in range(24):
		ghosts[i] = ghosts[i+1]

	if rect_x + rect_w > size[0] or rect_x < 0:
		v_x *= -1
	if rect_y + rect_h > size[1] or rect_y < 0:
		v_y *= -1

	# Clear The Screen
	screen.fill(BLACK)
	# Drawing
	for g in range(25):
		pygame.draw.rect(screen,(g*10,g*10,g*10),[ghosts[g][0],ghosts[g][1],rect_w,rect_h])
#	pygame.draw.rect(screen,C0,[ghosts[0][0],ghosts[0][1],rect_w,rect_h])
#	pygame.draw.rect(screen,C1,[ghosts[5][0],ghosts[5][1],rect_w,rect_h])
#	pygame.draw.rect(screen,C2,[ghosts[10][0],ghosts[10][1],rect_w,rect_h])
#	pygame.draw.rect(screen,BLACK,[rect_x,rect_y,rect_w,rect_h],1)
#	pygame.draw.rect(screen,RED,[rect_x+10,rect_y+10,rect_w-20,rect_h-20])

	# "Drawing" adds it to the drawing board. Flipping the screen draws the contents of the drawing board on the screen.
	pygame.display.flip()
	clock.tick(60)
print("Quitting...")
pygame.quit()
