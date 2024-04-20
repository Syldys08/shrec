#Создай собственный Шутер!

from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN', True, (255,255,255))
lose = font1.render('YOU LOSE', True, (180,0,0))

font2 = font.SysFont('Arial', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.y = player_y
        self.rect.x = player_x
        self.speed = player_speed
    def reset(self):
        window.blit(self.image, (self.rect.x,  self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 150, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = 0
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500


window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
galaxy = transform.scale(image.load("toilet.jpg"), (win_width, win_height))

ship = Player("shrek.png", 10, win_height-100, 80, 100, 10)
img_bullet = "harchok.png"
img_enemy = "qwerty.png"

score = 0
goal = 200
lost = 0
max_lost = 100

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 80, randint(1, 6))
    monsters.add(monster)

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if finish != True:
        window.blit(galaxy,(0, 0))

        text = font2.render("Счёт: " + str(score), 1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render("Пропущено: " +str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
        
        text_goal = font2.render('Цель: 200',1, (255,255,255))
        window.blit(text_goal, (500,50))

        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 80, randint(1, 5))
            monsters.add(monster)
            
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        display.update()
    time.delay(50)