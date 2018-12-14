import pygame
import random
pygame.init()

def new_snow(size, radius, mode):
	x = random.randrange(0,size[0])
	vx = random.randrange(-5,5)
	vy = random.randrange(5,10)
	if mode == 0:
		y = random.randrange(0,size[1])
	else:
		y = -2 * radius
	return [x,y,vx,vy]

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
snow_list = []
snow_num = 50
radius = 2
for i in range(snow_num):
	snow_list.append(new_snow(size,radius,0))

# Main Program Loop
while not done:
	# Main Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Game Logic

	# Clear The Screen
	screen.fill(BLACK)
	# Drawing
	for snow in snow_list:
		snow[0] += snow[2]
		snow[1] += snow[3]
		if snow[0] < -radius or snow[0] > size[0] + radius or snow[1] > size[1] + radius:
			snow[:] = new_snow(size,radius,1)
		pygame.draw.circle(screen,WHITE,[snow[0],snow[1]],radius)

	# "Drawing" adds it to the drawing board. Flipping the screen draws the contents of the drawing board on the screen.
	pygame.display.flip()
	clock.tick(60)
print("Quitting...")
pygame.quit()
