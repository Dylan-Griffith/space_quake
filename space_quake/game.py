import pygame
import random
from os import path
vec = pygame.math.Vector2


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 600
HEIGHT = 800
FPS = 60

# player Properties
PLAYER_ACC = 0.6
PLAYER_FRICTION = -0.14

GAME_NAME = 'Escape Quake!'
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_lives(surface, y, img):
    img_rect = img.get_rect()
    img_rect.centerx = 25
    img_rect.y = y
    surface.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, GAME_NAME, 64, WIDTH / 2, HEIGHT / 4)
    if level > 1:
        draw_text(screen, 'Previous Score: {}'.format(level), 22, WIDTH/2, 12)
    draw_text(screen, 'Arrow keys to move', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, 'Avoid the eneimes and collect the treasure   ', 22, WIDTH / 2, HEIGHT / 2 + 44)
    draw_text(screen, 'Highscore: {}'.format(highscore), 32, WIDTH / 2, HEIGHT * 2 / 5)
    draw_text(screen, 'Press enter to begin', 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sound.toggle()
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_RETURN]:
                waiting = False


def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def new_treasure():
    t = Treasure(random.randrange(25, WIDTH - 25), random.randrange(25, HEIGHT - 25))
    all_sprites.add(t)
    treasures.add(t)


def speed_powerup_check():
    global speed_power_up_time
    now = pygame.time.get_ticks()
    if now - speed_power_up_time > 8000:
        if random.random() > .01 and len(pows) < 1:
            pow = Pow('speed', speed_pow_img)
            all_sprites.add(pow)
            pows.add(pow)
        speed_power_up_time = pygame.time.get_ticks()


def life_powerup_check():
    global life_power_up_time
    now = pygame.time.get_ticks()
    if now - life_power_up_time > 10000:
        if random.random() > .50 and len(pows) < 1:
            pow = Pow('life', life_pow_img)
            all_sprites.add(pow)
            pows.add(pow)
        life_power_up_time = pygame.time.get_ticks()


def power_up_check():
    life_powerup_check()
    speed_powerup_check()


def save_highscore(player, highscore):
    if player.level > highscore:
        print(True)
        with open('highscore.txt', 'w') as fout:
            fout.write(str(player.level))


def load_highscore():
    try:
        with open('highscore.txt', 'r') as fin:
            highscore = int(fin.readline())
    except FileNotFoundError:
        highscore = 0
    return highscore


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((25, 25))
        # self.image.fill(GREEN)
        self.image = pygame.transform.scale(player_img, (25, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.PLAYER_SPEED = 6
        self.speedy = self.PLAYER_SPEED
        self.speedx = self.PLAYER_SPEED
        self.level = 1
        self.lives = 3
        self.pos = vec(WIDTH / 2, HEIGHT - 20)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        # print(self.vel)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.acc.y = -PLAYER_ACC
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.acc.y = PLAYER_ACC

        self.acc += self.vel * PLAYER_FRICTION
        # equation of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Check screen boundaries
        if self.pos.x > WIDTH - 12:
            self.pos.x = WIDTH - 12
        if self.pos.x < 12:
            self.pos.x = 12
        if self.pos.y > HEIGHT - 12:
            self.pos.y = HEIGHT - 12
        if self.pos.y < 12:
            self.pos.y = 12
        self.rect.center = self.pos

        # self.speedx = 0
        # self.speedy = 0
        # keystate = pygame.key.get_pressed()
        # if keystate[pygame.K_UP] or keystate[pygame.K_w]:
        #     self.speedy = -self.PLAYER_SPEED
        # if keystate[pygame.K_DOWN]or keystate[pygame.K_s]:
        #     self.speedy = self.PLAYER_SPEED
        # if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
        #     self.speedx += self.PLAYER_SPEED
        # if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
        #     self.speedx += -self.PLAYER_SPEED
        # self.rect.y += self.speedy
        # self.rect.x += self.speedx
        # # Check screen boundaries
        # if self.rect.right > WIDTH:
        #     self.rect.right = WIDTH
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT
        # if self.rect.top < 0:
        #     self.rect.top = 0

    def speed_up(self):
        global PLAYER_ACC
        # self.PLAYER_SPEED += 1
        if PLAYER_ACC < 1.0:
            PLAYER_ACC += .05


class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30))
        # self.image.fill(BLUE)
        self.image = pygame.transform.scale(mob_img, (30, 30))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(50, WIDTH - 50)
        self.rect.top = random.randrange(50, HEIGHT - 100)
        self.SPEED = random.randrange(2, 5)
        self.base_speed = self.SPEED
        self.speedx = self.SPEED

    def update(self):
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.speedx = -abs(self.SPEED)
        if self.rect.left < 0:
            self.speedx = abs(self.SPEED)
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def speed_up(self):
        if self.speedx > 0:
            self.speedx += (self.base_speed * .1)
        else:
            self.speedx += -(self.base_speed * .1)
        self.SPEED = self.speedx
        if self.SPEED > 13:
            self.SPEED = 13


