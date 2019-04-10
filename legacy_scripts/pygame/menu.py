def main():

	import pygame
	pygame.init()
	global screen, size

	BLACK = (  0,  0,  0)
	WHITE = (255,255,255)
	BLUE  = (  0,  0,255)
	GREEN = (  0,255,  0)
	RED   = (255,  0,  0)
	SKY   = ( 90,135,255)
	PI = 3.141592653

	def draw_button(colour1,label,colour2,y,width=0):
		# Creates a button, centered on the screen, with the top at coord_y.
		# Returns the limits of the button in the form [x_min, x_max, y_min, y_max].
		global screen, size
		b_font = pygame.font.SysFont('Calibri',25,True,False)
		b_text = b_font.render(label,True,colour2,1)
		b_text_width = b_text.get_width()
		b_text_height = b_text.get_height()
		b_height = b_text_height * 2
		if width != 0:
			b_width = width
		else:
			b_width = b_text_width + 50
		x = (size[0] - b_width)/2
		pygame.draw.rect(screen, colour1, [x, y, b_width, b_height], 0)
		screen.blit(b_text,[x + (b_width - b_text_width)/2, y + (b_height - b_text_height)/2])
		return [x, x + b_width, y, y + b_height]

	def draw_title(y,colour,label,fsize):
		global size, screen
		t_font = pygame.font.SysFont('Calibri',fsize,True,False)
		t_text = t_font.render(label,True,colour,1)
		t_text_width = t_text.get_width()
		x = (size[0] - t_text_width)/2
		screen.blit(t_text,[x,y])

	size = (400,500)
	screen = pygame.display.set_mode(size)
	done = False
	pygame.display.set_caption("Menu")
	clock = pygame.time.Clock()
	choice = 0

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					done = True
			elif event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0] == 1:
					xpos = pygame.mouse.get_pos()[0]
					ypos = pygame.mouse.get_pos()[1]
					if button1[0] < xpos < button1[1] and button1[2] < ypos < button1[3]:
						choice = 1
						done = True
						break
					if button2[0] < xpos < button2[1] and button2[2] < ypos < button2[3]:
						choice = 2
						done = True
						break
					if button3[0] < xpos < button3[1] and button3[2] < ypos < button3[3]:
						choice = 3
						done = True
						break
					if button0[0] < xpos < button0[1] and button0[2] < ypos < button0[3]:
						choice = 0
						done = True
						break 
		# Clear the screen
		screen.fill(WHITE)
		# Draw
		draw_title(20,BLACK,"2D Map Creator",50)
		draw_title(80,BLACK,"Select Mode:",30)
		button1 = draw_button(SKY,"New Map",WHITE,150)
		button2 = draw_button(SKY,"Import Map",WHITE,200)
		button3 = draw_button(SKY,"Pathing",WHITE,250)
		button0 = draw_button(SKY,"Quit",WHITE,300)
		# Flip the screen
		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
	return choice