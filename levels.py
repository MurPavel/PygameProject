from objects import *
import sys
import pygame


FPS = 30


def new_game():
    file = open("data/source.txt", mode='w')
    file.write('1\n0')
    file.close()


def continue_game():
    file = open("data/source.txt", mode='r').read().split('\n')
    levels = [first_level, second_level, level3, level4, level5, level6, finish_screen]
    return levels[int(file[0]) - 1]


def get_score():
    file = open("data/source.txt", mode='r').read().split('\n')
    return file[1]


def update_source(score):
    file_r = open("data/source.txt", mode='r').read()
    source = [int(i) for i in file_r.split('\n')]
    file = open("data/source.txt", mode='w')
    file.write(str(source[0] + 1) + '\n')
    file.write(str(source[1] + score))


def terminate():
    pygame.quit()
    sys.exit()


def clear():
    for i in BULLETS:
        i.kill()
    for i in SHIP:
        i.kill()
    for i in METEORITES:
        i.kill()
    for i in PIRATES:
        i.kill()
    for i in PIRATES_BULLETS:
        i.kill()


def main_menu(screen):
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    text = font.render(f"Space adventure", True, (255, 0, 0))
    new_game_button = Button((10, 40), "Новая игра", 125)
    continue_button = Button((10, 80), "Продолжить", 125)
    exit_button = Button((10, 120), "Выход", 125)
    flag_new_game = False
    flag_continue = False
    flag_exit = False
    fon = pygame.transform.scale(pygame.image.load("data/main_menu.jpg"), (800, 600))

    while running:
        screen.blit(fon, (0, 0))
        screen.blit(text, (10, 10))
        new_game_button.draw(screen)
        continue_button.draw(screen)
        exit_button.draw(screen)
        if flag_new_game:
            new_game()
            res = first_level(screen)
            if res == "continue":
                flag_continue = True
            flag_new_game = False
        elif flag_continue:
            res = continue_game()
            r = res(screen)
            if r != 'continue':
                flag_continue = False
        elif flag_exit:
            terminate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    flag_new_game = new_game_button.update(event.pos)
                    flag_continue = continue_button.update(event.pos)
                    flag_exit = exit_button.update(event.pos)
        pygame.display.flip()
        clock.tick(FPS)


def first_intro(screen):
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load("data/space_intro1.jpg"), (800, 600))
    screen.blit(fon, (0, 0))
    intro_text = ["Начало пути", "",
                  "Вам поручили доставить ценный груз до далекой планеты Альдераан,",
                  "но не все так просто! По пути вам предстоит через обломки",
                  "разрушенной планеты Бисс и прибыть на ближайшую планету Татуин"]
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return 0
        pygame.display.flip()
        clock.tick(FPS)


