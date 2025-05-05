import pygame, random, sys
from map import *

pygame.init()
pygame.joystick.init()
pygame.mixer.init()
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick başarıyla bağlandı.")
else:
    joystick = None
    print("Joystick bağlanmadı.")

class Map():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/gm.png'), pygame.Rect(x, y, 2240, 2240)
    def draw(self):
        ekran.blit(self.image,self.rect)
class Map2():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/gm2.png'), pygame.Rect(x, y, 2240, 2240)
    def draw(self):
        ekran.blit(self.image,self.rect)
class Map3():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/gm3.png'), pygame.Rect(x, y, 2240, 2240)
    def draw(self):
        ekran.blit(self.image,self.rect)
class Map4():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/gm4.png'), pygame.Rect(x, y, 2240, 2240)
    def draw(self):
        ekran.blit(self.image,self.rect)

class Wall():
    def __init__(self, x, y, en, boy):        
        self.x, self.y, self.en, self.boy = x, y, en, boy
        self.rect = pygame.Rect(x, y, self.en, self.boy)

    def draw(self):
        pygame.draw.rect(ekran,(233,231,23),self.rect)

class Alien(): 
    def __init__(self, x, y, en, boy, speed, alien_type):  
        self.images = {
            'idle': pygame.image.load('img/alien.png'),
            'idle2': pygame.image.load('img/alien2.png')
        }
        self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 114, 41, 57)) 
        self.x, self.y = x, y
        self.en, self.boy = en, boy
        self.rect = pygame.Rect(self.x, self.y, self.en, self.boy)
        self.speed = speed
        self.gravity = 0.5  
        self.vertical_speed = 0  
        self.on_ground = False  
        self.move_direction, self.move_status = "right",  0
        self.animation_time = 0
        self.health = 50
        self.animation_frame = 0
        self.bullets = []
        self.shoot_cooldown = 0
        self.alien_type = alien_type
        self.right_imgs = [(0, 0, 44, 57),(44, 0, 44, 57),(88, 0, 41, 57),(129, 0, 41, 57),(170, 0, 41, 57),(211, 0, 41, 57)]
        self.left_imgs = [(0, 57, 41, 57),(44, 57, 44, 57),(88, 57, 44, 57),(129, 57, 41, 57),(170, 57, 41, 57),(211, 57, 41, 57)]
        
    def apply_gravity(self, walls):
        if not self.on_ground:
            self.vertical_speed += self.gravity
        else:
            self.vertical_speed = 0 
        self.rect.y += self.vertical_speed

        self.on_ground = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.vertical_speed > 0:
                    self.rect.bottom = wall.rect.top  
                    self.on_ground = True

    def move(self):
        moving_horizontally = False
        moving_vertically = False
        original_position = self.rect.topleft

        distance_threshold = 350 
        if 40 < abs(player.rect.x - self.rect.x) <= distance_threshold and abs(player.rect.y - self.rect.y) <= distance_threshold:
            if player.rect.x > self.rect.x:
                self.rect.x += 2
                self.move_direction = "right"
                moving_horizontally = True            
            if player.rect.x < self.rect.x:
                self.rect.x -= 2 
                self.move_direction = "left"
                moving_horizontally = True         
        if abs(player.rect.x - self.rect.x) <= distance_threshold and abs(player.rect.y - self.rect.y) <= 20:       
            if self.shoot_cooldown == 0:
                bullet_x = self.rect.centerx - 5
                bullet_y = self.rect.centery + 1
                if self.alien_type == 'alien1':
                  self.bullets.append(Bullet(bullet_x, bullet_y, self.move_direction, (123,233,21)))
                if self.alien_type == 'alien2':
                  self.bullets.append(Bullet(bullet_x, bullet_y, self.move_direction, (123,12,255)))
                self.shoot_cooldown = 40
                laser.play() 

        if moving_horizontally or moving_vertically:
            self.move_status = 1
        else:
            self.move_status = 0

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.topleft = original_position
                moving_horizontally = False
                moving_vertically = False
                self.move_status = 0
                break
        if self.rect.colliderect(wall2.rect):
            self.rect.topleft = original_position
            moving_horizontally = False
            moving_vertically = False
            self.move_status = 0

        if self.move_status == 1:
            self.animation_time += 1
            if self.move_direction == "right":
                if self.animation_time >= 10:
                    self.animation_frame = (self.animation_frame + 1) % len(self.right_imgs)
                    frame_rect = pygame.Rect(self.right_imgs[self.animation_frame])
                    if self.alien_type == 'alien1':
                      self.endimage = self.images["idle"].subsurface(frame_rect)
                    if self.alien_type == 'alien2':
                      self.endimage = self.images["idle2"].subsurface(frame_rect)
                    self.animation_time = 0
            elif self.move_direction == "left":
                if self.animation_time >= 10:
                    self.animation_frame = (self.animation_frame + 1) % len(self.left_imgs)
                    frame_rect = pygame.Rect(self.left_imgs[self.animation_frame])
                    if self.alien_type == 'alien1':
                      self.endimage = self.images["idle"].subsurface(frame_rect)
                    if self.alien_type == 'alien2':
                      self.endimage = self.images["idle2"].subsurface(frame_rect)
                    self.animation_time = 0
        else:  
            if self.move_direction == "right" or player.rect.x > self.rect.x and player.rect.y > self.rect.y:
                if self.alien_type == 'alien1':
                    self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 114, 41, 57)) 
                if self.alien_type == 'alien2':
                    self.endimage = self.images["idle2"].subsurface(pygame.Rect(0, 114, 41, 57)) 
            elif self.move_direction == "left" or player.rect.x < self.rect.x and player.rect.y > self.rect.y:
                if self.alien_type == 'alien1':
                    self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 171, 41, 57)) 
                if self.alien_type == 'alien2':
                    self.endimage = self.images["idle2"].subsurface(pygame.Rect(0, 171, 41, 57)) 

    def draw_health_bar(self):
        pygame.draw.rect(ekran, (0, 0, 0), (self.rect.x-2, self.rect.y-17, 54, 14))
        pygame.draw.rect(ekran, (255, 0, 0), (self.rect.x, self.rect.y-15, 50, 10))
        pygame.draw.rect(ekran, (0, 255, 0), (self.rect.x, self.rect.y-15, self.health, 10))

    def draw(self):
        for bullet in self.bullets:
            bullet.update()
            for wall in walls:
                if bullet.rect.colliderect(wall.rect):
                    try:
                      self.bullets.remove(bullet)
                    except:
                        print('olmadı')
            if bullet.rect.colliderect(wall2.rect):
                try:
                    self.bullets.remove(bullet)
                except:
                    print('olmadı')
        self.bullets = [b for b in self.bullets if 0 <= b.rect.x <= width]
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        ekran.blit(self.endimage, self.rect)

    def player_attack_hit(self):
        for bullet in player.bullets:
          if self.rect.colliderect(bullet.rect):
            self.health -= 14.5
            player.bullets.remove(bullet)
        for alien in aliens:
            if alien.health <= 0:
                aliens.remove(alien)
        for alien2 in aliens2:
            if alien2.health <= 0:
                aliens2.remove(alien2)

    def update(self, walls):
        self.apply_gravity(walls)
        self.draw()
        if player.died_end == 0:
            self.draw_health_bar()
            self.player_attack_hit()
            self.move()

