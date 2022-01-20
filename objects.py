import pygame
import random


BULLETS = pygame.sprite.Group()
METEORITES = pygame.sprite.Group()
SHIP = pygame.sprite.Group()
PIRATES = pygame.sprite.Group()
PIRATES_BULLETS = pygame.sprite.Group()


class Ship(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group, SHIP)
        self.image_common = pygame.image.load("data/ship.png")
        self.image_common = pygame.transform.scale(self.image_common, (40, 40))
        self.image_common.set_colorkey(self.image_common.get_at((0, 0)))
        self.image = self.image_common
        self.rect = pygame.Rect(400, 500, 40, 40)
        self.group = group
        self.health = 100

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.y > 320:
            self.rect.y -= 4
        if keys[pygame.K_s] and self.rect.y < 540:
            self.rect.y += 4
        if keys[pygame.K_a] and self.rect.x > 10:
            self.rect.x -= 10
        if keys[pygame.K_d] and self.rect.x < 730:
            self.rect.x += 10
        if keys[pygame.K_SPACE] and len(BULLETS) < 2:
            Bullet(self.group, self.rect.x + 18, self.rect.y - 10)
        if not self.rect.colliderect((0, 0, 800, 600)):
            self.kill()
        if pygame.sprite.spritecollideany(self, METEORITES):
            self.health -= 25
        if pygame.sprite.spritecollideany(self, PIRATES):
            self.health -= 25
        if pygame.sprite.spritecollideany(self, PIRATES_BULLETS):
            self.health -= 10

    def end_level(self, all_sprites, screen, bg, mode=False):
        clock = pygame.time.Clock()
        image = pygame.image.load("data/ship.png")
        for i in BULLETS:
            i.kill()
        if mode:
            while self.rect.width < 100:
                self.rect.y -= 20
                self.rect.width += 3
                self.rect.height += 3
                self.image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
                self.image.set_colorkey(image.get_at((0, 0)))
                screen.blit(bg, (0, 0))
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(30)
        else:
            while self.rect.x > 400:
                self.rect.x -= 20
                screen.blit(bg, (0, 0))
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(30)
            while self.rect.x < 400:
                self.rect.x += 20
                screen.blit(bg, (0, 0))
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(30)
            while self.rect.y > 400:
                self.rect.y -= 20
                screen.blit(bg, (0, 0))
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(30)
            while self.rect.width > 2:
                self.rect.y -= 20
                self.rect.width -= 3
                self.rect.height -= 3
                self.image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
                self.image.set_colorkey(image.get_at((0, 0)))
                screen.blit(bg, (0, 0))
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(30)
        self.kill()

    def destroy(self, all_sprites, screen, bg, n):
        clock = pygame.time.Clock()
        for i in BULLETS:
            i.kill()
        image = pygame.image.load("data/ship.png")
        while self.rect.width > 2:
            self.rect.width -= 3
            self.rect.height -= 3
            self.image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
            self.image.set_colorkey(image.get_at((0, 0)))
            screen.blit(bg, (0, n))
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(30)
        self.kill()

    def set_health(self):
        self.health += 50


class Pirate(pygame.sprite.Sprite):
    def __init__(self, group, flag=False):
        super().__init__(group)
        if flag:
            image = pygame.image.load("data/sep.png")
        else:
            image = pygame.image.load("data/pirate.png")
        self.image = pygame.transform.scale(image, (40, 40))
        self.image.set_colorkey(image.get_at((0, 0)))
        self.rect = pygame.Rect(random.randrange(35, 700), 0, 40, 40)
        while pygame.sprite.spritecollideany(self, PIRATES):
            self.rect.x = random.randrange(100, 700)
        PIRATES.add(self)
        self.group = group
        self.health = 100
        self.timer = 0
        self.spead = random.randint(-5, 5)
        self.shoats_spead = random.randint(20, 30)

    def update(self, keys):
        self.rect.y += 2
        self.timer += 1
        if self.rect.x >= 760:
            self.spead = -self.spead
        if self.rect.x <= 0:
            self.spead = -self.spead
        self.rect.x += self.spead
        if not self.rect.colliderect((0, 0, 800, 600)):
            self.kill()
        if pygame.sprite.spritecollideany(self, BULLETS):
            self.health -= 25
            if not self.health:
                self.kill()
        if pygame.sprite.spritecollideany(self, SHIP):
            SHIP.update(pygame.key.get_pressed())
            self.kill()
        if self.timer % self.shoats_spead == 0:
            PiratesBullet(self.group, self.rect.x, self.rect.y + 41)


