#region какая то фигня
from pygame import *
from random import randint
font.init()
window = display.set_mode((700, 490))
display.set_caption('Bam, bam, bam')
background = transform.scale(image.load("sd2.png"), (710,510))
#музон тип
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
#endregion
#класс школьный
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

x = 10
y = 10
speed = 25

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 50:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
    def fire(self):
        bulet = Shoots('spooly.png', 10, self.rect.centerx, self.rect.top, 50, 80)
        bullets.add(bulet)

class Shoots(GameSprite):
    def update(self):
        self.rect.y -= self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 400:
            self.rect.y = 0
            self.rect.x = randint(50, 600)
            lost = lost + 1
            text1.set_text("Пропущено: " + str(lost))


hero = Player('gas.png', speed, 180, 400, 100, 100)

game = True
finish = 0

class Label():
    def __init__(self, text, x, y):
        self.font1 = font.SysFont('Arial', 36)
        self.text = self.font1.render(text, True, (255, 255, 255))
        self.x = x
        self.y = y
    def set_text(self, text):
        self.text = self.font1.render(text, True, (255, 255, 255))
    def draw(self):
        window.blit(self.text, (self.x, self.y))

lost = 0
score = 0

text1 = Label('Пропущено: 0', 20, 50)
text2 = Label('Счет: 0', 20, 20)

background1 = transform.scale(image.load("yw.jpg"), (710,510))
background2 = transform.scale(image.load("yl.jpg"), (710,510))

enemies = sprite.Group()
bullets = sprite.Group()
while game:
    if finish == 0:
        if len(enemies) < 5:
            x = randint(50, 650)
            enemies.add(Enemy('power.png', randint(3, 7), x, 40, 70, 70))
        window.blit(background,(0, 0))
        hero.update()
        enemies.update()
        bullets.draw(window)
        bullets.update()
        hero.reset()
        text1.draw()
        text2.draw()
        enemies.draw(window)
        
        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        score += len(sprites_list)
        text2.set_text("Счет: " + str(score))
        sprites_list = sprite.spritecollide(hero, enemies, False)
        if lost >= 3:
            finish = 2
        if score >= 5:
            finish = 1
    else:
        if finish == 1:
            window.blit(background1,(0, 0))
        if finish == 2:
            window.blit(background2,(0, 0))

    for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN and e.key == K_w:
                hero.fire()     
    display.update()
    time.delay(50)
