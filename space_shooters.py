# Space Game ISU
# Andrew Kang 599269
# ICS3U0 June 2019

# imports libraries to be used throughout the game program
import pygame, os, random, time

# initializes pygame
pygame.init()

# sets some colours that will be used throughout the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCORECOLOUR = (98, 226, 229)

# gets the background music file and plays it an infinite number of times
# background music file downloaded from https://www.youtube.com/watch?v=Zz4CFHiBpds
background_music = pygame.mixer.Sound(os.path.join('Game_Files', 'backgroundmusic.wav'))
background_music.play(-1)

# sets the screen size and window caption
screen_x = 600
screen_y = 600
screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("Space Shooters by Andrew Kang")

# imports the font for the score and sets the score to 0
# font downloaded from https://www.1001fonts.com/blackhole-bb-font.html
gamefont = pygame.font.Font(os.path.join('Game_Files', 'BlackHoleBB.ttf'), 70)
global score
score = 0

# all photos from https://opengameart.org/content/complete-spaceship-game-art-pack by sujit1717
backgroundPhoto = pygame.image.load(os.path.join('Game_Files', 'background.jpg' ))
backgroundPhoto2 = pygame.image.load(os.path.join('Game_Files', 'background2.jpg' ))
background1_y = 0
background2_y = -600


# importing all fightership animation (controlled by the user) images + the x and y position of the ship
fighter_ship_1 = pygame.image.load(os.path.join('Game_Files', 'fightership1.png'))
fighter_ship_2 = pygame.image.load(os.path.join('Game_Files', 'fightership2.png'))
fighter_ship_right = pygame.image.load(os.path.join('Game_Files', 'fightershipright.png'))
fighter_ship_left = pygame.image.load(os.path.join('Game_Files', 'fightershipleft.png'))
fighter_x = (screen_x / 2) - 50
fighter_y = screen_y - 100

# importing fightership (controlled by the user) bullet image + the x and y positions of the bullets
# also sets the variables for the x and y positions, as well as an array for all the bullets that are on the screen at once
fighter_bullet_image = pygame.image.load(os.path.join('Game_Files', 'fighterbullet.png'))
global fighter_bullet_x 
global fighter_bullet_y
fighter_bullets = []

# importing all enemy space ship animations (each picture is a different flame out of the back of the ship)
# also sets the x and y positions, as well as an empty array for all the enemy spaceships on the screen
enemy_ship_1 = pygame.image.load(os.path.join('Game_Files', 'enemyship1.png'))
enemy_ship_2 = pygame.image.load(os.path.join('Game_Files', 'enemyship2.png'))
enemy_ship_3 = pygame.image.load(os.path.join('Game_Files', 'enemyship3.png'))
enemy_ship_4 = pygame.image.load(os.path.join('Game_Files', 'enemyship4.png'))
enemy_ship_5 = pygame.image.load(os.path.join('Game_Files', 'enemyship5.png'))
enemy_ship_6 = pygame.image.load(os.path.join('Game_Files', 'enemyship6.png'))
enemy_ship_7 = pygame.image.load(os.path.join('Game_Files', 'enemyship7.png'))
enemy_ship_8 = pygame.image.load(os.path.join('Game_Files', 'enemyship8.png'))
enemy_ship_explosion = pygame.image.load(os.path.join('Game_Files', 'enemyshipexplosion.png'))
global enemy_ship_x
global enemy_ship_y
enemy_ships = []
# Starts a timer for the spawn rate of enemy ships
t1_enemy_ship = time.time()
spawn_rate_enemy_ship = 70

# importing all asteroid animations (each picture is a different orientation of the asteroid)
asteroid_1 = pygame.image.load(os.path.join('Game_Files', 'asteroid1.png'))
asteroid_2 = pygame.image.load(os.path.join('Game_Files', 'asteroid2.png'))
asteroid_3 = pygame.image.load(os.path.join('Game_Files', 'asteroid3.png'))
asteroid_4 = pygame.image.load(os.path.join('Game_Files', 'asteroid4.png'))
global asteroid_x
global asteroid_y
global asteroid_status
asteroids = []

# sets the clock to be used between loops
clock = pygame.time.Clock()