class BossAlien(): 
    def __init__(self, x, y, en, boy, speed):  
        self.images = {
            'idle': pygame.image.load('img/bossalien.png')
        }
        self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 0, 106, 78)) 
        self.x, self.y = x, y
        self.en, self.boy = en, boy
        self.rect = pygame.Rect(self.x, self.y, self.en, self.boy)
        self.speed = speed
        self.move_direction, self.move_status, self.direction = "right",  0, 'right'
        self.health = 100
        self.bullets = []
        self.shoot_cooldown = 0
        self.moved = 0
        self.wall_hit = 0
        self.died = 0
        
    def move(self):
        moving_horizontally = False
        moving_vertically = False
        original_position = self.rect.topleft

        distance_threshold = 950 
        if 80 <= abs(player.rect.x - self.rect.x) <= distance_threshold and abs(player.rect.y - self.rect.y) <= distance_threshold:
            self.moved = 1
            if player.rect.x > self.rect.x:
                self.rect.x += 2
                self.move_direction = "right"
                self.direction = 'right'
                moving_horizontally = True            
            if player.rect.x < self.rect.x:
                self.rect.x -= 2 
                self.move_direction = "left"
                self.direction = 'left'
                moving_horizontally = True                     
            if player.rect.y > self.rect.y:
                self.rect.y += 2
                moving_horizontally = True  
                self.direction = 'up'          
            if player.rect.y < self.rect.y:
                self.rect.y -= 2 
                moving_horizontally = True  
                self.direction = 'down'  
        else:
            self.moved = 0
        if abs(player.rect.x - self.rect.x) <= distance_threshold and abs(player.rect.y - self.rect.y):       
            if self.shoot_cooldown == 0:
                bullet_x = self.rect.centerx - 10
                bullet_y = self.rect.centery + 1
                self.bullets.append(Bullet(bullet_x, bullet_y, self.move_direction, (123,233,21)))
                self.shoot_cooldown = 40
                laser.play() 

        if moving_horizontally or moving_vertically:
            self.move_status = 1
        else:
            self.move_status = 0

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.topleft = original_position
                moving_horizontally = False
                moving_vertically = False
                self.move_status = 0
                self.wall_hit = 1
                break
            else: 
                self.wall_hit = 0

        if self.move_direction == "right":
            self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 0, 106, 78)) 
        elif self.move_direction == "left":
            self.endimage = self.images["idle"].subsurface(pygame.Rect(106, 0, 106, 78)) 

    def draw_health_bar(self):
        pygame.draw.rect(ekran, (0, 0, 0), (self.rect.x-2, self.rect.y-17, 104, 14))
        pygame.draw.rect(ekran, (255, 0, 0), (self.rect.x, self.rect.y-15, 100, 10))
        pygame.draw.rect(ekran, (0, 255, 0), (self.rect.x, self.rect.y-15, self.health, 10))

    def draw(self):
        for bullet in self.bullets:
            bullet.update()
            for wall in walls:
                if bullet.rect.colliderect(wall.rect):
                    self.bullets.remove(bullet)
        self.bullets = [b for b in self.bullets if 0 <= b.rect.x <= width]
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        ekran.blit(self.endimage, self.rect)

    def player_attack_hit(self):
        for bullet in player.bullets:
          if self.rect.colliderect(bullet.rect):
            self.health -= random.randint(5,12)
            player.bullets.remove(bullet)

    def update(self):
        self.draw()
        if player.died_end == 0:
            self.draw_health_bar()
            self.player_attack_hit()
            self.move()
        if self.health <= 0:
            self.died = 1

