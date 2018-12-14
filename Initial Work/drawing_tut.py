import pygame
pygame.init()

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
RED   = (255,  0,  0)
PI = 3.141592653

size = (700,500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Drawing Tutorial")
font = pygame.font.SysFont('Calibri', 25, True, False)

done = False
clock = pygame.time.Clock()
# Main Program Loop
while not done:
	# Main Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Game Logic
	
	# Clear The Screen
	screen.fill(WHITE)
	# Drawing
	# pygame.draw.line(desired_screen, colour, [start_coords],[end_coords],thickness)
	# pygame.draw.rect(desired_screen, colour, [left_x, top_y, width, height], thickness)
	# pygame.draw.ellipse(desired_screen, colour, [bound_rectangle_left_x, b_r_top_y, width, height], thickness)
	# pygame.draw.arc(screen,colour,[b_r_left_x,b_r_top_y,ellipse_width,ellipse_height],angle_start,angle_stop,thickness)
	# pygame.draw.polygon(screen,colour,[POINTS],thickness)
		# To Draw Text on 'screen':
		# font = pygame.font.SysFont('font_here',size,T/F_bold,T/F_italics)
		# text = font.render("text_here",T/F_anti-aliased,colour)
		# screen.blit(text,[position])
	# NOTE: Setting a rectangle to have thickness 0 will cause it to be filled.
	pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
	for y_offset in range(0, 100, 10):
		pygame.draw.line(screen, RED, [0, 10 + y_offset], [100, 110 + y_offset], 5)
	pygame.draw.rect(screen, BLACK, [20, 20, 250, 100], 2)
	pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2)
	pygame.draw.arc(screen, BLACK, [20, 220, 250, 200], 0, PI / 2, 2)
	pygame.draw.arc(screen, GREEN, [20, 220, 250, 200], PI / 2, PI, 2)
	pygame.draw.arc(screen, BLUE, [20, 220, 250, 200], PI, 3 * PI / 2, 2)
	pygame.draw.arc(screen, RED, [20, 220, 250, 200], 3 * PI / 2, 2 * PI, 2)
	pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)
	text = font.render("hello", True, BLACK, 1)
	screen.blit(text, [250, 250])

	pygame.draw.rect(screen, GREEN,[0,0,600,400],0)
	pygame.draw.ellipse(screen, RED, [0,0,600,400],0)
	
	# "Drawing" adds it to the drawing board. Flipping the screen draws the contents of the drawing board on the screen.
	pygame.display.flip()
	clock.tick(60)
print("Quitting...")
pygame.quit()
