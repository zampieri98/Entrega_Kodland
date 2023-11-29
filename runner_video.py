import pygame
from sys import exit			# importamos comando para cerrar el programa
from random import randint

def display_score():
	current_time = round((pygame.time.get_ticks() - start_time)/1000)
	score_surf = game_font.render(f"{current_time}", False, (64,64,64))
	score_rect = score_surf.get_rect(center=(400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_rect_list:

			if obstacle_rect.bottom == 300: 
				screen.blit(snail_surf, obstacle_rect)
				obstacle_rect.x -= 5
			else: 
				if obstacle_rect.bottom == 210:
					screen.blit(fly_surf, obstacle_rect)
					obstacle_rect.x -= 5
				else: 
					screen.blit(spider_surf, obstacle_rect)
					obstacle_rect.x -= 7

		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
		return obstacle_list
	else: return []

def collisions(player, obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if player.colliderect(obstacle_rect): return False
	return True

def player_animation():
	global player_surf, player_index

	if player_rect.bottom < 300:
		player_surf = player_jump
	else:
		player_index += 0.1 							# actualizo cada 10 frames
		if player_index >= len(player_walk):player_index = 0
		player_surf = player_walk[int(player_index)]

def select_player():
	global player_walk, player_jump, player_surf, player_index, player_stand, switch_surf

	player_walk1 = pygame.image.load("graphics/Player"+str(jugador)+"/player_walk_1.png").convert_alpha()
	player_walk2 = pygame.image.load("graphics/Player"+str(jugador)+"/player_walk_2.png").convert_alpha()
	player_walk = [player_walk1,player_walk2]
	player_index= 0
	player_jump = pygame.image.load("graphics/Player" + str(jugador) +"/jump.png").convert_alpha()
	player_surf = player_walk[player_index]
	player_rect = player_surf.get_rect(bottomright = (80,300))
	player_stand = pygame.image.load("graphics/Player"+str(jugador)+"/player_stand.png").convert_alpha()
	player_stand = pygame.transform.rotozoom(player_stand, 0, 1.75)

	switch_surf = pygame.image.load("graphics/Extras/switch" + str(jugador) +".png").convert_alpha()



pygame.init()
screen = pygame.display.set_mode((800,400))				# tamaño de la ventana
pygame.display.set_caption("Runner")					# nombre de la ventana
clock = pygame.time.Clock()
game_font = pygame.font.Font("font/Pixeltype.ttf",50)	# tipo de letra
menu_font = pygame.font.Font("font/Pixeltype.ttf",30)	# tipo de letra
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()



# Snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]



# Fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]


# spider
spider_frame_1 = pygame.image.load("graphics/spider/spider1.png").convert_alpha()
spider_frame_2 = pygame.image.load("graphics/spider/spider2.png").convert_alpha()
spider_frames = [spider_frame_1, spider_frame_2]
spider_frame_index = 0
spider_surf = spider_frames[spider_frame_index]



obstacle_rect_list = []


# Dificultad
dif = 1
flecha = pygame.image.load("graphics/Extras/flecha.png").convert_alpha()
flecha1 = pygame.transform.rotozoom(flecha, 270, 0.5)
flecha1_rect = flecha1.get_rect(center = (650,250))

flecha2 = pygame.transform.rotozoom(flecha, 90, 0.5)
flecha2_rect = flecha2.get_rect(center = (650,150))


# Player
jugador = 1
select_player()

player_rect = player_surf.get_rect(bottomright = (80,300))
player_gravity = 0

switch_rect = switch_surf.get_rect(center = (100,300))


# Intro screen
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = game_font.render("Pixel Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = game_font.render("< Seleccionar personaje >", False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))



# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

spider_animation_timer = pygame.USEREVENT + 5
pygame.time.set_timer(spider_animation_timer, 200)



while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	
		if game_active:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom == 300:
					player_gravity = -20
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = pygame.time.get_ticks()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
				if jugador == 0: jugador = 1
				else: jugador = 2
				select_player()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
				if jugador == 2: jugador = 1
				else: jugador = 0
				select_player()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				if dif == 2: dif = 1
				else: dif = 0
				select_player()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				if dif == 0: dif = 1
				else: dif = 2
				select_player()

			

		if game_active:
			if event.type == obstacle_timer:
				
				if dif == 2:
					num_rand = randint(0,6)
				else:
					if dif == 1:
						num_rand = randint(0,4)
					else:
						num_rand = randint(0,2)

				if num_rand <=2:
					obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
				else:
					if num_rand >=2 and num_rand <=4: 
						obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))
					else: 
						obstacle_rect_list.append(spider_surf.get_rect(bottomright = (randint(900,1100),299)))

			if event.type == snail_animation_timer:
				if snail_frame_index == 0: snail_frame_index = 1
				else: snail_frame_index = 0
				snail_surf = snail_frames[snail_frame_index]

			if event.type == fly_animation_timer:
				if fly_frame_index == 0: fly_frame_index = 1
				else: fly_frame_index = 0
				fly_surf = fly_frames[fly_frame_index]

			if event.type == spider_animation_timer:
				if spider_frame_index == 0: spider_frame_index = 1
				else: spider_frame_index = 0
				spider_surf = spider_frames[spider_frame_index]



	if game_active:
		screen.blit(sky_surf,(0,0))
		screen.blit(ground_surf,(0,300))
		score = display_score()

		# Player
		player_gravity += 1
		player_rect.y += player_gravity
		if player_rect.bottom >= 300: player_rect.bottom = 300
		player_animation()
		screen.blit(player_surf,player_rect)

		# Obstacle movement
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)

		# Collision
		game_active = collisions(player_rect, obstacle_rect_list)

	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)
		screen.blit(switch_surf,switch_rect)
		obstacle_rect_list.clear()
		player_rect.midbottom = (80,300)



		if dif == 0:
			difficulty_message = game_font.render("Inicial", False, (0,100,0))
		else:
			if dif == 1:
				difficulty_message = game_font.render("Intermedio", False, (0,0,100))
			else: difficulty_message = game_font.render("Imposible", False, (100,0,0))

		difficulty_message_rect = difficulty_message.get_rect(center=(650,200))
		screen.blit(difficulty_message, difficulty_message_rect)
		screen.blit(flecha1, flecha1_rect)
		screen.blit(flecha2, flecha2_rect)


		score_message = game_font.render(f"Your score: {score}", False, (111,196,169))
		score_message_rect = score_message.get_rect(center=(400,350))
		screen.blit(game_name, game_name_rect)

		Mensaje = menu_font.render("Presionar espacio para iniciar", False, (0,0,0))
		Mensaje_rect = Mensaje.get_rect(center=(400,390))
		screen.blit(Mensaje, Mensaje_rect)


		if score == 0:	screen.blit(game_message, game_message_rect)
		else: screen.blit(score_message,score_message_rect)


	pygame.display.update()
	clock.tick(60)										# tasa de refrescado