class Oxygen():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/oxygen.png'), pygame.Rect(x, y, 32, 32)
    def draw(self):
        ekran.blit(self.image,self.rect)

class Weapon():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/weapon.png'), pygame.Rect(x, y, 32, 32)
    def draw(self):
        ekran.blit(self.image,self.rect)

class HpBattery():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/healthbattery.png'), pygame.Rect(x, y, 32, 32)
    def draw(self):
        ekran.blit(self.image,self.rect)

class Player():
    def __init__(self, x, y, en, boy, speed):  
        self.images = {
            'idle': pygame.image.load('img/playerimage.png'),
            'idle2': pygame.image.load('img/player2.png'),
        }
        self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 0, 33, 57)) 
        self.x = x
        self.y = y
        self.en = en
        self.boy = boy
        self.rect = pygame.Rect(self.x, self.y, self.en, self.boy)
        self.speed = speed
        self.health, self.max_health = 200, 200
        self.oxygen, self.max_oxygen = 200, 200
        self.move_direction = "stay"
        self.direction = "right"
        self.end = 0
        self.move_status = 0
        self.velocity_y = 0  
        self.on_ground = False 
        self.animation_time = 0
        self.animation_frame= 0
        self.weapon_hit = 0
        self.player_move = 1
        self.border1, self.border2, self.border3 = 0, 0, 0
        self.attack = 0        
        self.gravity = 0.4 
        self.jump_strength = -10  
        self.max_fall_speed = 3 
        self.bullets = []
        self.shoot_cooldown = 0
        self.player_wall_hit = 0
        self.attack_time = 0
        self.wallborderhit = 0
        self.died, self.died_time, self.died_end = 0, 0, 0
        self.died_frame = 0
        self.border_hit, self.border_time,self.border_hit2, self.border_time2,self.border_hit3, self.border_time3 = 0,0,0,0,0,0
        self.right_imgs,self.left_imgs = [(0, 114, 33, 57),(33, 114, 33, 57),(66, 114, 33, 57),(99, 114, 33, 57),(132, 114, 33, 57),(165, 114, 33, 57)], [(0, 171, 33, 57),(33, 171, 33, 57),(66, 171, 33, 57),(99, 171, 33, 57),(132, 171, 33, 57),(165, 171, 33, 57)]
        self.attack_right_imgs,self.attack_left_imgs = [(66, 0, 45, 57),(111, 0, 45, 57),(156, 0, 42, 57),(198, 0, 42, 57),(240, 0, 42, 57),(84, 57, 42, 57)], [(0, 228, 45, 57),(45, 228, 45, 57),(90, 228, 42, 57),(132, 228, 42, 57),(174, 228, 42, 57),(216, 228, 42, 57)]
        self.died_imgs, self.died_imgs_left = [(126, 57, 33, 57),(159, 57, 33, 57),(192, 57, 33, 57),(225, 57, 33, 57),(258, 57, 33, 57)],[(198, 114, 33, 57),(231, 114, 33, 57),(264, 114, 33, 57),(198, 171, 33, 57),(231, 171, 33, 57)]

    def move(self):
        if self.died == 0:
            global game_menu
            key = pygame.key.get_pressed()

            joystick_x = 0
            joystick_buttons = []

            if joystick:
                joystick_x = joystick.get_axis(0)  
                joystick_buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

            if self.border1 == 0 and self.border2 == 0 and self.border3 == 0:
              self.oxygen -= 0.23
            else:
                self.oxygen += 0.5
            if self.oxygen <= 0:
                self.oxygen = 0
                self.health -= 0.7

            if key[pygame.K_SPACE] or (joystick and joystick_buttons and joystick_buttons[1]):
                self.attack = 1            
                if self.shoot_cooldown == 0:
                    if self.direction == "right":
                      bullet_x = self.rect.centerx + 5
                    if self.direction == "left":
                      bullet_x = self.rect.centerx - 5
                    bullet_y = self.rect.centery + 1
                    self.bullets.append(Bullet(bullet_x, bullet_y, self.direction,(255,0,0)))
                    self.shoot_cooldown = 40                    
                    laser.play() 
            else:
                if self.attack_time >= 70:
                  self.attack = 0
                  self.attack_time = 0

            if self.attack == 1:
                self.attack_time += 1

            if self.player_move == 1:
                if key[pygame.K_d] or key[pygame.K_RIGHT] or (joystick and joystick_x > 0.3):
                    self.rect.x += self.speed
                    self.move_direction = "right"
                    self.direction = "right"
                    self.move_status = 1
                elif key[pygame.K_a] or key[pygame.K_LEFT] or (joystick and joystick_x < -0.3):
                    self.rect.x -= self.speed
                    self.move_direction = "left"
                    self.direction = "left"
                    self.move_status = 1
                else:
                    self.move_direction = "stay"
                    self.move_status = 0

            if ((key[pygame.K_UP] or key[pygame.K_w]) or (joystick and joystick_buttons and joystick_buttons[0])) and self.on_ground and self.player_wall_hit == 0:
                    jump.play()
                    self.velocity_y = self.jump_strength 
                    self.on_ground = False  

            self.velocity_y += self.gravity 
            if self.velocity_y > self.max_fall_speed:
                self.velocity_y = self.max_fall_speed  

            self.rect.y += self.velocity_y

            if self.rect.y + self.boy >= height:
                self.rect.y = height - self.boy  
                self.on_ground = True  
                self.velocity_y = 0  
            else:
                self.on_ground = False

            if self.rect.x <= 100:
                self.rect.x = 100
            if self.rect.x >= 566 - self.en:
              self.rect.x = 566 - self.en

            if self.move_status == 1 and self.attack == 0 and self.end == 0:
                self.animation_time += 1
                if self.move_direction == "right":
                    if self.animation_time >= 12:
                        self.animation_frame = (self.animation_frame + 1) % len(self.right_imgs)
                        frame_rect = pygame.Rect(self.right_imgs[self.animation_frame])
                        self.endimage = self.images["idle"].subsurface(frame_rect)
                        self.animation_time = 0
                elif self.move_direction == "left":
                    if self.animation_time >= 12:
                        self.animation_frame = (self.animation_frame + 1) % len(self.left_imgs)
                        frame_rect = pygame.Rect(self.left_imgs[self.animation_frame])
                        self.endimage = self.images["idle"].subsurface(frame_rect)
                        self.animation_time = 0
            if self.move_status == 0 and self.died == 0 and self.end == 0:
                if self.attack == 0:
                    if self.direction == "right":
                        self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 0, 33, 57))
                    elif self.direction == "left":
                        self.endimage = self.images["idle"].subsurface(pygame.Rect(33, 0, 33, 57))

            if self.attack == 1:
                if self.move_status == 0:
                    if self.direction == "right":
                        self.endimage = self.images["idle"].subsurface(pygame.Rect(0, 57, 42, 57))
                    if self.direction == "left":
                        self.endimage = self.images["idle"].subsurface(pygame.Rect(42, 57, 42, 57))
                if self.move_status == 1:
                    self.animation_time += 1
                    if self.move_direction == "right":
                        if self.animation_time >= 12:
                            self.animation_frame = (self.animation_frame + 1) % len(self.attack_right_imgs)
                            frame_rect = pygame.Rect(self.attack_right_imgs[self.animation_frame])
                            self.endimage = self.images["idle"].subsurface(frame_rect)
                            self.animation_time = 0
                    if self.move_direction == "left":
                        if self.animation_time >= 12:
                            self.animation_frame = (self.animation_frame + 1) % len(self.attack_left_imgs)
                            frame_rect = pygame.Rect(self.attack_left_imgs[self.animation_frame])
                            self.endimage = self.images["idle"].subsurface(frame_rect)
                            self.animation_time = 0
        
        if self.died == 1:
            self.player_move = 0
            self.animation_time += 1
            self.died_time += 1
            if self.direction == "right":
                if self.animation_time >= 12:
                    self.died_frame += 1
                    self.animation_frame = (self.animation_frame + 1) % len(self.died_imgs)
                    frame_rect = pygame.Rect(self.died_imgs[self.animation_frame])
                    self.endimage = self.images["idle"].subsurface(frame_rect)
                    self.animation_time = 0
                if self.died_frame >= 4:
                    self.died_end = 1
            if self.direction == "left":
                if self.animation_time >= 12:
                    self.died_frame += 1
                    self.animation_frame = (self.animation_frame + 1) % len(self.died_imgs_left)
                    frame_rect = pygame.Rect(self.died_imgs_left[self.animation_frame])
                    self.endimage = self.images["idle"].subsurface(frame_rect)
                    self.animation_time = 0
                if self.died_frame >= 4:
                    self.died_end = 1

    def wall_hit(self):        
        self.player_wall_hit = 0
        for wall in walls:
          if self.rect.colliderect(wall.rect):
                if self.velocity_y > 0 and self.rect.bottom > wall.rect.top and self.rect.top < wall.rect.top:
                    self.rect.bottom = wall.rect.top
                    self.on_ground = True
                    self.velocity_y = 0

                elif self.velocity_y < 0 and self.rect.top < wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                    self.rect.top = wall.rect.bottom
                    self.velocity_y = 0

                elif self.rect.right > wall.rect.left and self.rect.left < wall.rect.left:
                    self.rect.right = wall.rect.left
                    self.player_wall_hit = 1

                elif self.rect.left < wall.rect.right and self.rect.right > wall.rect.right:
                    self.rect.left = wall.rect.right
                    self.player_wall_hit = 1

        if self.rect.colliderect(weapon.rect) and bossalien.died == 1:
              self.weapon_hit = 1

        if self.rect.colliderect(border1.rect):
              self.border_hit = 1
              self.border1 = 1

        if self.border_hit == 1:
            self.border_time += 1
            if self.border_time <= 150:
                font = pygame.font.Font(None,50)
                text = font.render('Alien Base Area 1',True,(240,230,235))
                ekran.blit(text,(249,124))
            else:
                self.border_hit = 0        
            
        if self.rect.colliderect(border2.rect):
              self.border_hit2 = 1
              self.border2 = 1

        if self.border_hit2 == 1:
            self.border_time2 += 1
            if self.border_time2 <= 150:
                font = pygame.font.Font(None,50)
                text = font.render('Alien Base Area 2',True,(240,230,235))
                ekran.blit(text,(249,124))
            else:
                self.border_hit2 = 0      

        if self.rect.colliderect(border3.rect):
              self.border_hit3 = 1
              self.border3 = 1

        if self.rect.colliderect(border4.rect):
            self.border1 = 0
        if self.rect.colliderect(border5.rect):
            self.border2 = 0

        if self.border_hit3 == 1:
            self.border_time3 += 1
            if self.border_time3 <= 150:
                font = pygame.font.Font(None,50)
                text = font.render('Alien Base Area 3',True,(240,230,235))
                ekran.blit(text,(249,124))
            else:
                self.border_hit3 = 0      

        for wallborder in wallborders:
          if self.rect.colliderect(wallborder.rect):
              self.wallborderhit = 1

        if self.wallborderhit == 1:
            if self.rect.colliderect(wall2.rect):
                    if self.velocity_y > 0 and self.rect.bottom > wall2.rect.top and self.rect.top < wall2.rect.top:
                        self.rect.bottom = wall2.rect.top
                        self.on_ground = True
                        self.velocity_y = 0

                    elif self.velocity_y < 0 and self.rect.top < wall2.rect.bottom and self.rect.bottom > wall2.rect.bottom:
                        self.rect.top = wall2.rect.bottom
                        self.velocity_y = 0

                    elif self.rect.right > wall2.rect.left and self.rect.left < wall2.rect.left:
                        self.rect.right = wall2.rect.left
                        self.player_wall_hit = 1

                    elif self.rect.left < wall2.rect.right and self.rect.right > wall2.rect.right:
                        self.rect.left = wall2.rect.right
                        self.player_wall_hit = 1

        for oxygen in oxygens:
          if self.rect.colliderect(oxygen.rect):
              self.oxygen += 60
              oxygens.remove(oxygen)

        if self.oxygen >= self.max_oxygen:
            self.oxygen = self.max_oxygen

        for hpbattery in hpbatterys:
          if self.rect.colliderect(hpbattery.rect):
              self.health += 60
              hpbatterys.remove(hpbattery)

        if self.health >= self.max_health:
            self.health = self.max_health

        for diedw in diedws:
          if self.rect.colliderect(diedw.rect):
              self.died = 1

    def draw_health_bar(self):
      pygame.draw.rect(ekran,(0,0,0),(8,8,204,24))
      pygame.draw.rect(ekran,(255,0,0),(10,10,200,20))
      pygame.draw.rect(ekran,(0,255,0),(10,10,self.health,20))
      pygame.draw.rect(ekran,(0,0,0),(8,38,204,24))
      pygame.draw.rect(ekran,(255,0,0),(10,40,200,20))
      pygame.draw.rect(ekran,(55,191,180),(10,40,self.oxygen,20))
      font = pygame.font.Font(None,18)
      text = font.render('Health',True,(0,0,0))
      ekran.blit(text,(90,14))
      text = font.render('Oxygen',True,(0,0,0))
      ekran.blit(text,(89,44))
      if self.health <= 0:
          self.health = 0
          self.died = 1

    def alien_attack_hit(self):
        for alien in aliens:
           for bullet in alien.bullets:
            if self.rect.colliderect(bullet.rect):
              alien.bullets.remove(bullet)
              self.health -= 5.5
        for alien2 in aliens2:
           for bullet in alien2.bullets:
            if self.rect.colliderect(bullet.rect):
              alien2.bullets.remove(bullet)
              self.health -= 7.5
        for bullet in bossalien.bullets:
          if self.rect.colliderect(bullet.rect):
            bossalien.bullets.remove(bullet)
            self.health -= 9.5

    def draw(self):
        ekran.blit(self.endimage,self.rect)

    def update(self): 
        if self.died_end == 0:
            for bullet in self.bullets:
                bullet.update()
                for wall in walls:
                    if bullet.rect.colliderect(wall.rect):
                        try:
                            self.bullets.remove(bullet)
                        except:
                            print("olmadı")

            self.bullets = [b for b in self.bullets if 0 <= b.rect.x <= width]

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        self.draw()
        if self.died_end == 0:
            self.move()
            self.draw_health_bar()
            self.alien_attack_hit()
            self.wall_hit()        