class Boss(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        image = pygame.image.load("data/boss.png")
        self.image = pygame.transform.scale(image, (100, 50))
        self.image.set_colorkey(image.get_at((0, 0)))
        self.rect = pygame.Rect(random.randrange(35, 700), 0, 100, 50)
        while pygame.sprite.spritecollideany(self, PIRATES):
            self.rect.x = random.randrange(100, 700)
        PIRATES.add(self)
        self.group = group
        self.health = 100
        self.timer = 0
        self.spead = 1
        self.shoats_spead = 22

    def update(self, keys):
        self.rect.y += 2
        self.timer += 1
        if self.rect.x >= 760:
            self.spead = -self.spead
        if self.rect.x <= 0:
            self.spead = -self.spead
        self.rect.x += self.spead
        if not self.rect.colliderect((0, 0, 800, 600)):
            self.kill()
        if pygame.sprite.spritecollideany(self, BULLETS):
            self.health -= 1
            if not self.health:
                self.kill()
        if pygame.sprite.spritecollideany(self, SHIP):
            SHIP.update(pygame.key.get_pressed())
            self.kill()
        if self.timer % self.shoats_spead == 0:
            PiratesBullet(self.group, self.rect.x - 10, self.rect.y + 41)
            PiratesBullet(self.group, self.rect.x + 10, self.rect.y + 41)
            PiratesBullet(self.group, self.rect.x, self.rect.y + 41)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group,  x, y):
        super().__init__(group, BULLETS)
        self.image = pygame.Surface((5, 5),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 5, 5))
        self.rect = pygame.Rect(x, y, 5, 5)

    def update(self, keys):
        if keys == "kill":
            if pygame.sprite.spritecollideany(self, METEORITES):
                self.kill()
            if pygame.sprite.spritecollideany(self, PIRATES):
                self.kill()
        self.rect.y -= 20
        if not self.rect.colliderect((0, 0, 800, 600)):
            self.kill()


class PiratesBullet(pygame.sprite.Sprite):
    def __init__(self, group,  x, y):
        super().__init__(group, PIRATES_BULLETS)
        self.image = pygame.Surface((5, 5),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 5, 5))
        self.rect = pygame.Rect(x, y, 5, 5)

    def update(self, keys):
        if keys == "kill":
            if pygame.sprite.spritecollideany(self, SHIP):
                self.kill()
        if pygame.sprite.spritecollideany(self, SHIP):
            self.kill()
        self.rect.y += 10
        if not self.rect.colliderect((0, 0, 800, 600)):
            self.kill()


class Meteorite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.frames = []
        self.cur_frame = 0
        for i in range(1, 21):
            self.frames.append(pygame.transform.scale(pygame.image.load(f"meteor/rotationY{i}.png"), (65, 65)))
        self.image = self.frames[0]
        self.rect = pygame.Rect(random.randrange(35, 700), 0, 65, 65)
        while pygame.sprite.spritecollideany(self, METEORITES):
            self.rect.x = random.randrange(100, 700)
        METEORITES.add(self)
        self.health = 50

    def update(self, keys):
        self.rect.y += 2
        if not self.rect.colliderect((0, 0, 800, 600)):
            self.kill()
        if pygame.sprite.spritecollideany(self, BULLETS):
            self.health -= 25
            if not self.health:
                self.kill()
        if pygame.sprite.spritecollideany(self, SHIP):
            SHIP.update(pygame.key.get_pressed())
            self.kill()
        self.cur_frame += 1
        if self.cur_frame == 20:
            self.cur_frame = 0
        self.image = self.frames[self.cur_frame]


class Button:
    def __init__(self, pos, text, width):
        self.x = pos[0]
        self.y = pos[1]
        self.t = text
        self.width = width
        font = pygame.font.Font(None, 24)
        self.text = font.render(text, True, (255, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, 25), 1)
        screen.blit(self.text, (self.x + 5, self.y + 5))

    def update(self, pos):
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + 25:
            return True
        return False
