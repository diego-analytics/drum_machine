# Criando uma Drum Machine 1.5

import pygame
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
import boardSupport
import virtual_kit


def play_notes(grid, kit):
    for i in range(kit.num_insts):
        if grid.isClicked(i, grid.current_beat) and grid.isInstActive(i):
            kit.inst[i].play()


def draw_grid(board: boardSupport.drumBoard, kit: virtual_kit.drum_kit, top):
    boxes = []
    top_boxes = []
    active_patterns = []
    grid = board.getDisplayPattern()
    # for grid area and box dimension
    tot_h = HEIGHT - 150 - top
    b_height = int(tot_h / kit.num_insts)
    b_width = int((WIDTH - 200) / grid.beats)
    # left box
    pygame.draw.rect(screen, gray, [0, top, 200, tot_h], 5)

    # bottom menu box
    # and track label boxes
    pygame.draw.rect(screen, gray, [0, top + tot_h, WIDTH, 150], 5)
    for i in range(grid.inst):
        color = dark_gray
        if grid.isInstActive(i):
            color = white
        text = track_font.render(kit.inst[i].name, True, color)
        screen.blit(text, (15, top + b_height // 4 + b_height * i))
        pygame.draw.line(screen, gray, (0, top + (i*b_height) + b_height),
                         (195, top + (i*b_height) + b_height), 3)

    # top grid boxes
    for b in range(board.num_patterns):
        if b == board.current:
            pygame.draw.rect(
                screen, blue, [b * (35 + 10) + 210 - 2, 3, 39, 45], 0, 3)
        color = dark_pink
        act_color = dark_gray
        if b == board.display:
            color = pink
        if board.isActive(b):
            act_color = green
        rect = pygame.draw.rect(screen, color,
                                [b * (35 + 10) + 210, 5, 35, 26], 0, 3)
        act_rect = pygame.draw.rect(screen, act_color,
                                    [b * (35 + 10) + 210, 30, 35, 15], 0, 3)
        top_boxes.append((rect, b))
        active_patterns.append((act_rect, b))

    # grid of boxes
    for b in range(grid.beats):
        for i in range(grid.inst):
            if not grid.isInstActive(i):
                color = dark_gray
                if grid.isClicked(i, b):
                    color = dark_green
            else:
                color = gray
                if grid.isClicked(i, b):
                    color = green

            # button fill
            rect = pygame.draw.rect(screen, color, [b * b_width + 200, top + (i * b_height),
                                                    b_width - b_width // 12, b_height], 0, 3)
            # button outline
            pygame.draw.rect(screen, gold, [b * b_width + 200, top + (i*b_height),
                                            b_width, b_height], 5, 5)
            # button spacing
            pygame.draw.rect(screen, black, [b * b_width + 200, top + (i*b_height),
                                             b_width, b_height], 3, 5)
            boxes.append((rect, (b, i)))

        # highlight box for current beat in blue
        if board.current == board.display:
            pygame.draw.rect(screen, blue,
                             [200 + grid.current_beat * b_width, top, b_width, tot_h - 3], 3, 5)
    return boxes, top_boxes, active_patterns


def save_to_file(grid, name='songBeat.beat'):
    song_file = open(name, 'w')
    meta_data = str(grid.bpm) + ' ' + str(grid.beats) + ' ' + str(grid.inst)
    song_file.write(meta_data + '\n')
    for inst in range(grid.inst):
        for bt in range(grid.beats):
            txt_val = '0'
            if grid.grid[(inst, bt)] == True:
                txt_val = '1'
            song_file.write(txt_val + ' ')
        song_file.write('\n')

    song_file.close()


def load_from_file(name='songBeat.beat', maxBeats=64):
    song_file = open(name, 'r')
    clicked = [[-1 for _ in range(maxBeats)] for _ in range(kit.num_insts)]
    values = song_file.readline().split(' ')
    bpm, beats, insts = int(values[0]), int(values[1]), int(values[2])

    for inst in range(kit.num_insts):
        beatlist = song_file.readline()
        clicked[inst] = [int(val) for val in beatlist.split(' ')[0:-1]]

    song_file.close()
    return (bpm, insts, beats, clicked)


def file_dialog(title):
    '''utilize the pygame GUI file dialog UI window to return filename'''
    clock = pygame.time.Clock()
    win_w, win_h = 500, 400
    manager = pygame_gui.UIManager((win_w, win_h))
    file_selection = UIFileDialog(rect=pygame.Rect(0, 0, win_w, win_h),
                                  manager=manager,
                                  window_title=title,
                                  allow_picking_directories=True)

    selection = ''
    out = False
    while not out:
        tick = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame_gui.UI_WINDOW_CLOSE:
                out = True

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                out = True
                selection = event.text

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == file_selection.cancel_button:
                        out = True

                    if event.ui_element == file_selection.ok_button:
                        selection = file_selection.current_file_path
                        out = True

            manager.process_events(event)

        manager.update(tick)
        manager.draw_ui(screen)
        pygame.display.update()

    return selection


if __name__ == '__main__':

    black, gray, white = (0, 0, 0),  (128, 128, 128), (255, 255, 255)
    dark_gray = (50, 50, 50)
    dark_green, green = (0, 128, 0), (0, 255, 0)
    gold = (212, 175, 55)
    blue = (0, 255, 255)
    dark_pink, pink = (120, 25, 85), (240, 50, 170)

    pygame.init()

    WIDTH, HEIGHT = 1300, 650

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Drummy 1.5')
    label_font = pygame.font.Font('robotomono.ttf', 24)
    medium_font = pygame.font.Font('robotomono.ttf', 22)

    fps = 60
    timer = pygame.time.Clock()

    # load drum kit
    kit = virtual_kit.load_Couch_Kit()
    # kit = virtual_kit.load_YamahaRm50()

    total_patterns = 10
    board = boardSupport.drumBoard()

    # load button grid object
    for i in range(total_patterns):
        board.add_pattern(boardSupport.grid(kit.num_insts, 120, 4))

    board.active[0] = True
    grid = board.pattern[0]

    pygame.mixer.set_num_channels(kit.num_insts * 5)

    # set maximum number beats for the board
    maxBeats = 64

    # adjust font size for track names
    track_font_size = min(int((HEIGHT - 150) / (1.5 * kit.num_insts)), 22)
    track_font = pygame.font.Font('robotomono.ttf', track_font_size)

    # set states
    playing = False
    beat_changed = True
    active_length = 0
    initial_start = True
    save_menu, load_menu = False, False

    KeyinProcess = {key: False for key in boardSupport.bindings.keys()}

    run = True
    while run:
        timer.tick(fps)
        screen.fill(black)

        # Menu inferior (botões)
        play_pause = pygame.draw.rect(
            screen, gray, [7, HEIGHT-140, 185, 100], 0, 5)
        if playing:
            screen.blit(boardSupport.icon['play'],
                        play_pause, (-185 // 4, -5, 100 + 185 // 4, 100))
        else:
            screen.blit(boardSupport.icon['pause'],
                        play_pause, (-185 // 4, -5, 100 + 185 // 4, 100))

        # board buttons

        # Bpm funcionamento e botão
        bpm_rect = pygame.draw.rect(
            screen, gray, [255, HEIGHT - 140, 250, 100], 5, 5)
        screen.blit(boardSupport.icon['metronome'],
                    bpm_rect, (-50, -5, 100 + 50, 100))
        bpm_text2 = label_font.render(f'{grid.bpm}', True, white)
        screen.blit(bpm_text2, (400, HEIGHT - 105))

        bpm_add_rect = pygame.draw.rect(
            screen, gray, [510, HEIGHT - 138, 48, 48], 0, 5)
        bpm_sub_rect = pygame.draw.rect(
            screen, gray, [510, HEIGHT - 88, 48, 48], 0, 5)
        add_text = medium_font.render('+5', True, white)
        sub_text = medium_font.render('-5', True, white)
        screen.blit(add_text, (520, HEIGHT - 130))
        screen.blit(sub_text, (520, HEIGHT - 80))

        # Beats funcionalidades
        beats_rect = pygame.draw.rect(
            screen, gray, [600, HEIGHT - 140, 250, 100], 5, 5)
        screen.blit(boardSupport.icon['loop'],
                    beats_rect, (-80, -30, 200 + 100, 100))
        beats_count = label_font.render(f'{grid.beats}', True, white)
        if beats_count.get_width() > 14:
            screen.blit(beats_count, (713, HEIGHT - 125))
        else:
            screen.blit(beats_count, (720, HEIGHT - 125))
        beats_add_rect = pygame.draw.rect(
            screen, gray, [855, HEIGHT - 138, 48, 48], 0, 5)
        beats_sub_rect = pygame.draw.rect(
            screen, gray, [855, HEIGHT - 88, 48, 48], 0, 5)
        add_text2 = medium_font.render('+1', True, white)
        sub_text2 = medium_font.render('-1', True, white)
        screen.blit(add_text2, (865, HEIGHT - 130))
        screen.blit(sub_text2, (865, HEIGHT - 80))

        # Retangulos dos instrumentos  (Rectangles for instruments)
        top = 50
        b_height = int((HEIGHT - 150 - top) / kit.num_insts)
        instrument_rects = []
        for i in range(kit.num_insts):
            rect = pygame.rect.Rect((0, i * b_height + top), (200, b_height))
            instrument_rects.append(rect)

        # Menu save/load
        save_buttom = pygame.draw.rect(
            screen, gray, [930, HEIGHT - 135, 100, 48], 0, 5)
        screen.blit(boardSupport.icon['save'],
                    save_buttom, (-30, -2, 100 + 30, 50))
        load_buttom = pygame.draw.rect(
            screen, gray, [930, HEIGHT - 85, 100, 48], 0, 5)
        screen.blit(boardSupport.icon['load'],
                    load_buttom, (-30, -2, 100 + 30, 50))

        # Limpar batidas
        clear_buttom = pygame.draw.rect(
            screen, gray, [1050, HEIGHT - 135, 100, 100], 0, 5)
        screen.blit(boardSupport.icon['clear'],
                    clear_buttom, (-5, -5, 100 + 10, 100 + 10))

        ############################

        # handle key press states
        KeyinProcess = boardSupport.keyRelease(KeyinProcess)
        keysPressed = boardSupport.getKeysDown()

        if len(keysPressed) > 0:
            for key in keysPressed:
                name = boardSupport.bindings[key]
                # Esc key - quit progrm
                if name == 'esc' and not KeyinProcess[key]:
                    run = False
                # Spacebar key - toggle play state
                if name == 'space' and not KeyinProcess[key]:
                    KeyinProcess[key] = True
                    playing = not playing
                # up key - increase bpm
                if name == 'up' and not KeyinProcess[key]:
                    KeyinProcess[key] = True
                    grid.inc_bpm()
                    board.setDisplayPattern(grid)
                # down key - decrease bpm
                if name == 'dn' and not KeyinProcess[key]:
                    KeyinProcess[key] = True
                    grid.dec_bpm()
                    board.setDisplayPattern(grid)
                # left key - decrease beat count
                if name == 'left' and not KeyinProcess[key]:
                    KeyinProcess[key] = True
                    grid.dec_beat()
                    board.setDisplayPattern(grid)
                # right key - increase beat count
                if name == 'right' and not KeyinProcess[key]:
                    KeyinProcess[key] = True
                    grid.inc_beat(maxBeats)
                    board.setDisplayPattern(grid)
                # w key - reWind to start
                if name == 'w' and not KeyinProcess[key]:
                    KeyinProcess[key] = True
                    beat_changed = False
                    initial_start = True
                    grid.current_beat = 0
                    active_length = 0

        grid = board.getDisplayPattern()
        boxes, sel_boxes, active_patterns = draw_grid(board, kit, top)

        if save_menu:
            file_name = file_dialog('Save File')
            if file_name != '':
                save_to_file(grid, file_name)
            save_menu = False
        if load_menu:
            file_name = file_dialog('Load File')
            if file_name != '':
                (bpm, insts, beats, clicked) = load_from_file(file_name)
                grid.load(bpm, insts, beats, clicked)
            load_menu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
                # iterate over grid boxes
                for i in range(len(boxes)):
                    if boxes[i][0].collidepoint(event.pos):
                        coords = boxes[i][1]
                        grid.toggle_click(coords[1], coords[0])

                # iterate over pattern selection
                for p in range(len(sel_boxes)):
                    if sel_boxes[p][0].collidepoint(event.pos):
                        board.setDisplayPattern(grid)
                        board.display = p
                        grid = board.getDisplayPattern()

                for p in range(len(sel_boxes)):
                    if active_patterns[p][0].collidepoint(event.pos):
                        board.toggle_active_pattern(p)

            if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
                if play_pause.collidepoint(event.pos):
                    playing = not playing

                elif bpm_add_rect.collidepoint(event.pos):
                    grid.inc_bpm()
                elif bpm_sub_rect.collidepoint(event.pos):
                    grid.dec_bpm()
                elif beats_add_rect.collidepoint(event.pos):
                    grid.inc_beat(maxBeats)
                elif beats_sub_rect.collidepoint(event.pos):
                    grid.dec_beat()
                elif clear_buttom.collidepoint(event.pos):
                    grid.clear()

                elif save_buttom.collidepoint(event.pos):
                    save_menu = True
                elif load_buttom.collidepoint(event.pos):
                    load_menu = True

                for i in range(len(instrument_rects)):
                    if instrument_rects[i].collidepoint(event.pos):
                        grid.toggle_active(i)

                board.setDisplayPattern(grid)

        beat_length = 3600 // board.getCurrentPattern().bpm

        if playing:
            if active_length == 0:
                beat_changed = True
            active_length = (active_length + 1) % beat_length

        if playing and beat_changed:
            beat_changed = False
            if initial_start:
                initial_start = False
                play_notes(board.getCurrentPattern(), kit)
            else:
                go_to_next_pattern = board.getCurrentPattern().tick_current_beat()
                if go_to_next_pattern:
                    board.inc_current_pattern()
                play_notes(board.getCurrentPattern(), kit)

        pygame.display.flip()

    pygame.quit()