class Bullet():
    def __init__(self, x, y, direction, color, speed=4):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 10, 4) 
        self.color = color

    def update(self):
        self.draw()
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def draw(self):
        pygame.draw.rect(ekran, self.color, self.rect)

class Wall2():
    def __init__(self, x, y):        
        self.image, self.rect = pygame.image.load('img/wall2.png').subsurface(pygame.Rect(0, 0, 64, 320)) , pygame.Rect(x, y, 64, 320)
    def draw(self):          
        ekran.blit(self.image,self.rect)

width, height = 700, 476

ekran = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")
bg = pygame.image.load('img/bg2.jpg')
bg2 = pygame.image.load('img/bg.png')
time = 0

clock = pygame.time.Clock()

player = Player(x=200,y=90,en=33,boy=53,speed=5)
map = Map(0,0)
map2 = Map2(8000,0)
map3 = Map3(16064,0)
map4 = Map4(24064,0)
wall2 = Wall2(30848,64)
weapon = Weapon(31500,352)
bossalien = BossAlien(31744,200,106,78,3)
skipbutton = Wall(610,440,60,30)
border1 = Wall(12480,128,96,192)
border2 = Wall(20160,128,96,192)
border3 = Wall(27840,128,96,192)
border4 = Wall(16064,128,96,192)
border5 = Wall(24064,128,96,192)
pygame.mixer.music.load("gmusic.mp3") 
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
laser = pygame.mixer.Sound("laser.wav")
jump = pygame.mixer.Sound("jump.wav")
laser.set_volume(0.1)
jump.set_volume(0.1)