def first_level(screen):
    first_intro(screen)
    planet = pygame.sprite.Sprite()
    planet.image = pygame.image.load("data/planet_41.png")
    planet.rect = planet.image.get_rect()
    planet.rect.x = 120
    planet.rect.y = -2100
    bg = pygame.transform.scale(pygame.image.load("data/space_rt.png"), (800, 2600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    running = True
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BULLETS)
    all_sprites.add(planet)
    ship = Ship(all_sprites)
    n = -2000
    score = 0
    flag = True
    continue_esc_menu = Button((300, 200), "Продолжить", 200)
    exit_esc_menu = Button((300, 250), "Выйти в главное меню", 200)
    flag_continue_esc_menu = False
    flag_exit_esc_menu = False
    game = True
    esc = False
    game_over = False
    finish = False
    while running:
        if game:
            if flag and n < -400:
                Meteorite(all_sprites)
                flag = False
            if n % 12 == 0:
                flag = True
            screen.blit(bg, (0, n))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True
                        game = False
            all_sprites.draw(screen)
            all_sprites.update(pygame.key.get_pressed())
            pygame.draw.rect(screen, (0, 255, 0), (0, 595, ship.health, 5))
            pygame.display.flip()
            n += 1
            planet.rect.y += 1
            if pygame.sprite.groupcollide(BULLETS, METEORITES, True, True):
                score += 50
                BULLETS.update("kill")
            if n >= 0 or ship.health <= 0:
                if n >= 0:
                    ship.end_level(all_sprites, screen, bg)
                    game = False
                    finish = True
                elif ship.health <= 0:
                    game = False
                    game_over = True
                    ship.destroy(all_sprites, screen, bg, n)
                clear()
        if esc:
            text = font.render(f"Пауза", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                esc = False
                game = True
                flag_continue_esc_menu = False
            rect = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            rect.fill((20, 20, 20, 1))
            screen.blit(rect, (0, 0))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = False
                        game = True
                        flag_continue_esc_menu = False
                        flag_exit_esc_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if finish:
            text = font.render(f"You made it! Score:{score}", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                update_source(score)
                return 1
            if flag_continue_esc_menu:
                clear()
                update_source(score)
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if game_over:
            text = font.render(f"Game Over", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                clear()
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        clock.tick(FPS)
    return True


def second_intro(screen):
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load("data/space_intro2.jpg"), (800, 600))
    screen.blit(fon, (0, 0))
    intro_text = ["Первая встреча", "",
                  "Татуин славится своими механиками, и вам улучшили корабль.",
                  "Но Татуин также точка пиратов. И к сожелению, ",
                  "пираты узнали о вашем визите.",
                  "В момент вылета на вас напали пираты.",
                  "Пролетите через пустыню ветров.",
                  "Дайте бой пиратам и взлетите с планеты!"]
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return 0
        pygame.display.flip()
        clock.tick(FPS)


def second_level(screen):
    second_intro(screen)
    bg = pygame.transform.scale(pygame.image.load("data/sand2.jpg"), (800, 2600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    running = True
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BULLETS)
    all_sprites.add(PIRATES_BULLETS)
    ship = Ship(all_sprites)
    ship.set_health()
    n = -2000
    score = 0
    flag = True
    game = True
    esc = False
    game_over = False
    finish = False
    continue_esc_menu = Button((300, 200), "Продолжить", 200)
    exit_esc_menu = Button((300, 250), "Выйти в главное меню", 200)
    flag_continue_esc_menu = False
    flag_exit_esc_menu = False
    while running:
        if game:
            if flag and n < -100:
                Pirate(all_sprites)
                flag = False
            if n % 40 == 0:
                flag = True
            screen.blit(bg, (0, n))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            pygame.draw.rect(screen, (0, 255, 0), (0, 595, ship.health, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True
                        game = False
            all_sprites.draw(screen)
            all_sprites.update(pygame.key.get_pressed())
            pygame.display.flip()
            n += 1
            if pygame.sprite.groupcollide(BULLETS, PIRATES, True, True):
                score += 150
                BULLETS.update("kill")
            if n >= 0 or ship.health <= 0:
                if n >= 0:
                    ship.end_level(all_sprites, screen, bg, mode=True)
                    game = False
                    finish = True
                elif ship.health <= 0:
                    game = False
                    game_over = True
                    ship.destroy(all_sprites, screen, bg, n)
                clear()
        if esc:
            text = font.render(f"Пауза", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                esc = False
                game = True
                flag_continue_esc_menu = False
            rect = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            rect.fill((125, 103, 73, 2))
            screen.blit(rect, (0, 0))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = False
                        game = True
                        flag_continue_esc_menu = False
                        flag_exit_esc_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if finish:
            text = font.render(f"You made it! Score:{score}", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                update_source(score)
                return 1
            if flag_continue_esc_menu:
                clear()
                update_source(score)
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if game_over:
            text = font.render(f"Game Over", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                clear()
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        clock.tick(FPS)
    return True


def intro3(screen):
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load("data/space_intro1.jpg"), (800, 600))
    screen.blit(fon, (0, 0))
    intro_text = ["Проблема", "",
                  "Вы успешно сбежали от пиратов, но из-за лишних полетов",
                  "топлива хватит лишь до Набу.",
                  "Долетите до планеты без проишествий."]
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return 0
        pygame.display.flip()
        clock.tick(FPS)


def level3(screen):
    intro3(screen)
    planet = pygame.sprite.Sprite()
    planet.image = pygame.image.load("data/planet_43.png")
    planet.rect = planet.image.get_rect()
    planet.rect.x = 120
    planet.rect.y = -2100
    bg = pygame.transform.scale(pygame.image.load("data/space_rt.png"), (800, 2600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    running = True
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BULLETS)
    all_sprites.add(planet)
    ship = Ship(all_sprites)
    ship.set_health()
    n = -2000
    score = 0
    flag = True
    continue_esc_menu = Button((300, 200), "Продолжить", 200)
    exit_esc_menu = Button((300, 250), "Выйти в главное меню", 200)
    flag_continue_esc_menu = False
    flag_exit_esc_menu = False
    game = True
    esc = False
    game_over = False
    finish = False
    while running:
        if game:
            if flag and n < -400:
                Meteorite(all_sprites)
                flag = False
            if n % 12 == 0:
                flag = True
            screen.blit(bg, (0, n))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True
                        game = False
            all_sprites.draw(screen)
            all_sprites.update(pygame.key.get_pressed())
            pygame.draw.rect(screen, (0, 255, 0), (0, 595, ship.health, 5))
            pygame.display.flip()
            n += 1
            planet.rect.y += 1
            if pygame.sprite.groupcollide(BULLETS, METEORITES, True, True):
                score += 50
                BULLETS.update("kill")
            if n >= 0 or ship.health <= 0:
                if n >= 0:
                    ship.end_level(all_sprites, screen, bg)
                    game = False
                    finish = True
                elif ship.health <= 0:
                    game = False
                    game_over = True
                    ship.destroy(all_sprites, screen, bg, n)
                clear()
        if esc:
            text = font.render(f"Пауза", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                esc = False
                game = True
                flag_continue_esc_menu = False
            rect = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            rect.fill((20, 20, 20, 1))
            screen.blit(rect, (0, 0))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = False
                        game = True
                        flag_continue_esc_menu = False
                        flag_exit_esc_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if finish:
            text = font.render(f"You made it! Score:{score}", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                update_source(score)
                return 1
            if flag_continue_esc_menu:
                clear()
                update_source(score)
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if game_over:
            text = font.render(f"Game Over", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                clear()
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        clock.tick(FPS)
    return True


def intro4(screen):
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load("data/space_intro4.jpg"), (800, 600))
    screen.blit(fon, (0, 0))
    intro_text = ["Внезапная встреча", "",
                  "Набу славится своей природой, а также производителями защиты.",
                  "Ваш корабль был улучшен.",
                  "Но вот незадача, на планете вас выследили Сепаратисты.",
                  "Оторвитесь от них и улетите с планеты!"]
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return 0
        pygame.display.flip()
        clock.tick(FPS)


def level4(screen):
    intro4(screen)
    bg = pygame.transform.scale(pygame.image.load("data/forest.png"), (800, 2600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    running = True
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BULLETS)
    all_sprites.add(PIRATES_BULLETS)
    ship = Ship(all_sprites)
    ship.set_health()
    ship.set_health()
    n = -2000
    score = 0
    flag = True
    game = True
    esc = False
    game_over = False
    finish = False
    continue_esc_menu = Button((300, 200), "Продолжить", 200)
    exit_esc_menu = Button((300, 250), "Выйти в главное меню", 200)
    flag_continue_esc_menu = False
    flag_exit_esc_menu = False
    while running:
        if game:
            if flag and n < -100:
                Pirate(all_sprites, flag=True)
                flag = False
            if n % 40 == 0:
                flag = True
            screen.blit(bg, (0, n))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            pygame.draw.rect(screen, (0, 255, 0), (0, 595, ship.health, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True
                        game = False
            all_sprites.draw(screen)
            all_sprites.update(pygame.key.get_pressed())
            pygame.display.flip()
            n += 1
            if pygame.sprite.groupcollide(BULLETS, PIRATES, True, True):
                score += 150
                BULLETS.update("kill")
            if n >= 0 or ship.health <= 0:
                if n >= 0:
                    ship.end_level(all_sprites, screen, bg, mode=True)
                    game = False
                    finish = True
                elif ship.health <= 0:
                    game = False
                    game_over = True
                    ship.destroy(all_sprites, screen, bg, n)
                clear()
        if esc:
            text = font.render(f"Пауза", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                esc = False
                game = True
                flag_continue_esc_menu = False
            rect = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            rect.fill((125, 103, 73, 2))
            screen.blit(rect, (0, 0))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = False
                        game = True
                        flag_continue_esc_menu = False
                        flag_exit_esc_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if finish:
            text = font.render(f"You made it! Score:{score}", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                update_source(score)
                return 1
            if flag_continue_esc_menu:
                clear()
                update_source(score)
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if game_over:
            text = font.render(f"Game Over", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                clear()
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        clock.tick(FPS)
    return True


def intro5(screen):
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load("data/space_intro1.jpg"), (800, 600))
    screen.blit(fon, (0, 0))
    intro_text = ["Прямая дорога", "",
                  "Наконец, все закончилось и остался прямой путь",
                  "до Альдераана. Долетите до планеты!"]
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return 0
        pygame.display.flip()
        clock.tick(FPS)


def level5(screen):
    intro5(screen)
    planet = pygame.sprite.Sprite()
    planet.image = pygame.image.load("data/planet_38.png")
    planet.rect = planet.image.get_rect()
    planet.rect.x = 120
    planet.rect.y = -2100
    bg = pygame.transform.scale(pygame.image.load("data/space_rt.png"), (800, 2600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    running = True
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BULLETS)
    all_sprites.add(planet)
    ship = Ship(all_sprites)
    ship.set_health()
    ship.set_health()
    n = -2000
    score = 0
    flag = True
    continue_esc_menu = Button((300, 200), "Продолжить", 200)
    exit_esc_menu = Button((300, 250), "Выйти в главное меню", 200)
    flag_continue_esc_menu = False
    flag_exit_esc_menu = False
    game = True
    esc = False
    game_over = False
    finish = False
    while running:
        if game:
            if flag and n < -400:
                Meteorite(all_sprites)
                flag = False
            if n % 12 == 0:
                flag = True
            screen.blit(bg, (0, n))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True
                        game = False
            all_sprites.draw(screen)
            all_sprites.update(pygame.key.get_pressed())
            pygame.draw.rect(screen, (0, 255, 0), (0, 595, ship.health, 5))
            pygame.display.flip()
            n += 1
            planet.rect.y += 1
            if pygame.sprite.groupcollide(BULLETS, METEORITES, True, True):
                score += 50
                BULLETS.update("kill")
            if n >= 0 or ship.health <= 0:
                if n >= 0:
                    ship.end_level(all_sprites, screen, bg)
                    game = False
                    finish = True
                elif ship.health <= 0:
                    game = False
                    game_over = True
                    ship.destroy(all_sprites, screen, bg, n)
                clear()
        if esc:
            text = font.render(f"Пауза", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                esc = False
                game = True
                flag_continue_esc_menu = False
            rect = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            rect.fill((20, 20, 20, 1))
            screen.blit(rect, (0, 0))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = False
                        game = True
                        flag_continue_esc_menu = False
                        flag_exit_esc_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if finish:
            text = font.render(f"You made it! Score:{score}", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                update_source(score)
                return 1
            if flag_continue_esc_menu:
                clear()
                update_source(score)
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if game_over:
            text = font.render(f"Game Over", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                clear()
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        clock.tick(FPS)
    return True


def intro6(screen):
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load("data/spase_inro6.jpg"), (800, 600))
    screen.blit(fon, (0, 0))
    intro_text = ["Последние приключения", "",
                  "Вы прилетели на Альдераан, но вот незадача. Здесь вас ждало",
                  "поткрепление сепаратистов. Сбейти их корабли, и доберитесь",
                  "до места назначения"]
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return 0
        pygame.display.flip()
        clock.tick(FPS)


def level6(screen):
    intro6(screen)
    bg = pygame.transform.scale(pygame.image.load("data/bg1.png"), (800, 2600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    running = True
    all_sprites = pygame.sprite.Group()
    all_sprites.add(BULLETS)
    all_sprites.add(PIRATES_BULLETS)
    ship = Ship(all_sprites)
    ship.set_health()
    ship.set_health()
    n = -2000
    score = 0
    flag = True
    game = True
    esc = False
    game_over = False
    finish = False
    continue_esc_menu = Button((300, 200), "Продолжить", 200)
    exit_esc_menu = Button((300, 250), "Выйти в главное меню", 200)
    flag_continue_esc_menu = False
    flag_exit_esc_menu = False
    while running:
        if game:
            if flag and n < -100:
                Pirate(all_sprites, flag=True)
                flag = False
            if n % 40 == 0:
                flag = True
            if n % 60 == 0:
                Boss(all_sprites)
            screen.blit(bg, (0, n))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            pygame.draw.rect(screen, (0, 255, 0), (0, 595, ship.health, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = True
                        game = False
            all_sprites.draw(screen)
            all_sprites.update(pygame.key.get_pressed())
            pygame.display.flip()
            n += 1
            if pygame.sprite.groupcollide(BULLETS, PIRATES, True, True):
                score += 150
                BULLETS.update("kill")
            if n >= 0 or ship.health <= 0:
                if n >= 0:
                    ship.end_level(all_sprites, screen, bg, mode=True)
                    game = False
                    finish = True
                elif ship.health <= 0:
                    game = False
                    game_over = True
                    ship.destroy(all_sprites, screen, bg, n)
                clear()
        if esc:
            text = font.render(f"Пауза", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                esc = False
                game = True
                flag_continue_esc_menu = False
            rect = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
            rect.fill((125, 103, 73, 2))
            screen.blit(rect, (0, 0))
            text = font.render(f"Score: {score}", True, (255, 0, 0))
            screen.blit(text, (0, 0))
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc = False
                        game = True
                        flag_continue_esc_menu = False
                        flag_exit_esc_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if finish:
            text = font.render(f"You made it! Score:{score}", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                update_source(score)
                return 1
            if flag_continue_esc_menu:
                clear()
                update_source(score)
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        if game_over:
            text = font.render(f"Game Over", True, (255, 0, 0))
            screen.blit(text, (300, 150))
            if flag_exit_esc_menu:
                clear()
                return 1
            if flag_continue_esc_menu:
                clear()
                return 'continue'
            continue_esc_menu.draw(screen)
            exit_esc_menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        flag_continue_esc_menu = continue_esc_menu.update(event.pos)
                        flag_exit_esc_menu = exit_esc_menu.update(event.pos)
            pygame.display.flip()
        clock.tick(FPS)
    return True


def finish_screen(screen):
    flag_exit_esc_menu = False
    exit_esc_menu = Button((300, 450), "Выйти в главное меню", 200)
    screen.fill((0, 0, 0))
    running = True
    clock = pygame.time.Clock()
    fon = pygame.transform.scale(pygame.image.load("data/spase_inro6.jpg"), (800, 600))
    score = get_score()
    screen.blit(fon, (0, 0))
    intro_text = ["Конец испытаний", "",
                  "Вы успешно прошли все испытания!",
                  "Вы проявили мужество и отвагу, за что получили"
                  "награду от Республики.",
                  f"Спасибо за игру! Твой итоговый счет:{score}"]
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while running:
        exit_esc_menu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    flag_exit_esc_menu = exit_esc_menu.update(event.pos)
        if flag_exit_esc_menu:
            clear()
            return 1
        pygame.display.flip()
        clock.tick(FPS)
