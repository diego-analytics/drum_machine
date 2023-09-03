##
# Supporting classes to handle:
#   - virtual instrument sample
#   - drum kit class for providing a framework to handle all the instruments
#   - grid to store state of sample grid.
##

from pygame import mixer
import random
import glob


def get_files(path):
    return glob.glob(path + '\\*.wav')


class instrument():
    '''instrument class:
         contains name and audio sample varients
         method: play -> play random varient
    '''

    def __init__(self, name: str, audiofiles: list):
        self.name = name
        self.audio = [mixer.Sound(file) for file in audiofiles]
        self.varients = len(self.audio)

    def play(self):
        if self.varients == 1:
            self.audio[0].play()
        else:
            choice = random.choice(self.audio)
            choice.play()


class drum_kit():
    ''' the drum_kit class uses a dictionary to store vitrual instruments
        The dictionary key increments up as instruemtns are added.
        The order of adding instruments will be the final track listing
        in the GUI.
    '''

    def __init__(self):
        self.inst = dict()
        self.num_insts = len(self.inst)

    def add_instrument(self, name: str, files: list):
        self.inst.update({self.num_insts: instrument(name, files)})
        self.num_insts = len(self.inst)


def load_YamahaRm50():
    kit = drum_kit()
    kit.add_instrument(
        'Closed Hi-Hat', get_files('YamahaRM50/Hi-Hat/Closed-Hi-Hat'))
    kit.add_instrument(
        'Open Hi-Hat', get_files('YamahaRM50/Hi-Hat/Open-Hi-Hat'))
    kit.add_instrument('Kick', get_files('YamahaRM50/Kick/Rock-Kick'))
    kit.add_instrument('Snare', get_files('YamahaRM50/Snare/Snare-Drum'))
    kit.add_instrument('Side-Stick', get_files('YamahaRM50/Side-Stick'))
    kit.add_instrument('Hi-Tom', get_files('YamahaRM50/Toms/High-Tom'))
    kit.add_instrument('Mid-Tom', get_files('YamahaRM50/Toms/Mid-Tom'))
    kit.add_instrument('Low-Tom', get_files('YamahaRM50/Toms/Low-Tom'))
    kit.add_instrument('Splash', get_files('YamahaRM50/Splash'))
    kit.add_instrument('Ride', get_files('YamahaRM50/Ride'))
    kit.add_instrument(
        'Tamborine', ['YamahaRM50/Percussion/Yamaha-RM50-Tambourine.wav'])

    return kit


def load_Couch_Kit():
    kit = drum_kit()
    path = 'COUCH-KIT/02 ONE SHOTS/'
    closedHH = [path + 'HiHat/CKV1_HH Closed Loud.wav',
                path + 'HiHat/CKV1_HH Closed Medium.wav']
    openHH = [path + 'HiHat/CKV1_HH Open Loud.wav',
              path + 'HiHat/CKV1_HH Open Medium.wav']
    crossStick = [path + 'Cross Stick/CKV1_Cross Stick 1.wav']
    kit.add_instrument('Closed Hi-Hat', closedHH)
    kit.add_instrument('Open Hi-Hat', openHH)
    kit.add_instrument('Kick', [path + 'Kick/CKV1_Kick Loud.wav'])
    kit.add_instrument('Snare', get_files(path + 'Snare'))
    kit.add_instrument('Cross Stick', crossStick)
    kit.add_instrument('Rim Click', get_files(path + 'Rim Click'))

    return kit