def create_walls(wall_map):
    walls = []
    cell_size = 32
    for y, row in enumerate(wall_map):  
        for x, value in enumerate(row):
            if value == 1: 
                wall = Wall(x * cell_size, y * cell_size, cell_size, cell_size)
                walls.append(wall)
    return walls

def create_border(wall_map):
    borders = []
    cell_size = 32
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 3: 
                border = Wall(x * cell_size, y * cell_size, cell_size, cell_size)
                borders.append(border)
    return borders

def create_alien(wall_map):
    aliens = []
    cell_size = 32
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 2: 
                alien = Alien(x * cell_size, y * cell_size+10, 41, 53,3,'alien1')
                aliens.append(alien)
    return aliens

def create_alien2(wall_map):
    aliens2 = []
    cell_size = 32
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 5: 
                alien2 = Alien(x * cell_size, y * cell_size+10, 41, 53,4,'alien2')
                aliens2.append(alien2)
    return aliens2

def create_borderwall(wall_map):
    wallborders = []
    cell_size = 32
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 4: 
                wallborder = Wall(x * cell_size, y * cell_size, cell_size, cell_size)
                wallborders.append(wallborder)
    return wallborders

def create_oxygen(wall_map):
    oxygens = []
    cell_size = 32
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 8: 
                oxygen = Oxygen(x * cell_size, y * cell_size)
                oxygens.append(oxygen)
    return oxygens

