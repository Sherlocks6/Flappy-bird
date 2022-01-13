
import random
import pip
import pygame
import sys






#Zeichnet den Hintergrund des Spiels
def draw_bg():
    screen.blit(bg_surface,(0, 0))

#Zeichnet den Boden
def draw_floor():
    screen.blit(floor_surface,(floor_x_postion, 900))
    screen.blit(floor_surface,(floor_x_postion + WIDTH, 900))


#Erschafft die pipes
def create_pipe():
    #Kreiert ein der drei mögichen höhen für die pipe
    random_pipe_pos = random.choice(pipe_height)
    #Erschafft ein Viereck um die Zufällige höhe wo dann ein bild gemalt werden kann
    bottom_pipe = pipe_surface.get_rect(midtop =(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom =(700, random_pipe_pos - 300))
    #gibt die Ergebnisse aus
    return bottom_pipe, top_pipe

#Verschiebt die Piped
def move_pipes(pipes):
    for pipe in pipes:
        #verschiebt das Zentrum um -5 auf der x achse
        pipe.centerx -=5
    return pipes


#Zeichnet die Pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            #Dreht die Pipes um um einen Tunnel zu schaffen
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)


#Rotiert den Vogel
def rotate_bird(bird):
    #rotozoom = Rotieren und vergößern
    new_bird = pygame.transform.rotozoom(bird, -bird_movment * 3,1)
    return new_bird


#animiert den Vogel
def bird_animation():
    #Liste wo die 3 Frames drin sind
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center =(100, bird_rect.centery))
    return new_bird, new_bird_rect


#checkt die berührungen des Vogels mit anderen Oberflächen
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print("Kollision")
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >=900:
        print("collision")
        death_sound.play()
        return False
    
    return True


#displayed den Punktestand (wenn normales game dann nur score)
#wenn game over dann auch highscore
def score_display(game_state):
    

    #normaler score
    if game_state == "main_game":
        score_surface = game_font.render(f"Score: {int(score)}",True,(white))#f-string um in dem String code schreiben zu können# 
        score_rect = score_surface.get_rect(center= (288, 100))
        screen.blit(score_surface,score_rect)

    if game_state == "game_over":
        #highscore
        global high_score #global um auf einen Wert auserhalb einer funktion zuzugreifen und ihn zu verändern
        high_score_surface = game_font.render(f"High Score: {int(high_score)}",True,(white)) #f-string um in dem String code schreiben zu können# 
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

        score_surface = game_font.render(f"Score: {int(score)}",True,(white)) #f-string um in dem String code schreiben zu können# 
        score_rect = score_surface.get_rect(center= (288, 100))
        screen.blit(score_surface,score_rect)


#Updated den score immer wenn der Timer abgelaufen ist(loop)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score






#
#Variablen
#
WIDTH, HEIGHT = 576, 1024
#Zeigt Spielzustand an
game_active = True
#Gravitation
gravity = 0.5
#joa selbsterklärend
high_score = 0
#Vogel Geschwindigkeit
bird_movment = 0
#Score
score = 0
#Score countdown zum genauen Gräusch
score_sound_countdown = 100


#Farben
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)








#Erschafft ein fenster Welches die Größe von WIDTH und HEIGTH hat
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#Überschrift gestalten
pygame.display.set_caption("Flappy Bird")
#lässt mich audios benutzen
pygame.mixer.init()
#lässt mich pygame benutzen (i guess)
pygame.init()
#ist die refresh rate des Bildes
clock = pygame.time.Clock()


#Schrftart einfügen
game_font = pygame.font.Font("04B_19.ttf",40)



#Bilder

#Bild vom vogel frame 1
bird_downflap = pygame.image.load("assets//bluebird-downflap.png")
#Vergrößert das bild um den Faktor 2
bird_downflap = pygame.transform.scale2x(bird_downflap)