class Treasure(pygame.sprite.Sprite):

    def __init__(self, centerx, bottom):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30))
        # self.image.fill(RED)
        self.image = pygame.transform.scale(treasure_img, (25, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom


class Pow(pygame.sprite.Sprite):

    def __init__(self, pow_type, image):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.transform.scale(speed_pow_img, (25, 25))
        self.type = pow_type
        self.image = image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(25, WIDTH - 25)
        self.rect.bottom = random.randrange(25, HEIGHT - 25)
        self.last_update = pygame.time.get_ticks()
        self.decay_time = 5000

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.decay_time:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, frame_rate=75):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Sound(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = unmute_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - 25
        self.rect.bottom = 30
        self.sound_on = True

    def toggle(self):
        if self.sound_on:
            self.mute()
            self.image = mute_img
            self.sound_on = False
        else:
            self.unmute()
            self.image = unmute_img
            self.sound_on = True

    def mute(self):
        mob_sound.set_volume(0)
        treasure_sound.set_volume(0)
        levelup_sound.set_volume(0)
        speed_up_sound.set_volume(0)
        life_up_sound.set_volume(0)
        pygame.mixer.music.set_volume(0.0)

    def unmute(self):
        mob_sound.set_volume(1)
        treasure_sound.set_volume(1)
        levelup_sound.set_volume(1)
        speed_up_sound.set_volume(1)
        life_up_sound.set_volume(1)
        pygame.mixer.music.set_volume(1)





# Load game graphics
background = pygame.image.load(path.join(img_dir, 'space.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'alienGreen_stand.png')).convert()
player_sm_img = pygame.transform.scale(player_img, (15, 15))
mob_img = pygame.image.load(path.join(img_dir, 'enemy.png')).convert()
treasure_img = pygame.image.load(path.join(img_dir, 'treasure.png')).convert()
speed_pow_img = pygame.image.load(path.join(img_dir, 'bolt_bronze.png')).convert()
life_pow_img = pygame.image.load(path.join(img_dir, 'pill_green.png')).convert()
mute_img = pygame.image.load(path.join(img_dir, 'mute.png')).convert()
mute_img = pygame.transform.scale(mute_img, (20, 20))
unmute_img = pygame.image.load(path.join(img_dir, 'unmute.png')).convert()
unmute_img = pygame.transform.scale(unmute_img, (20, 20))
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['power_up'] = []
explosion_anim['treasure'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (40, 40))
    explosion_anim['sm'].append(img_sm)
for i in range(3):
    filename = 'explosionSmoke{}.png'.format(i)
    filename = 'flash0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (40, 40))
    explosion_anim['power_up'].append(img)
    filename = 'explosionSmoke{}.png'.format(i)
    filename = 'whitePuff0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img = pygame.transform.scale(img, (40, 40))
    explosion_anim['treasure'].append(img)


# Load Game Sounds
mob_sound = pygame.mixer.Sound(path.join(snd_dir, 'Hit_Hurt2.wav'))
treasure_sound = pygame.mixer.Sound(path.join(snd_dir, 'collide1.wav'))
levelup_sound = pygame.mixer.Sound(path.join(snd_dir, 'levelup.wav'))
speed_up_sound = pygame.mixer.Sound(path.join(snd_dir, 'speed_up.wav'))
life_up_sound = pygame.mixer.Sound(path.join(snd_dir, 'life_up.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'TLE Digital Loop Short.wav'))
# pygame.mixer.music.set_volume(0.0)


# Game loop
running = True
game_over = True
pygame.mixer.music.play(loops=-1)
speed_power_up_time = pygame.time.get_ticks()
life_power_up_time = pygame.time.get_ticks()
sound = Sound()
level = 0

while running:
    if game_over:
        highscore = load_highscore()
        show_go_screen()
        level = 1
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        treasures = pygame.sprite.Group()
        pows = pygame.sprite.Group()
        player = Player()
        game_over = False
        all_sprites.add(player)
        for i in range(5):
            new_mob()
        treasure = Treasure(WIDTH / 2, 50)
        all_sprites.add(treasure)
        treasures.add(treasure)
        all_sprites.add(sound)

    # keep loop running at right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # chest for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                    sound.toggle()

    # Update
    all_sprites.update()

    # random Power up spawn:
    power_up_check()
    # Check if player and mob collide
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        for hit in hits:
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
        mob_sound.play()
        player.lives -= 1
        player.pos.x = WIDTH / 2
        player.pos.y = HEIGHT - 20

        # game_over = True
    # Check if player and treasure collide
    hits = pygame.sprite.spritecollide(player, treasures, True)
    if hits:
        treasure_sound.play()
        new_treasure()
        player.level += 1
        level += 1
        if player.level > 1 and player.level % 3 == 0:
            levelup_sound.play()
            new_mob()
            for mob in mobs:
                mob.speed_up()
        for hit in hits:
            tre_expl = Explosion(hit.rect.center, 'treasure', frame_rate=75)
            all_sprites.add(tre_expl)

    # check if player collides with power up
    hits = pygame.sprite.spritecollide(player, pows, True)
    for hit in hits:
        if hit.type == 'speed':
            speed_up_sound.play()
            player.speed_up()
        if hit.type == 'life':
            life_up_sound.play()
            player.lives += 1
        pow_expl = Explosion(hit.rect.center, 'power_up', frame_rate=75)
        all_sprites.add(pow_expl)

    # checks if game over
    if player.lives < 1:
        save_highscore(player, highscore)
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'level {}'.format(str(player.level)), 12, WIDTH / 2, 10)
    draw_lives(screen, 5, player_sm_img)
    draw_text(screen, 'X {}'.format(str(player.lives)), 12, 50, 6)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