def create_battery(wall_map):
    hpbatterys = []
    cell_size = 32
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 9: 
                hpbattery = HpBattery(x * cell_size, y * cell_size)
                hpbatterys.append(hpbattery)
    return hpbatterys

def create_died(wall_map):
    diedws = []
    cell_size = 32
    for y, row in enumerate(wall_map):
        for x, value in enumerate(row):
            if value == 6: 
                diedw = Wall(x * cell_size, y * cell_size,cell_size,cell_size)
                diedws.append(diedw)
    return diedws

sprities = []
sprities_list = []
game_menu = 0
aliens = create_alien(wall_map)
aliens2 = create_alien2(wall_map)
walls = create_walls(wall_map)
borders = create_border(wall_map)
wallborders = create_borderwall(wall_map)
oxygens = create_oxygen(wall_map)
hpbatterys = create_battery(wall_map)
diedws = create_died(wall_map)
sprities.append(map)
sprities.append(bossalien)
sprities.append(map2)
sprities.append(map3)
sprities.append(map4)
sprities.append(wall2)
sprities.append(border1)
sprities.append(border2)
sprities.append(border3)
sprities.append(border4)
sprities.append(border5)
sprities.append(weapon)
sprities_list.append(walls)
sprities_list.append(diedws)
sprities_list.append(oxygens)
sprities_list.append(hpbatterys)
sprities_list.append(borders)
sprities_list.append(wallborders)
sprities_list.append(aliens)
sprities_list.append(aliens2)

