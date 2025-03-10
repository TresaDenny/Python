import pygame
import random

pygame.init()

#screen size
width,height= 800,400

#COLORS
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)

#FONTS
font = pygame.font.Font(None, 36)

#Screen Setup
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Block Runner Game")
clock=pygame.time.Clock()

#Screen Setup
char_x,char_y= 100,height //2     # x coordinate starts from 100 pixels to the left y: starts halfway down the screen vertically ( // represents the floor division)
char_vel_y= 0                      # characters velocity starts at 0 ; no initial movement
gravity=0.5                    # makes the character fall; on each frame the velocity increases by 0.5 and then falls down
fly_power= -10                   # Fly power determines how strongly the character flies up when yu press space (-7: character moves up to the -ve direction on the y axis with speed -7)

#Obstacles
obstacle_speed = 4                           # obstacle starts moving from right to left at four pixels per frame
speed_increase_interval=5000                 #obstacle speed inc at every 5000 ms(5 sec)
last_speed_increase=pygame.time.get_ticks()  #returns the no. of ms since the game started
obstacle_list=[]
top_obstacle=True

#score and game state
score=0
game_over=False

#Function to create obstacles
'''makes use of  RANDOM library to randomly create rectangular obstacles at the top and bottom of varying length'''
def create_obstacles():
    global top_obstacle
    HEIGHT = random.randint(50, height // 2)
    if top_obstacle:
        obstacle_list.append({"rect": pygame.Rect(width, 0, 30, HEIGHT), "passed": False})
    else:
        obstacle_list.append({"rect": pygame.Rect(width, height - HEIGHT, 30, HEIGHT), "passed": False})
    top_obstacle = not top_obstacle
    
#Main loop
running=True
while running:
    screen.fill(WHITE)


# Event handling
# pygame.event.get() is a built-in function in Pygame 
# that captures all events, like mouse clicks, key presses, 
# and other user interactions. It collects them in a queue
# for you to handle in your game loop.


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                char_vel_y=fly_power    

    #Applying gravity
    #char_vel_y inc the gravity value by 0.5 in every frame
    #char_y changes value by velocity(+ve flies up -ve falls down)
    #if case : makes sure the character doesnt fly out of the screen
    #elif case: height of the char is 40 - if the character goes blw the screen it gets ocked to the bottom 

    char_vel_y+=gravity
    char_y+= char_vel_y
    if char_y<0:
        char_y=0
    elif char_y + 40 > height:
        char_y=height-40

     # Create new obstacle
    if len(obstacle_list) == 0 or obstacle_list[-1]["rect"].x < width - 200:
        create_obstacles()

    # Move obstacles and check for score increment
    for obstacle in obstacle_list:
        obstacle["rect"].x -= obstacle_speed #moves the obstacle left
        if not obstacle["passed"] and char_x > obstacle["rect"].x + obstacle["rect"].width:
            score += 1
            obstacle["passed"] = True

    # Remove off-screen obstacles
    obstacle_list = [obstacle for obstacle in obstacle_list if obstacle["rect"].x > -30]            

    #Detects collison with the help of colliderect function (checks if the character and obstacle collide with each other)
    char_rect = pygame.Rect(char_x, char_y, 40, 40)
    for obstacle in obstacle_list:
        if char_rect.colliderect(obstacle["rect"]):
            game_over = True

    # Increase the speed of the game over time
    '''get.ticks() gives u the current speed of the char in ms .... on subtracting the last speed inc with current speed if it is > speed inc interval inc the speed and set the last speed to current speed '''
    if pygame.time.get_ticks() - last_speed_increase > speed_increase_interval:
        obstacle_speed += 1
        last_speed_increase = pygame.time.get_ticks()

    # Draw obstacles as red rectangles
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, RED, obstacle["rect"])

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw the player
    pygame.draw.rect(screen,BLACK,(char_x,char_y,40,40))   # starting x position andd y position and the height and width of the player


    if game_over:
        over_text=font.render("Game Over!!Press R to Restart",True,BLACK)
        screen.blit(over_text,(width//4,height//2))
        pygame.display.flip()
        while True:
            event=pygame.event.wait()
            if event.type==pygame.QUIT:
                running=False
                game_over=False
                break
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
                char_y=height//2
                obstacle_list.clear()
                score=0
                obstacle_speed=4
                last_speed_increase=pygame.time.get_ticks()
                game_over=False
                break
    else:    
        pygame.display.flip()
        clock.tick(30)

pygame.quit()            




    
    