# sets the function gameover after the player loses the game
def gameover():
    # stops the background music after the game is lost
    background_music.stop()

    # after the game is lost, this loop will start with the end messages
    quitting = True
    while quitting:
        for event in pygame.event.get():
            # if the exit button is clicked, quitting will be set to false
            if event.type == pygame.QUIT:
                quitting = False

        # ending message after the game is lost
        endtext1 = gamefont.render("Game Over", True, WHITE)
        endtext2 = gamefont.render("You scored:", True, WHITE)
        # if only 1 point is scored, "point" is singular instead of plural
        if score == 1:
            endtext3 = gamefont.render(str(score) + " point!", True, SCORECOLOUR)
        else:
            endtext3 = gamefont.render(str(score) + " points!", True, SCORECOLOUR)

        # adds all the text to the screen
        screen.blit(endtext1, (100, 150))
        screen.blit(endtext2, (80, 220))
        screen.blit(endtext3, (130, 290))

        # updates the screen
        pygame.display.flip()


# sets playing to true, and starts the game
playing = True
while playing:
    for event in pygame.event.get():
        # if the exit button is clicked, playing will be set to false
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # bullet sound effect by Kenney Vleugels (www.kenney.nl)
            # when the space bar is clicked, a bullet is added to the bullets array
            pygame.mixer.music.load(os.path.join('Game_Files', 'bulletsound.mp3'))
            pygame.mixer.music.play()
            fighter_bullets.append([fighter_x + 23, fighter_y])

    # chooses a random animation each loop, unless it is moving left or right
    fighter_ship_animation = [[fighter_ship_1, fighter_ship_2], fighter_ship_left, fighter_ship_right]
    fighter_normal_status = random.randint(0,1)
    fighter_ship_status = fighter_ship_animation[0][fighter_normal_status]

    # left and right movement of the fighter ship. Fighter ship will not move if it reaches the edge of the screen
    keys = pygame.key.get_pressed()
    # when the left or right arrow key is pressed, the ship will move in that direction and their respective animation will be put onto the screen
    if keys[pygame.K_RIGHT] and fighter_x < 500:
        fighter_x += 5
        fighter_ship_status = fighter_ship_animation[2]
    if keys[pygame.K_LEFT] and fighter_x > 0:
        fighter_x -= 5
        fighter_ship_status = fighter_ship_animation[1]

    # the scrolling effect of the background. Using 2 identical background photos, one starts off screen, and one starts on screen
    # they both go down 1 pixel each loop. Once it gets to the bottom of the screen, it will reset to above the screen
    background1_y += 1
    if background1_y >= 600:
        background1_y = -600
    background2_y += 1
    if background2_y >= 600:
        background2_y = -600

    # adds both background photos to the screen, as well as the fighter ship
    screen.blit(backgroundPhoto, (0, background1_y))
    screen.blit(backgroundPhoto2, (0, background2_y))
    screen.blit(fighter_ship_status, (fighter_x, fighter_y))
    
    # every bullet in the bullet array is updated each loop, until it reaches the top of the screen
    for i in range(len(fighter_bullets)):
        fighter_bullets[i][1] -= 10
    for bullet in fighter_bullets[:]:
        screen.blit(fighter_bullet_image, (bullet[0], bullet[1]))
        if bullet[1] < 0:
            fighter_bullets.remove(bullet)

    # every 10 seconds that the game is being played, the spawn rate of enemy ships will begin to increase, making it more difficult
    if time.time() - t1_enemy_ship >= 10 and spawn_rate_enemy_ship >= 20:
        spawn_rate_enemy_ship -= 5
        t1_enemy_ship = time.time()
     
    # randomly spawns an enemy ship, and adds it to the enemy ships array
    spawn_enemy_ship = random.randint(0, spawn_rate_enemy_ship)
    if spawn_enemy_ship == 1:
        enemy_ship_x = random.randint(0, screen_x - 99)
        enemy_ship_y = -110
        enemy_ships.append([enemy_ship_x, enemy_ship_y])
    
    # all the enemy ship animations are placed into this list
    enemy_ship_animation = [enemy_ship_1, enemy_ship_2, enemy_ship_3, enemy_ship_4, enemy_ship_5, enemy_ship_6, enemy_ship_7, enemy_ship_8]
    # loops through all enemy ships
    for ship in enemy_ships[:]:
        # updates each enemy ship, and gives it a random animation
        ship[1] += 2
        enemy_ship_status = random.randint(0, 7)
        screen.blit(enemy_ship_animation[enemy_ship_status], (ship[0], ship[1]))

        for i in range(len(fighter_bullets)):
            # if a bullet comes into contact with the enenmy ship, the enemy ship is destroyed and the bullet is gone
            # also increases the score by 1
            if fighter_bullets[i][0] + 24 >= ship[0] and fighter_bullets[i][0] + 24 <= ship[0] + 90 and fighter_bullets[i][1] >= ship[1] and fighter_bullets[i][1] <= ship[1] + 100:
                score += 1
                enemy_ships.remove(ship)
                screen.blit(enemy_ship_explosion, (ship[0], ship[1]))
                fighter_bullets.remove(fighter_bullets[i])
                break
            # if the ship reaches the end of the screen, it will be removed
            if ship[1] > 600:
                enemy_ships.remove(ship)
                break
        
        # if an enemy ship hits the fighter ship, the gameover function is called and playing is set to false
        if (ship[0] + 20 in range (int(fighter_x + 20), int(fighter_x + 81)) and ship[1] + 20 in range (int(fighter_y + 20), int(fighter_y + 81))) or (ship[0] + 81 in range (int(fighter_x + 20), int(fighter_x + 81)) and ship[1] + 20 in range (int(fighter_y + 20), int(fighter_y + 81))) or (ship[0] + 20 in range (int(fighter_x + 20), int(fighter_x + 81)) and ship[1] + 81 in range (int(fighter_y + 20), int(fighter_y + 81))) or (ship[0] + 81 in range (int(fighter_x + 20), int(fighter_x + 81)) and ship[1] + 81 in range (int(fighter_y + 20), int(fighter_y + 81))):
            gameover()
            playing = False

    # randomly spawns an asteroid and randomly chooses the asteroid picture
    spawn_asteroid = random.randint(0, 100)
    asteroid_animation = [asteroid_1, asteroid_2, asteroid_3, asteroid_4]
    if spawn_asteroid == 1:
        asteroid_x = random.randint(0, screen_x - 99)
        asteroid_y = -110
        asteroid_status = random.randint(0, 3)
        asteroids.append([asteroid_x, asteroid_y, asteroid_status])
    
    # loops through all the asteroids
    for asteroid in asteroids[:]:
        # updates each asteroid and puts it onto the screen
        asteroid[1] += 3
        screen.blit(asteroid_animation[asteroid[2]], (asteroid[0], asteroid[1]))
        for i in range(len(fighter_bullets)):
            # checks if a bullet comes into contact with an asteroid, and removes the bullet if it does
            if fighter_bullets[i][0] + 24 >= asteroid[0] and fighter_bullets[i][0] + 24 <= asteroid[0] + 90 and fighter_bullets[i][1] >= asteroid[1] and fighter_bullets[i][1] <= asteroid[1] + 100:
                fighter_bullets.remove(fighter_bullets[i])
                break
            # asteroid is removed when it reaches the end of the screen
            if asteroid[1] > 600:
                asteroids.remove(asteroid)
                break

        # if the asteroid hits the ship, the gameover function is called and playing is set to false
        if (asteroid[0] + 10 in range (int(fighter_x + 10), int(fighter_x + 91)) and asteroid[1] + 10 in range (int(fighter_y + 10), int(fighter_y + 91))) or (asteroid[0] + 91 in range (int(fighter_x + 10), int(fighter_x + 91)) and asteroid[1] + 10 in range (int(fighter_y + 10), int(fighter_y + 91))) or (asteroid[0] + 10 in range (int(fighter_x + 10), int(fighter_x + 91)) and asteroid[1] + 91 in range (int(fighter_y + 10), int(fighter_y + 91))) or (asteroid[0] + 91 in range (int(fighter_x + 10), int(fighter_x + 91)) and asteroid[1] + 91 in range (int(fighter_y + 10), int(fighter_y + 91))):
            gameover()
            playing = False
            
    # updates the score text in the top left corner of the screen
    scoretext = gamefont.render(str(score), True, SCORECOLOUR)
    screen.blit(scoretext, (0, 0))

    #updates all the changes made to the screen, and sets a delat of 60 milliseconds
    pygame.display.flip()
    clock.tick(60)

# game is quit at the end of the program
pygame.quit()