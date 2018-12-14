# This script sets up the creation of a new map, to be passed to map_edit.py
# Maybe try and find and/or create some input box in pygame to allow the user to type in dimensions and names
# Set up dimensions and name-of-map and return
def main():

	import pygame
	pygame.init()
	global screen, size
	size = (400,500)

	def draw_title(y,colour,label,fsize):
		global size, screen
		t_font = pygame.font.SysFont('Calibri',fsize,True,False)
		t_text = t_font.render(label,True,colour,1)
		t_text_width = t_text.get_width()
		x = (size[0] - t_text_width)/2
		screen.blit(t_text,[x,y])

	def input_box(y,bool_int,maxlength,font_size):
		global size, screen
		input_font = pygame.font.SysFont('Calibri',font_size,False,True)
		test_text = input_font.render('K'*maxlength,True,(0,0,0),1)
		text_width = test_text.get_width()
		box_width = text_width + 100
		
	
	

	screen = pygame.display.set_mode(size)
	done = False
	pygame.display.set_caption("New Map")
	clock = pygame.time.Clock()

	while not done:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				pass
				# Check if left_mouse_pressed
				