#Frame 2
bird_midflap = pygame.image.load("assets//bluebird-midflap.png")
#Vergrößert das bild um den Faktor 2
bird_midflap = pygame.transform.scale2x(bird_midflap)

#Frame 3
bird_upflap = pygame.image.load("assets//bluebird-upflap.png")
#Vergrößert das bild um den Faktor 2
bird_upflap = pygame.transform.scale2x(bird_upflap)

#Alle Frames (Bilder) in einer Liste
bird_frames = [bird_downflap,bird_midflap,bird_upflap]

#Gibt die Zahl für die untrige Liste an
bird_index = 0

#Das erste Bild in Der Liste ist der Surface für den Vogel
bird_surface = bird_frames[bird_index]

#erschafft ein Viereck um  das Hauptvogelbild welches man kontrollieren kann
bird_rect = bird_surface.get_rect(center = (100, 512))

#Userevent für den Vogel(sagt dass etwas mit dem Vogel passiert)
BIRDFLAP = pygame.USEREVENT + 1
#Ich verstehe die Zeile Nicht(Funktioniertr aber)
pygame.time.set_timer(BIRDFLAP,200)




#Bilder vom Boden
floor_surface = pygame.image.load("assets//base.png")
#Vergrößert das bild um den Faktor 2
floor_surface = pygame.transform.scale2x(floor_surface)

#Zeigt die x Koordinate des Boden
floor_x_postion = 0



#Bilder vom Hintergrund
bg_surface = pygame.image.load("assets//background-night.png")
#Vergrößert das bild um den Faktor 2
bg_surface = pygame.transform.scale2x(bg_surface)



#Bild der Pipes
pipe_surface = pygame.image.load("assets//pipe-green.png")
#Vergrößert das bild um den Faktor 2
pipe_surface = pygame.transform.scale2x(pipe_surface)

#Liste mit den pipes die gemacht werden sollen
pipe_list = []
#Userevent für die Pipes wenn sie erscheinen
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
#höhe der pipes
pipe_height = [400, 600, 800]



#
#gameover Bilder zum anzeigen
#
#Zeigt welches Bild verwendet werden soll
game_over_surface = pygame.image.load("assets//message.png")
#Vergrößert das bild um den Faktor 2
game_over_surface = pygame.transform.scale2x(game_over_surface)
#Schafft ein Viereck um das Bild und zeigt wo es liegt
game_over_rect = game_over_surface.get_rect(center =(288,512))




#Geräusche einbauen

#kannste dir ja denken OMEGALUL
flap_sound = pygame.mixer.Sound("sound//sfx_wing.wav")

death_sound = pygame.mixer.Sound("sound//sfx_die.wav")

score_sound = pygame.mixer.Sound("sound//sfx_point.wav")





run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movment = 0
                bird_movment -=12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movment = 0
                score = 0



        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            #print(pipe_list)

        #Wechselt durch die verschiedenen Bilder des Vogels
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            

            bird_surface, bird_rect = bird_animation()

        
        





    #Zeichnet den Hintergrund
    draw_bg()





    #läuft immer durch
    if game_active is True:

        #regelt geschwindigkeit und gravitation des Vogels
        bird_movment += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movment
        screen.blit(rotated_bird, bird_rect)


        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #bewegt den Boden im main_game
        floor_x_postion -=1
        draw_floor()
        if floor_x_postion <= -576:
            floor_x_postion = 0


        #Punkte anzeigen
        
        score += 0.01
        score_display("main_game")


        #Punkte Sound
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100


    else:
        score_sound_countdown = 100
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")
    

        #bewegt den Boden auch wenn das Spiel nicht läuft
        floor_x_postion -=1
        draw_floor()
        #setzt den Boden zurück
        if floor_x_postion <= -576:
            floor_x_postion = 0









    #updatet bei jedem Loop den screen
    pygame.display.update()
    #updated so oft wies in der Klammer steht
    clock.tick(60)
















