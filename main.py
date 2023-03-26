import random
import pygame
import os
# init mixer for sound and font for writing on screen
pygame.mixer.init()
pygame.font.init()

# create global variable fps and assign it value 60 (frame per seconds)
fps = 60
# load 2 sound files
laser = pygame.mixer.Sound(os.path.join('assets', 'laser1.wav'))
hit_sound = pygame.mixer.Sound(os.path.join('assets', 'Explosion_02.wav'))
# create a font variable
font = pygame.font.Font('freesansbold.ttf', 32)
# create global variable level for kipping level number
level = 1
# create a new event for next level situation
next_level = pygame.USEREVENT + 1


# create class Ship for human ship
class Ship:
    def __init__(self, window, colors):
        # ship dimensions
        self.width = 60
        self.height = 48
        # define ship speed
        self.speed = 5
        # create object in current class of window and colors classes for accessing methods from this classes
        self.window = window
        self.colors = colors
        # define rectangle for human ship
        self.ship_rect = pygame.Rect(self.window.width/2 - self.width/2, self.window.height - 10 - self.height,
                                     self.width, self.height)
        # load image for human ship
        self.ship_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'spaceship.png')), (60, 48))
        # load image for explosion
        self.image_explosion = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'explosion.png')),
                                                      (60, 48))
        # create a list to store human bullet
        self.bullet = []
        # create life bar rect
        self.life_rect = pygame.Rect(self.ship_rect.x, self.ship_rect.y + self.height + 5, 60, 5)
        # create a bool variable that is True if not all aliens ships was killed
        self.not_all_aliens_killed = True

    # create method for draw human ship
    def draw_ship(self):
        # draw human ship only if live is > 0
        if self.life_rect.width > 0:
            # draw on current screen at human ship x and y ship image
            Window.return_win(self.window).blit(self.ship_image, (self.ship_rect.x, self.ship_rect.y))
            # draw on current screen life bar for human ship
            pygame.draw.rect(self.window.win, self.colors.green, self.life_rect)
        else:
            # if human ship life = 0 draw on current screen at human ship x and y image for explosion
            Window.return_win(self.window).blit(self.image_explosion, (self.ship_rect.x, self.ship_rect.y))
            # create a text variable with white color
            text = font.render('GAME OVER!', True, (255, 255, 255))
            text_rect = text.get_rect()
            # set text center to middle of screen
            text_rect.center = (self.window.width // 2, self.window.height // 2)
            # display text on window at above coordinate
            Window.return_win(self.window).blit(text, text_rect)

    # method for human ship movement
    def ship_move(self):
        # if human ship live > 0 and not all alien ships was killed move human ship
        if self.life_rect.width > 0 and self.not_all_aliens_killed:
            # create a list with all key pressed
            keys_pressed = pygame.key.get_pressed()
            # move left
            if keys_pressed[pygame.K_LEFT] and self.ship_rect.left - self.speed >= 0:
                self.ship_rect.x -= self.speed
                self.life_rect.x = self.ship_rect.x
            # move right
            if keys_pressed[pygame.K_RIGHT] and self.ship_rect.right + self.speed <= self.window.width:
                self.ship_rect.x += self.speed
                self.life_rect.x = self.ship_rect.x

    # method for creating human bullets
    def create_bullets(self):
        # if human ship live > 0, not all alien ships was killed and bullets nr < 6 create another bullet
        if self.life_rect.width > 0 and self.not_all_aliens_killed and len(self.bullet) < 6:
            keys_pressed = pygame.key.get_pressed()
            # create new bullet if space key is pressed
            if keys_pressed[pygame.K_SPACE]:
                # create rec af new bullet based on current human ship position
                new_bullet = pygame.Rect(int(self.ship_rect.midtop[0]) - 2, int(self.ship_rect.midtop[1]) - 10, 4, 10)
                # append new bullet in human ship bullet list
                self.bullet.append(new_bullet)
                # play sound for creating a new bullet
                laser.play()
        # for all bullet in list subtract 5 at y for moving
        for bullet in self.bullet:
            bullet[1] -= 5
            if bullet[1] <= 0:
                # if bullet y is above 0 remove it from bullets list
                self.bullet.remove(bullet)

    # draw bullets
    def draw_bullets(self):
        # if not all alien ship was killed draw bullets
        if self.not_all_aliens_killed:
            for bullet in self.bullet:
                # for all bullets draw on screen bullet rec with red color
                pygame.draw.rect(Window.return_win(self.window), self.colors.red, bullet)

    def return_human_bullet_list(self):
        return self.bullet

    def return_human_ship(self):
        return self.ship_rect

    def return_human_life(self):
        return self.life_rect

    def not_get_all_aliens_killed(self):
        return self.not_all_aliens_killed

    def change_not_all_aliens_killed(self, value):
        self.not_all_aliens_killed = value


# create class for alien ships
class AliensShips:
    def __init__(self, window, colors, ship):
        # dimensions
        self.width = 60
        self.height = 48
        # define ship velocity
        self.speed = 2
        # create object in current class of window, colors and ship classes for accessing methods from this classes
        self.window = window
        self.colors = colors
        self.ship = ship
        # define rectangle for alien ship
        self.aliens_ship_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'alien2.png')), (60,
                                                                                                                  48))
        # create a list to store bullet
        self.aliens_ships_list = []
        # create rec for alien life
        self.alien_life_rect = (0, 0, 0, 0)
        # create list to store alien ships life
        self.aliens_life_list = []
        # create a list to store alin ships bullets
        self.aliens_bullet = []
        # create a value for move alin ships
        self.move_nr = 1
        self.shot_timer = 0

    # generate aliens and life for level 1
    def generate_aliens_l1(self):
        for x in [100, 200, 300, 400, 500, 600, 700]:
            # define rectangle for alien ship
            self.aliens_ship_rect = pygame.Rect(x, 100, self.width, self.height)
            # define rectangle for alien live
            self.alien_life_rect = pygame.Rect(self.aliens_ship_rect.x, self.aliens_ship_rect.y - 5, 60, 5)
            # if alien ship rectangle is not in aliens ship list append it
            if self.aliens_ship_rect not in self.aliens_ships_list:
                self.aliens_ships_list.append(self.aliens_ship_rect)
                # append aliens ship live in aliens life list
                self.aliens_life_list.append(self.alien_life_rect)

    # generate aliens and life for level 2
    def generate_aliens_l2(self):
        for x in [100, 200, 300, 400, 500, 600, 700]:
            for y in [100, 300]:
                # rec for alien ship
                self.aliens_ship_rect = pygame.Rect(x, y, self.width, self.height)
                # rec for aliens life
                self.alien_life_rect = pygame.Rect(self.aliens_ship_rect.x, self.aliens_ship_rect.y - 5, 60, 5)
                if self.aliens_ship_rect not in self.aliens_ships_list:
                    self.aliens_ships_list.append(self.aliens_ship_rect)
                    self.aliens_life_list.append(self.alien_life_rect)

    # draw aliens ships and life
    def draw_aliens_ships(self):
        for ship in self.aliens_ships_list:
            Window.return_win(self.window).blit(self.aliens_ship_image, (ship.x, ship.y))
        for life in self.aliens_life_list:
            pygame.draw.rect(self.window.win, self.colors.green, life)

    # move alien ships
    def aliens_ship_move(self):
        if self.move_nr % 40 == 0:
            for index in range(0, len(self.aliens_ships_list)):
                self.aliens_ships_list[index][0] += 15
        elif self.move_nr % 40 == 10:
            for index in range(0, len(self.aliens_ships_list)):
                self.aliens_ships_list[index][1] -= 15
        elif self.move_nr % 40 == 20:
            for index in range(0, len(self.aliens_ships_list)):
                self.aliens_ships_list[index][0] -= 15
        elif self.move_nr % 40 == 30:
            for index in range(0, len(self.aliens_ships_list)):
                self.aliens_ships_list[index][1] += 15
        self.move_nr += 1

    # check if aliens ship is hit
    def check_alien_ship_hit(self):
        for bullet in Ship.return_human_bullet_list(self.ship):
            for ship in self.aliens_ships_list:
                # check if human bullet hit alien ships
                if pygame.Rect.colliderect(bullet, ship):
                    # play hit sound
                    hit_sound.play()
                    # if bullet hit remove bullet from human bullets list
                    Ship.return_human_bullet_list(self.ship).remove(bullet)
                    # find position of current alien ship in alien ships list
                    # alien ships at index have life at alien life list same index
                    index = self.aliens_ships_list.index(ship)
                    # if hit alien ship life > 6 subtract 6
                    if self.aliens_life_list[index][2] >= 6:
                        self.aliens_life_list[index][2] -= 6
                    # if hit alien ship life = 0 remove current alien ship from alien ships list and remove current
                    # alien ship life from alien ships live list
                    if self.aliens_life_list[index][2] == 0:
                        self.aliens_life_list.remove(self.aliens_life_list[index])
                        self.aliens_ships_list.remove(ship)
                    # if all alien ships is killed
                    if len(self.aliens_ships_list) == 0:
                        # change value of not_all_aliens_killed from ship class to False
                        Ship.change_not_all_aliens_killed(self.ship, False)
                        # create next_level event
                        pygame.event.post(pygame.event.Event(next_level))

    def alien_ship_shot(self):
        # if human live and aliens ships number > 0 alien ships shot
        if Ship.return_human_life(self.ship)[2] > 0 and len(self.aliens_ships_list) > 0:
            # use self.shot_timer to make alien ships to shot one time in 8 while loop from main
            if self.shot_timer % 8 == 4:
                # choice o random alien ship from all ships
                ship_nr_1 = random.randint(0, len(self.aliens_ships_list) - 1)
                # create rect af new bullet in from of alien ship choice above
                new_aliens_bullet = pygame.Rect(self.aliens_ships_list[ship_nr_1][0] + self.width/2, self.
                                                aliens_ships_list[ship_nr_1][1] + self.height, 4, 10)
                # append new bullet in alien ships bullets list
                self.aliens_bullet.append(new_aliens_bullet)
                # play shot sound
                laser.play()
            # move alien ships bullets
            for bullet in self.aliens_bullet:
                # increase each bullet y coordinate
                bullet[1] += 5
                # if bullet y coordinate > window.height delete current bulet from list
                if bullet[1] >= self.window.height:
                    self.aliens_bullet.remove(bullet)
            # increment self.shot_timer at every iteration
            self.shot_timer += 1

    # draw aliens bullets method
    def draw_aliens_bullets(self):
        for bullet in self.aliens_bullet:
            if level == 1:
                pygame.draw.rect(Window.return_win(self.window), self.colors.yellow, bullet)
            if level == 2:
                pygame.draw.rect(Window.return_win(self.window), self.colors.blue, bullet)

    def check_if_human_ship_is_hit(self):
        for bullet in self.aliens_bullet:
            # if any alien bullets hit human ship
            if pygame.Rect.colliderect(bullet, Ship.return_human_ship(self.ship)):
                # remove alien bullet
                self.aliens_bullet.remove(bullet)
                hit_sound.play()
                # if human life >= 6 subtract 6 from human ship life
                if Ship.return_human_life(self.ship).width >= 6:
                    Ship.return_human_life(self.ship).width -= 6

    def game_win(self):
        if not Ship.not_get_all_aliens_killed(self.ship):
            # create a text variable
            text = font.render('YOU DEFEATED ALL ALIENS!', True, (0, 255, 0))
            text_rect = text.get_rect()
            # set text center to middle of screen
            text_rect.center = (self.window.width // 2, self.window.height // 2)
            # display text on window
            self.window.win.blit(text, text_rect)
            pygame.display.update()
            # update window after write text


# this class contain colors
class Colors:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.blue = (0, 0, 255)


class Window:
    global level

    def __init__(self):
        # window dimension
        self.width = 840
        self.height = 624
        # create a window and display it
        self.win = pygame.display.set_mode((self.width, self.height))
        # set win title
        pygame.display.set_caption("Alien invasion!")
        self.image_l1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background1.PNG')), (840, 624))
        self.image_l2 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background2.jpg')), (840, 624))

    def draw_window(self):
        # draw image
        if level == 1:
            self.win.blit(self.image_l1, self.image_l1.get_rect())
        if level == 2:
            self.win.blit(self.image_l2, self.image_l1.get_rect())

        # create a text variable
        text = font.render(f'LEVEL: {level}', True, (0, 255, 0))
        text_rect = text.get_rect()
        # set text center to middle of screen
        text_rect.x = 0
        text_rect.y = 0
        # display text on window
        self.win.blit(text, text_rect)
        # update window after write text

    def return_win(self):
        return self.win


def main():
    global level
    run = True
    clock = pygame.time.Clock()
    window = Window()
    colors = Colors()
    ship = Ship(window, colors)
    aliens = AliensShips(window, colors, ship)
    if level == 1:
        aliens.generate_aliens_l1()
    if level == 2:
        aliens.generate_aliens_l2()
    while run:
        clock.tick(fps)
        window.draw_window()
        ship.draw_ship()
        aliens.draw_aliens_ships()
        ship.ship_move()
        ship.create_bullets()
        ship.draw_bullets()
        aliens.aliens_ship_move()
        aliens.check_alien_ship_hit()
        aliens.alien_ship_shot()
        aliens.draw_aliens_bullets()
        aliens.check_if_human_ship_is_hit()
        aliens.game_win()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == next_level:
                if level == 1:
                    level += 1
                    main()
                if level == 2:
                    aliens.game_win()

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
