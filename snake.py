# import modules
import pygame
import random

WIDTH = 800 # width of the screen
HEIGHT = 600 # height of the screen
BLOCK_SIZE = 40 # Set a block size for the pattern

class Block():
	def __init__(self, eyes, x, y, xdir, ydir, color):
		self.x = x
		self.y = y
		self.rect = pygame.Rect((self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))
		self.xdir = xdir
		self.ydir = ydir
		self.eyes = eyes
		self.color = color

	def draw(self, surface):
		# draw rectangle
		pygame.draw.rect(surface, self.color, self.rect)

		# draw eyes for the head
		if self.eyes:
			pygame.draw.circle(surface, "black",
				(self.x + BLOCK_SIZE / 3, self.y + BLOCK_SIZE / 3), BLOCK_SIZE / 10)
			pygame.draw.circle(surface, "black",
				(self.x + BLOCK_SIZE * 2 / 3, self.y + BLOCK_SIZE/3), BLOCK_SIZE/10)

	def update(self, turns, position, xdir, ydir, body):
		# update xdir and ydir (if the snake is turning)
		for t in turns:
			# check if the updated block is in the turn
			if position == turns[t]:
				# treat the head: give it the dir of the snake
				if turns[t] == 0:
					self.xdir = xdir
					self.ydir = ydir
				# treat the body: give it the dir of the previous block
				else:
					self.xdir = body[turns[t] - 1].xdir
					self.ydir = body[turns[t] - 1].ydir

		# update x and y
		self.x += BLOCK_SIZE * self.xdir
		self.y +=  BLOCK_SIZE * self.ydir

		# if snake goes out of the window, make it go to the other side
		if self.x >= WIDTH:
			self.x = 0
		if self.x < 0:
			self.x = WIDTH
		if self.y >= HEIGHT:
			self.y = 0
		if self.y < 0:
			self.y = HEIGHT
		
		self.rect = pygame.Rect((self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))


class Snake():
	def __init__(self, x, y):
		self.body = []
		self.x = x
		self.y = y
		self.xdir = 0
		self.ydir = 0
		self.turns = {}
		self.nb_turns = 0
		
		# create the head of the snake
		head = Block(True, self.x, self.y, self.xdir, self.ydir, "green")
		self.body.append(head)
	
	def draw(self, surface):
		for block in self.body:
			block.draw(surface)

	def update(self):
		# update each block's position
		for i in range(len(self.body), 0,  -1):
			# start by updating the last blocks of the body, and move to the heaad
			block = self.body[i - 1]
			block.update(self.turns, i - 1, self.xdir, self.ydir, self.body)

		# increment the counter to then turn the next block of the body
		for turn in self.turns.copy():
			self.turns[turn] += 1
			# when all blocks have been updated, remove the turn from the turns dict
			if self.turns[turn] > len(self.body):
				self.turns.pop(turn)

		# update the snake's position
		self.x = self.body[0].x
		self.y = self.body[0].y		


def init_window(surface):
	# Define the background colour
	surface.fill((0,0,0))

	# Create the grid
	# create all lines in a double loop
	for i in range(int(HEIGHT / BLOCK_SIZE)):
		for j in range(int(WIDTH / BLOCK_SIZE)):
			pygame.draw.line(surface, "grey", (0, BLOCK_SIZE * i), (WIDTH, BLOCK_SIZE * i))
			pygame.draw.line(surface, "grey", (BLOCK_SIZE * j, 0), (BLOCK_SIZE * j, HEIGHT))

	return surface


def main():
	# Init pygame
	pygame.init()

	# Create window
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	# Set the caption of the screen
	pygame.display.set_caption('🐍 Snake Game 🐍')

	# create the snake
	snake = Snake(80, 120)

	# create the candy at a random location
	candy = Block(False, random.randint(0, int(WIDTH / BLOCK_SIZE) - 1) * BLOCK_SIZE,
					random.randint(0, int(HEIGHT / BLOCK_SIZE) - 1)  * BLOCK_SIZE, 0, 0, "red")

	# create clock
	clock = pygame.time.Clock()

	# count the number of rounds
	rounds = 0

	# Variable to know that the game is running
	running = True

	# Loop to check for events
	while running:
		for event in pygame.event.get():
			# Check for QUIT event
			if event.type == pygame.QUIT:
				running = False
			# Check for direction key pressed
			if event.type == pygame.KEYDOWN:
				# update the snakes's direction
				if event.key == pygame.K_RIGHT:
					snake.xdir = 1
					snake.ydir = 0
				if event.key == pygame.K_LEFT:
					snake.xdir = -1
					snake.ydir = 0
				if event.key == pygame.K_UP:
					snake.xdir = 0
					snake.ydir = -1
				if event.key == pygame.K_DOWN:
					snake.xdir = 0
					snake.ydir = 1

				# add the new turn into the turns dict, and increment turn id
				snake.turns[snake.nb_turns] = 0
				snake.nb_turns += 1

		# Update snake
		snake.update()
		
		# Check if the snake's head reached the candy
		if snake.body[0].x == candy.x and snake.body[0].y == candy.y:
			# update the candy's position
			candy = Block(False, random.randint(0, int(WIDTH / BLOCK_SIZE) - 1) * BLOCK_SIZE,
					random.randint(0, int(HEIGHT / BLOCK_SIZE) - 1)  * BLOCK_SIZE, 0, 0, "red")
			# add a block to the snack
			# get the last block's info
			last = snake.body[len(snake.body) - 1]
			# add the block on a position depending on the snake's direction
			snake.body.append(Block(False, last.x + (last.xdir * (-1) * BLOCK_SIZE),
									last.y + (last.ydir * (-1) * BLOCK_SIZE), last.xdir, last.ydir, last.color))
			# update the rounds counter
			rounds += 1
		
		# Check if snake hits itself
		# Loop on the snake body - start to 1 to avoid the head
		for i in range(1, len(snake.body)):
			head = snake.body[0]
			block = snake.body[i]
			if head.x == block.x and head.y == block.y:
				# if collision, initialise the game
				rounds = 0
				snake = Snake(80, 120)
				candy = Block(False, random.randint(0, int(WIDTH / BLOCK_SIZE) - 1) * BLOCK_SIZE,
					random.randint(0, int(HEIGHT / BLOCK_SIZE) - 1)  * BLOCK_SIZE, 0, 0, "red")
				break

		# Init window
		screen = init_window(screen)

		# Draw
		candy.draw(screen)
		snake.draw(screen)

		# Update
		pygame.display.update()
		pygame.display.flip()

		# adapt the updates frequence according to the number of rounds
		clock.tick(min(rounds + 2, 15))

if __name__ == "__main__":
	main()