def camera():
    if player.player_wall_hit == 0:
        if player.move_direction == "right" and map4.rect.x+8000 > 700:
            for spritie in sprities:
                spritie.rect.x -= player.speed
            for spritiex in sprities_list:
              for spritie in spritiex:
                spritie.rect.x -= player.speed
        if player.move_direction == "left" and map.rect.x != 0:
            for spritie in sprities:
                spritie.rect.x += player.speed
            for spritiex in sprities_list:
              for spritie in spritiex:
                spritie.rect.x += player.speed

def menu(): 
   ekran.blit(bg2,(0,0))
   text = pygame.font.Font(None,38).render("You fell into space due to an accident. But you ", True, (0,0,0))
   text_1 = pygame.font.Font(None,38).render("remembered that the aliens had a teleportation ", True, (0,0,0))
   text_2 = pygame.font.Font(None,38).render("weapon. You must find that weapon. Don't fall into ", True, (0,0,0))
   text_3 = pygame.font.Font(None,38).render("deep pits and be careful with your oxygen.", True, (0,0,0))
   text_4 = pygame.font.Font(None,38).render("Skip", True, (0,0,0))
   ekran.blit(text,(40,120))
   ekran.blit(text_1,(40,160))
   ekran.blit(text_2,(40,200))
   ekran.blit(text_3,(40,240))
   ekran.blit(text_4,(610,440))

