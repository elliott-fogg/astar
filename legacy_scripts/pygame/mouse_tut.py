import pygame
import random
pygame.init()

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
RED   = (255,  0,  0)
PI = 3.141592653

size = (700,500)
screen = pygame.display.set_mode(size)
done = False
pygame.display.set_caption("Mouse-work Tutorial")
clock = pygame.time.Clock()

# initialise variables
pygame.mouse.set_visible(False)
rect_x = 50
rect_y = 50
xv = 0
yv = 0

# Main Program Loop
while not done:
	# Main Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				xv = -3
			elif event.key == pygame.K_RIGHT:
				xv = 3
			elif event.key == pygame.K_UP:
				yv = -3
			elif event.key == pygame.K_DOWN:
				yv = 3
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				xv = 0
			elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				yv = 0
	# Game Logic
	pos = pygame.mouse.get_pos()
	xpos = pos[0]
	ypos = pos[1]
	mouse_pressed = pygame.mouse.get_pressed()
	lpress = mouse_pressed[0]

	rect_x += xv
	rect_y += yv

	if rect_x > size[0] - 50:
		rect_x = size[0] - 50
	elif rect_x < 0:
		rect_x = 0
	if rect_y > size[1] - 50:
		rect_y = size[1] - 50
	elif rect_y < 0:
		rect_y = 0
	# Clear The Screen
	screen.fill(BLACK)
	# Drawing
	font = pygame.font.SysFont('Calibri', 25, True, False)
	text = font.render("x: "+str(xpos)+", y: "+str(ypos)+", Mouse Pressed: "+str(mouse_pressed), True, WHITE, 1)
	screen.blit(text, [250, 250])
	pygame.draw.rect(screen,RED,[rect_x,rect_y,50,50],0)
	pygame.draw.circle(screen,WHITE,[xpos,ypos],2)
	# "Drawing" adds it to the drawing board. Flipping the screen draws the contents of the drawing board on the screen.
	pygame.display.flip()
	clock.tick(60)

print("Quitting...")
pygame.quit()