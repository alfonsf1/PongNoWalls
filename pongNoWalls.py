import pygame
from random import randint
pygame.init()
pygame.mixer.init()
pygame.font.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
WIDTH = 700
HEIGHT = 500
MAX_SCORE = 2

effect = pygame.mixer.Sound('pong.wav')
winner_song = pygame.mixer.Sound('winner_Song.wav')

#Pong Class
class Paddle(pygame.sprite.Sprite):
    #pulls sprites

    def __init__(self, color, WIDTH, HEIGHT):
        # Call contructor
        super().__init__()


        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        #Draw Paddle
        pygame.draw.rect(self.image, color, [0, 0, WIDTH, HEIGHT])

        #get rect
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
          self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
          self.rect.y = 400

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 350:
          self.rect.x = 350

    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x > 600:
          self.rect.x = 600




class Pong(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        # Constructor
        super().__init__()


        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        #Draw pong
        pygame.draw.rect(self.image, color, [0, 0, width, height])



        self.velocity = [randint(4,8),randint(-8,8)]

        #Get rect image
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8,8)




#Open a new window
window_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(window_size)

left_paddle = Paddle(WHITE, 10, 100)
left_paddle.rect.x = 0
left_paddle.rect.y = 200

left_paddle_top = Paddle(WHITE, 100, 10)
left_paddle_top.rect.x = 240
left_paddle_top.rect.y = 0

left_paddle_bottom = Paddle(WHITE, 100, 10)
left_paddle_bottom.rect.x = 240
left_paddle_bottom.rect.y = 490

right_paddle = Paddle(WHITE, 10, 100)
right_paddle.rect.x = 690
right_paddle.rect.y = 200

right_paddle_top = Paddle(WHITE, 100, 10)
right_paddle_top.rect.x = 350
right_paddle_top.rect.y = 0

right_paddle_bottom = Paddle(WHITE, 100, 10)
right_paddle_bottom.rect.x = 350
right_paddle_bottom.rect.y = 490

pong = Pong(WHITE,10,10)
pong.rect.x = 345
pong.rect.y = 195


#All sprites that were used
pygame_sprites = pygame.sprite.Group()


pygame_sprites.add(left_paddle)
pygame_sprites.add(left_paddle_top)
pygame_sprites.add(left_paddle_bottom)
pygame_sprites.add(right_paddle)
pygame_sprites.add(right_paddle_top)
pygame_sprites.add(right_paddle_bottom)
pygame_sprites.add(pong)

play_game = True

#times updated screen
clock = pygame.time.Clock()

left_player_score = 0
right_player_score = 0


while play_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
              play_game = False
        elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q: #Press q to quit game
                     play_game=False

    #Use arrow keys to move left right up and down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        right_paddle.moveUp(5)
    if keys[pygame.K_DOWN]:
        right_paddle.moveDown(5)
    if keys[pygame.K_RIGHT]:
        right_paddle_top.moveRight(5)
        right_paddle_bottom.moveRight(5)
    if keys[pygame.K_LEFT]:
        right_paddle_top.moveLeft(5)
        right_paddle_bottom.moveLeft(5)



    pygame_sprites.update()

    #Change velocity if pong hits wall
    if pong.rect.x>=690:
        left_player_score+=1
        pong.velocity[0] = -pong.velocity[0]
    if pong.rect.x<=0:
        right_player_score+=1
        pong.velocity[0] = -pong.velocity[0]
    if pong.rect.y>490:
        pong.velocity[1] = -pong.velocity[1]
    if pong.rect.y<0:
        pong.velocity[1] = -pong.velocity[1]

    #Detect collision with paddle and pounce if it does. Also play sound when collision occurs
    if pygame.sprite.collide_mask(pong, left_paddle) or pygame.sprite.collide_mask(pong, right_paddle):
      pong.bounce()
      effect.play()

    if pygame.sprite.collide_mask(pong, left_paddle_top) or pygame.sprite.collide_mask(pong, right_paddle_top):
      pong.bounce()
      effect.play()

    if pygame.sprite.collide_mask(pong, left_paddle_bottom) or pygame.sprite.collide_mask(pong, right_paddle_bottom):
      pong.bounce()
      effect.play()

    screen.fill(BLACK)

    pygame.draw.line(screen, WHITE, [349, 0], [349, 50], 5)
    pygame.draw.line(screen, WHITE, [349, 60], [349, 100], 5)
    pygame.draw.line(screen, WHITE, [349, 110], [349, 160], 5)
    pygame.draw.line(screen, WHITE, [349, 170], [349, 220], 5)
    pygame.draw.line(screen, WHITE, [349, 230], [349, 280], 5)
    pygame.draw.line(screen, WHITE, [349, 290], [349, 340], 5)
    pygame.draw.line(screen, WHITE, [349, 350], [349, 400], 5)
    pygame.draw.line(screen, WHITE, [349, 410], [349, 460], 5)
    pygame.draw.line(screen, WHITE, [349, 470], [349, 500], 5)


    pygame_sprites.draw(screen)

    font = pygame.font.Font(None, 74)
    text = font.render(str(left_player_score), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(right_player_score), 1, WHITE)
    screen.blit(text, (420,10))

    font = pygame.font.SysFont("comicsansms", 20)

    if left_player_score >= MAX_SCORE:
        text = font.render("Left player is winner!", True, (0, 128, 0))
        screen.blit(text, (250,300))
        winner_song.play()

    elif right_player_score >= MAX_SCORE:
        text = font.render("Right player is winnner", True, (0, 128, 0))
        screen.blit(text, (250,300))
        winner_song.play()

    # Update screen
    pygame.display.flip()

pygame.quit()
