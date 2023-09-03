##
# functions to handle keypress during pygame loop
##

import pygame


class grid():
    '''grid object to store atate of box grid and instrument active state

       instances:
         bpm:  beats / min
         inst: number of instruments to track
         beats: number of beats in a loop
         current beat: which beat is active
         grid: state of button board
         active: State of track that are muted or not
    '''

    def __init__(self, num_insts, bpm, beats):
        self.bpm = bpm
        self.inst = num_insts
        self.beats = beats
        self.current_beat = 0
        self.grid = {(i, b): False for i in range(self.inst)
                     for b in range(self.beats)}
        self.active = {i: True for i in range(self.inst)}

    def toggle_click(self, inst_num, beat):
        '''toggle if instruemt on beat is ON/OFF'''
        self.grid[(inst_num, beat)] = not self.grid[(inst_num, beat)]

    def toggle_active(self, inst):
        '''toggle is track is acive state is ON/OFF'''
        self.active[inst] = not self.active[inst]

    def inc_beat(self, maxBeats):
        '''increment beat in loop'''
        self.grid.update({(i, self.beats): False for i in range(self.inst)})
        self.beats = min(self.beats + 1, maxBeats)

    def dec_beat(self):
        '''decrement beat in loop'''
        if self.beats > 1:
            for i in range(self.inst):
                self.grid.pop((i, self.beats - 1))
            self.beats -= 1

        self.current_beat = max(self.current_beat - 1, 1)

    def inc_bpm(self):
        '''increment beat in loop'''
        self.bpm += 5

    def dec_bpm(self):
        '''decrement beat in loop'''
        self.bpm = max(self.bpm - 5, 5)

    def isClicked(self, inst_num, beat):
        '''check if grid value state is ON/OFF'''
        if (inst_num, beat) in self.grid.keys():
            return self.grid[(inst_num, beat)]
        return False

    def isInstActive(self, inst):
        '''check acive state of track'''
        return self.active[inst]

    def tick_current_beat(self):
        '''cyclicly increment current beat'''
        self.current_beat = (self.current_beat + 1) % self.beats

    def clear(self):
        '''clear board'''
        self.grid = {(i, b): False for i in range(self.inst)
                     for b in range(self.beats)}
        self.active = {i: True for i in range(self.inst)}

    def load(self, bpm, insts, beats, clicked):
        '''load board state'''
        self.bpm = bpm
        insts = min(self.inst, insts)
        self.beats = beats

        self.grid = {(i, b): False for i in range(self.inst)
                     for b in range(self.beats)}
        for i in range(insts):
            for b in range(self.beats):
                if clicked[i][b] == 1:
                    self.grid[(i, b)] = True
                else:
                    self.grid[(i, b)] = False

    def print_grid(self):
        '''print board state to terminal (for diagnostics)'''
        for i in range(self.inst):
            for b in range(self.beats):
                if self.grid[(i, b)]:
                    print('I ', end='')
                else:
                    print('_ ', end='')
                print()


# key bindings to constrict what keys will be searched for
# and gives integer key-codes a name
bindings = {pygame.K_SPACE: 'space', pygame.K_ESCAPE: 'esc',
            pygame.K_UP: 'up', pygame.K_DOWN: 'dn',
            pygame.K_RIGHT: 'right', pygame.K_LEFT: 'left',
            pygame.K_w: 'w'}


def getKeysDown():
    '''returns set of keys currently being pressed down'''
    key = pygame.key.get_pressed()
    pressingKeys = set()
    for ind in bindings.keys():
        if key[ind]:
            pressingKeys.add(ind)

    return pressingKeys


def keyRelease(pressedKeys):
    '''Check if pressed key is released'''
    keys = pygame.key.get_pressed()
    for key in pressedKeys.keys():
        if pressedKeys[key] and not keys[key]:
            pressedKeys[key] = False

    return pressedKeys