def game_over(): 
   ekran.fill((255,212,2))
   text = pygame.font.Font(None,78).render("Game over", True, (255,230,230))
   text_1 = pygame.font.Font(None,78).render("Thanks for playing", True, (255,230,230))
   ekran.blit(text,(210,110))
   ekran.blit(text_1,(110,180))

def draw_growing_ellipse(screen, width, height):
    global time
    center_x = 560
    center_y = 332

    pygame.draw.ellipse(screen, (137,192,73), (center_x, center_y, width, height))

    if width < max_width:
        width += 1
    if height < max_height:
        height += 2
        
    if player.end == 0:
      player.endimage = pygame.image.load('img/player2.png').subsurface(pygame.Rect(0, 0, 44, 57))

    if width >= max_width and height >= max_height:
        time += 1
        player.end = 1
        player.rect.x += 2
        player.animation_time += 1
        if player.animation_time >= 12:
            player.animation_frame = (player.animation_frame + 1) % len(player.right_imgs)
            frame_rect = pygame.Rect(player.right_imgs[player.animation_frame])
            player.endimage = player.images["idle"].subsurface(frame_rect)
            player.animation_time = 0
    if time >= 80:
        game_over()

    return width, height

ellipse_width = 50
ellipse_height = 30
max_width = 80
max_height = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                      
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
              if game_menu == 0:
                if skipbutton.rect.collidepoint(event.pos):
                    game_menu = 1

    ekran.fill((78,149,169))
    if game_menu == 0:
        menu()
    if game_menu == 1:
        ekran.blit(bg,(0,0))
        map.draw()
        map2.draw()
        if map2.rect.x <= 1000:
           map3.draw()
           map4.draw()
        player.update()
        if player.wallborderhit == 1:
          wall2.draw()
        if bossalien.died == 0:
           bossalien.update()
        if bossalien.died == 1 and player.weapon_hit == 0:
            weapon.draw()
        if player.weapon_hit == 1:
            ellipse_width, ellipse_height = draw_growing_ellipse(ekran, ellipse_width, ellipse_height)
        for alien in aliens:
            if alien.rect.x <= 800 and alien.rect.x >= -30:
              alien.update(walls)
        for alien2 in aliens2:
            if alien2.rect.x <= 800 and alien2.rect.x >= -30:
              alien2.update(walls)
        for oxygen in oxygens:
            oxygen.draw()
        for hpbattery in hpbatterys:
            hpbattery.draw()
        if player.died == 0:
          camera()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()