# Criando uma Drum Machine 1.0

import pygame
from pygame import mixer
pygame.init()

WIDTH = 1300
HEIGHT = 650

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
dark_gray = (50, 50, 50)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Drummy 1.0')
label_font = pygame.font.Font('robotomono.ttf', 28)
medium_font = pygame.font.Font('robotomono.ttf', 22)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open('salvos.txt', 'r')
for line in file:
    saved_beats.append(line)

# carregando os sons
hihat = mixer.Sound('sounds/hihat.wav')
snare = mixer.Sound('sounds/snare.wav')
crash = mixer.Sound('sounds/crash.wav')
clap = mixer.Sound('sounds/clap.WAV')
kick = mixer.Sound('sounds/kick.wav')
tom = mixer.Sound('sounds//tom.wav')
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hihat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 150, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi-hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (20, 30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (20, 110))
    kick_text = label_font.render('Kick', True, colors[actives[2]])
    screen.blit(kick_text, (20, 190))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (20, 270))
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (20, 350))
    floor_tom_text = label_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_tom_text, (20, 430))
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i*83) + 83), (195, (i*83) + 83), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH-260) // beats) + 200, (j*82) + 5,
                                                   ((WIDTH-200) // beats) - 10, ((HEIGHT-126)//instruments) - 10], 0, 3)
            pygame.draw.rect(screen, gold, [i * ((WIDTH-260) // beats) + 200, (j*82),
                                                   ((WIDTH-200) // beats), ((HEIGHT-126)//instruments)], 5, 5)
            pygame.draw.rect(screen, black, [i * ((WIDTH-260) // beats) + 200, (j*82),
                                                   ((WIDTH-200) // beats), ((HEIGHT-126)//instruments)], 3, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH-260) // beats) + 200, 0, ((WIDTH - 200)//beats), instruments * 82], 3, 5)
    return boxes

def draw_save_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('SAVE MENU: Digite um nome para o arquivo', True, white)
    screen.blit(menu_text, (330, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 170, HEIGHT - 100, 110, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH-160, HEIGHT-75))
    return exit_btn


def draw_load_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 170, HEIGHT - 100, 110, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 75))
    return exit_btn


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat, active_list)
    # Menu inferior (botões)
    play_pause = pygame.draw.rect(screen, gray, [7, HEIGHT-140, 185, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (15, HEIGHT - 120))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (20, HEIGHT - 80))
    # Bpm funcionamento e botão
    bpm_rect = pygame.draw.rect(screen, gray, [255, HEIGHT - 140, 250, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (278, HEIGHT-120))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (350, HEIGHT - 90))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 138, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 88, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, white)
    sub_text = medium_font.render('-5', True, white)
    screen.blit(add_text, (520, HEIGHT - 130))
    screen.blit(sub_text, (520, HEIGHT - 80))
    # Beats funcionalidades
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 140, 250, 100], 5, 5)
    beats_text = medium_font.render('Beats in Loop', True, white)
    screen.blit(beats_text, (638, HEIGHT - 120))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (720, HEIGHT - 90))
    beats_add_rect = pygame.draw.rect(screen, gray, [855, HEIGHT - 138, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [855, HEIGHT - 88, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    sub_text2 = medium_font.render('-1', True, white)
    screen.blit(add_text2, (865, HEIGHT - 130))
    screen.blit(sub_text2, (865, HEIGHT - 80))
    # Retangulos dos instrumentos
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 83), (200, 83))
        instrument_rects.append(rect)
    # Menu save/load
    save_buttom = pygame.draw.rect(screen, gray, [930, HEIGHT - 135, 100, 48], 0, 5)
    save_text = label_font.render('Save', True, white)
    screen.blit(save_text, (945, HEIGHT - 130))
    load_buttom = pygame.draw.rect(screen, gray, [930, HEIGHT - 85, 100, 48], 0, 5)
    load_text = label_font.render('Load', True, white)
    screen.blit(load_text, (945, HEIGHT - 80))

    # Limpar batidas
    clear_buttom = pygame.draw.rect(screen, gray, [1050, HEIGHT - 135, 100, 100], 0, 5)
    clear_text = label_font.render('Clear', True, white)
    screen.blit(clear_text, (1057, HEIGHT - 110))
    if save_menu:
        exit_buttom = draw_save_menu()
    if load_menu:
        exit_buttom = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_buttom.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_buttom.collidepoint(event.pos):
                save_menu = True
            elif load_buttom.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_buttom.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats -1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
