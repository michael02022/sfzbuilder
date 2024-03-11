import PySimpleGUI as sg
import re
import json
import os
import glob
from pprint import pprint
from collections import defaultdict
import pathlib

filter_type = ("lpf_1p", "hpf_1p", "lpf_2p", "hpf_2p", "bpf_2p", "brf_2p")
off_modes = ("fast", "normal")
loop_modes = ("None", "no_loop", "one_shot", "loop_continuous", "loop_sustain")
loop_directions = ("None", "forward", "reverse")
trigger_modes = ("attack", "release", "first", "legato", "release_key")
LINEAR_CURVE = 0.0000001
DECAY_CURVE = -10.3616

# Global
class Global:
    def __init__(self):
        self.keysw_range = [24, 36]
        self.sw_default = 24
    
    def update(self, values):
        self.keysw_range[0] = values["-sw_lokey-"]
        self.keysw_range[1] = values["-sw_hikey-"]
        self.sw_default = values["-sw_default-"]

class Mapping:
    def __init__(self, type):
        self.type = type
        self.pack = ""
        self.map = ""
        self.name = ""
        # MAP PROPERTIES
        self.map_key_range = [0, 127]
        self.map_vel_range = [0, 127]
        #self.map_chan_range = [1, 1]
        #self.map_prog_range = [0, 0]
        self.on_cc_rangebool = False
        self.on_cc_range = [64, 0, 127] # CC value, on_locc, on_hicc (CC64 is default because sustain pedal)
        self.random_rangebool = False
        self.random_range = [0, 1] # lorand / hirand
        #self.chanaft_range = [0, 127]
        #self.polyaft_range = [0, 127]

        self.bend_range = [-98304, 98304] # two octaves

        self.volume = 0

        self.keyswitchbool = False
        self.keyswitch = 24
        self.sw_label = ""

        self.output = 0

        self.polybool = False
        self.poly = 16
        self.note_polybool = False
        self.note_poly = 16
        self.note_selfmask = False

        self.trigger = trigger_modes[0]
        self.rt_dead = False
        self.rt_decaybool = False
        self.rt_decay = 0

        # (PERC RELATED)
        self.key_opcode = False # enable/disable key= opcode if the user want to use one note for each percussion
        self.keycenterbool = False
        self.keycenter = 60 # pitch_keycenter

        # SAMPLE PROPERTIES
        self.offsetbool = False
        self.offset = 0
        self.offset_random = 0
        self.delay = 0

        self.note_offset = 0
        self.pitch_transpose = 0

        self.quality = 2

        self.loop_mode = loop_modes[0]
        self.direction = loop_directions[0]

        # (PERC RELATED)
        self.vel2offset = 0 # offset_cc131

        # (EXCLUSIVE CLASS)
        self.exclass = False
        self.group = 0
        self.off_by = 0
        self.off_mode = off_modes[0]
        self.off_time = 0.006

        # PAN PROPERTIES
        self.panbool = False
        self.pan_value = 0
        self.pan_keycenter = 60
        self.pan_keytrack = 0
        self.pan_veltrack = 0
        self.pan_random = 0

        # AMP PROPERTIES
        self.amp_keycenter = 60
        self.amp_keytrack = 0
        self.amp_veltrack = 100
        self.amp_random = 0
        # (PERC RELATED)
        self.amp_velfloorbool = False
        self.amp_velfloor = 0 # amp_velcurve_1
        self.amp_env_vel2attackbool = False
        self.amp_env_vel2attack = 0 # ampeg_vel2attack

        # AMP ENVELOPE
        self.amp_env = False
        self.amp_env_delay = 0
        self.amp_env_attack = 0
        self.amp_env_attack_shapebool = False
        self.amp_env_attack_shape = LINEAR_CURVE
        self.amp_env_hold = 0
        self.amp_env_sustain = 100
        self.amp_env_decay = 0
        self.amp_env_decay_shapebool = False
        self.amp_env_decay_shape = 1.04
        self.amp_env_release = 0
        self.amp_env_release_shapebool = False
        self.amp_env_release_shape = 1.04
        # AMP LFO
        self.amp_lfo = False
        self.amp_lfo_delay = 0
        self.amp_lfo_fade = 0
        self.amp_lfo_depth = 0
        self.amp_lfo_freq = 15

        # FILTER PROPERTIES
        self.fil = False
        self.fil_type = filter_type[0]
        self.fil_veltrack = 0
        self.fil_keytrack = 0
        self.fil_keycenter = 60
        self.fil_random = 0
        self.cutoff = 11970
        self.resonance = 0
        # FILTER ENVELOPE
        self.fil_env = False
        self.fil_env_depth = 0
        self.fil_vel2depth = 0
        self.fil_env_delay = 0
        self.fil_env_attack = 0
        self.fil_env_hold = 0
        self.fil_env_sustain = 100
        self.fil_env_decay = 0
        self.fil_env_release = 0
        # FILTER LFO
        self.fil_lfo = False
        self.fil_lfo_delay = 0
        self.fil_lfo_fade = 0
        self.fil_lfo_depth = 0
        self.fil_lfo_freq = 15

        # PITCH PROPERTIES
        self.pitch = False
        self.pitch_veltrack = 0
        self.pitch_keytrack = 100
        self.pitch_random = 0
        # PITCH ENVELOPE
        self.pit_env = False
        self.pit_env_depth = 0
        self.pit_env_delay = 0
        self.pit_env_attack = 0
        self.pit_env_hold = 0
        self.pit_env_sustain = 100
        self.pit_env_decay = 0
        self.pit_env_release = 0
        # PITCH LFO
        self.pit_lfo = False
        self.pit_lfo_delay = 0
        self.pit_lfo_fade = 0
        self.pit_lfo_depth = 0
        self.pit_lfo_freq = 15

        # MISC
        self.opcode_notepad = ""

    def get_name(self):
        match self.type:
            case "MSamples":
                return f"M: {self.name}"
            case "PSamples":
                return f"P({self.keycenter[1]}): {self.name}"
    
    def set_map(self, pack, map):
        self.pack = pack
        self.map = map
        self.name = pathlib.Path(self.map).stem
    
    def change_type(self, type):
        self.type = type

    def update(self, values):
        self.map_key_range[0] = values['-MAINMAP_LOKEY-']
        self.map_key_range[1] = values['-MAINMAP_HIKEY-']
        self.map_vel_range[0] = values['-MAINMAP_LOVEL-']
        self.map_vel_range[1] = values['-MAINMAP_HIVEL-']
        self.on_cc_rangebool = values["-randBOOL-"]
        self.on_cc_range[0] = values['-on_ccNUMBER-']
        self.on_cc_range[1] = values['-on_locc-']
        self.on_cc_range[2] = values['-on_hicc']
        self.random_rangebool = values['-randBOOL-']
        self.random_range[0] = values['-lorand-']
        self.random_range[1] = values['-hirand-']
        self.volume = values['-volume-']
        self.output = values['-output-']
        self.polybool = values["-polyphonyBOOL-"]
        self.poly = values['-polyphony-']
        self.note_polybool = values['-note_polyphonyBOOL-']
        self.note_poly = values['-note_polyphony-']
        self.note_selfmask = values['-note_selfmaskBOOL-']
        self.trigger = values['-trigger_mode-']
        self.rt_dead = values['-rt_dead-']
        self.rt_decaybool = values["-rt_decayBOOL-"]
        self.rt_decay = values['-rt_decay-']
        self.keyswitchbool = values["-keyswitch_mapBOOL-"]
        self.keyswitch = values['-keyswitch_map-']
        self.sw_label = values['-keyswitch_label-']
        self.key_opcode = values['-keyopcodeBOOL-']
        self.keycenterbool = values["-pitch_keycenterBOOL-"]
        self.keycenter = values['-pitch_keycenter-']
        self.offsetbool = values["-offsetBOOL-"]
        self.offset = values['-offset-']
        self.offset_random = values['-random_offset-']
        self.vel2offset = values['-vel2offset-']
        self.delay = values['-sample_delay-']
        self.pitch_transpose = values['-pitch_transpose-']
        self.note_offset = values['-note_transpose-']
        self.quality = values['-sample_quality-']
        self.loop_mode = values['-loop_mode-']
        self.direction = values['-direction-']
        self.exclass = values["-exclassBOOL-"]
        self.group = values['-exclass_group-']
        self.off_by = values['-exclass_offby-']
        self.off_mode = values['-exclass_offmode-']
        self.off_time = values['-exclass_offtime-']
        self.panbool = values['-panBOOL-']
        self.pan_value = values['-pan-']
        self.pan_keycenter = values['-pan_keycenter-']
        self.pan_keytrack = values['-pan_keytrack-']
        self.pan_veltrack = values['-pan_veltrack-']
        self.pan_random = values['-pan_random-'] 
        self.amp_keycenter = values['-amp_keycenter-'] 
        self.amp_keytrack  = values['-amp_keytrack-']
        self.amp_veltrack = values['-amp_veltrack-']
        self.amp_random = values['-amp_random-']
        self.amp_lfo = values["-amp_lfoBOOL-"]
        self.amp_lfo_delay = values['-amp_lfo_delay-'] 
        self.amp_lfo_fade = values['-amp_lfo_fade-']
        self.amp_lfo_depth = values['-amp_lfo_depth-']
        self.amp_lfo_freq = values['-amp_lfo_freq-']
        self.amp_velfloorbool = values["-amp_velcurve_1BOOL-"]
        self.amp_velfloor = values['-amp_velcurve_1-']
        self.amp_lfo = values["-amp_lfoBOOL-"]
        self.amp_env_vel2attackbool = values["-vel2attackBOOL-"]
        self.amp_env_vel2attack = values['-vel2attack-']
        self.amp_env = values["-amp_envBOOL-"]
        self.amp_env_delay = values['-amp_env_delay-']
        self.amp_env_attack = values['-amp_env_attack-']
        self.amp_env_attack_shapebool = values['-attack_shapeBOOL-']
        self.amp_env_attack_shape = values['-attack_shape-']
        self.amp_env_hold = values['-amp_env_hold-'] 
        self.amp_env_sustain = values['-amp_env_sustain-']
        self.amp_env_decay = values['-amp_env_decay-']
        self.amp_env_decay_shapebool = values['-decay_shapeBOOL-']
        self.amp_env_decay_shape = values['-decay_shape-']
        self.amp_env_release = values['-amp_env_release-']
        self.amp_env_release_shapebool = values['-release_shapeBOOL-']
        self.amp_env_release_shape = values['-release_shape-']
        self.fil = values['-filterBOOL-']
        self.fil_type = values['-filter_type-']
        self.cutoff = values['-cutoff-']
        self.resonance = values['-resonance-']
        self.fil_keycenter = values['-fil_keycenter-']
        self.fil_keytrack = values['-fil_keytrack-']
        self.fil_veltrack = values['-fil_veltrack-']
        self.fil_random = values['-fil_random-']
        self.fil_lfo = values["-fil_lfoBOOL-"]
        self.fil_lfo_delay = values['-fil_lfo_delay-']
        self.fil_lfo_fade = values['-fil_lfo_fade-']
        self.fil_lfo_depth = values['-fil_lfo_depth-']
        self.fil_lfo_freq = values['-fil_lfo_freq-']
        self.fil_env_depth = values['-fil_env_depth-']
        self.fil_vel2depth = values['-vel2depth-']
        self.fil_env = values["-fil_envBOOL-"]
        self.fil_env_delay = values['-fil_env_delay-']
        self.fil_env_attack = values['-fil_env_attack-']
        self.fil_env_hold = values['-fil_env_hold-']
        self.fil_env_sustain = values['-fil_env_sustain-']
        self.fil_env_decay = values['-fil_env_decay-']
        self.fil_env_release = values['-fil_env_release-']
        self.pitch = values['-pitchBOOL-']
        self.pitch_keytrack = values['-pitch_keytrack-']
        self.pitch_veltrack = values['-pitch_veltrack-'] 
        self.pitch_random = values['-pitch_random-']
        self.pit_lfo = values['-pit_lfoBOOL-']
        self.pit_lfo_delay = values['-pit_lfo_delay-']
        self.pit_lfo_fade = values['-pit_lfo_fade-']
        self.pit_lfo_depth = ['-pit_lfo_depth-']
        self.pit_lfo_freq = values['-pit_lfo_freq-']
        self.pit_env = values['-pit_envBOOL-'] 
        self.pit_env_depth = values['-pit_env_depth-'] 
        self.pit_env_delay = values['-pit_env_delay-'] 
        self.pit_env_attack = values['-pit_env_attack-'] 
        self.pit_env_hold = values['-pit_env_hold-']
        self.pit_env_sustain = values['-pit_env_sustain-'] 
        self.pit_env_decay = values['-pit_env_decay-']
        self.pit_env_release = values['-pit_env_release-']
        self.opcode_notepad = values['-opcode_notepad-']
    
    def get_default_path(self):
        p = os.path.dirname(self.map)
        path = f"{self.pack}\\{p}\\"
        return path.replace('\\', '/')
    
    def get_include_path(self):
        path = f"{self.pack}\\{self.map}"
        return path.replace('\\', '/')

def get_map_values(window, values, obj):
    window.Element('-MAINMAP_LOKEY-').update(value=obj.map_key_range[0])
    window.Element('-MAINMAP_HIKEY-').update(value=obj.map_key_range[1])
    window.Element('-MAINMAP_LOVEL-').update(value=obj.map_vel_range[0])
    window.Element('-MAINMAP_HIVEL-').update(value=obj.map_vel_range[1])
    window.Element('-on_ccBOOL-').update(value=obj.on_cc_rangebool)
    window.Element('-on_ccNUMBER-').update(value=obj.on_cc_range[0])
    window.Element('-on_locc-').update(value=obj.on_cc_range[1])
    window.Element('-on_hicc').update(value=obj.on_cc_range[2])
    window.Element('-randBOOL-').update(value=obj.random_rangebool)
    window.Element('-lorand-').update(value=obj.random_range[0])
    window.Element('-hirand-').update(value=obj.random_range[1])
    window.Element('-volume-').update(value=obj.volume)
    window.Element('-output-').update(value=obj.output)
    window.Element('-polyphonyBOOL-').update(value=obj.polybool)
    window.Element('-polyphony-').update(value=obj.poly)
    window.Element('-note_polyphonyBOOL-').update(value=obj.note_polybool)
    window.Element('-note_polyphony-').update(value=obj.note_poly)
    window.Element('-note_selfmaskBOOL-').update(value=obj.note_selfmask)
    window.Element('-trigger_mode-').update(set_to_index=trigger_modes.index(obj.trigger))
    window.Element('-rt_dead-').update(value=obj.rt_dead)
    window.Element('-rt_decayBOOL-').update(value=obj.rt_decaybool)
    window.Element('-rt_decay-').update(value=obj.rt_decay)
    window.Element('-keyswitch_mapBOOL-').update(value=obj.keyswitchbool)
    window.Element('-keyswitch_map-').update(value=obj.keyswitch)
    window.Element('-keyswitch_label-').update(value=obj.sw_label)
    window.Element('-keyopcodeBOOL-').update(value=obj.key_opcode)
    window.Element('-pitch_keycenterBOOL-').update(value=obj.keycenterbool)
    window.Element('-pitch_keycenter-').update(value=obj.keycenter)
    window.Element('-offsetBOOL-').update(value=obj.offsetbool)
    window.Element('-offset-').update(value=obj.offset)
    window.Element('-random_offset-').update(value=obj.offset_random)
    window.Element('-vel2offset-').update(value=obj.vel2offset)
    window.Element('-sample_delay-').update(value=obj.delay)
    window.Element('-pitch_transpose-').update(value=obj.pitch_transpose)
    window.Element('-note_transpose-').update(value=obj.note_offset)
    window.Element('-sample_quality-').update(value=obj.quality)
    window.Element('-loop_mode-').update(set_to_index=loop_modes.index(obj.loop_mode))
    window.Element('-direction-').update(set_to_index=loop_directions.index(obj.direction))
    window.Element('-exclassBOOL-').update(value=obj.exclass)
    window.Element('-exclass_group-').update(value=obj.group)
    window.Element('-exclass_offby-').update(value=obj.off_by)
    window.Element('-exclass_offmode-').update(set_to_index=off_modes.index(obj.off_mode))
    window.Element('-exclass_offtime-').update(value=obj.off_time)
    window.Element('-panBOOL-').update(value=obj.panbool)
    window.Element('-pan-').update(value=obj.pan_value)
    window.Element('-pan_keycenter-').update(value=obj.pan_keycenter)
    window.Element('-pan_keytrack-').update(value=obj.amp_keytrack)
    window.Element('-pan_veltrack-').update(value=obj.pan_veltrack)
    window.Element('-pan_random-').update(value=obj.pan_random)
    window.Element('-amp_keycenter-').update(value=obj.amp_keycenter)
    window.Element('-amp_keytrack-').update(value=obj.amp_keytrack)
    window.Element('-amp_veltrack-').update(value=obj.amp_veltrack)
    window.Element('-amp_random-').update(value=obj.amp_random)
    window.Element('-amp_lfoBOOL-').update(value=obj.amp_lfo)
    window.Element('-amp_lfo_delay-').update(value=obj.amp_lfo_delay)
    window.Element('-amp_lfo_fade-').update(value=obj.amp_lfo_fade)
    window.Element('-amp_lfo_depth-').update(value=obj.amp_lfo_depth)
    window.Element('-amp_lfo_freq-').update(value=obj.amp_lfo_freq)
    window.Element('-amp_velcurve_1BOOL-').update(value=obj.amp_velfloorbool)
    window.Element('-amp_velcurve_1-').update(value=obj.amp_velfloor)
    window.Element('-vel2attackBOOL-').update(value=obj.amp_env_vel2attackbool)
    window.Element('-vel2attack-').update(value=obj.amp_env_vel2attack)
    window.Element('-amp_envBOOL-').update(value=obj.amp_env)
    window.Element('-amp_env_delay-').update(value=obj.amp_env_delay)
    window.Element('-amp_env_attack-').update(value=obj.amp_env_attack)
    window.Element('-attack_shapeBOOL-').update(value=obj.amp_env_attack_shapebool)
    window.Element('-attack_shape-').update(value=obj.amp_env_attack_shape)
    window.Element('-amp_env_hold-').update(value=obj.amp_env_hold)
    window.Element('-amp_env_sustain-').update(value=obj.amp_env_sustain)
    window.Element('-amp_env_decay-').update(value=obj.amp_env_decay)
    window.Element('-decay_shapeBOOL-').update(value=obj.amp_env_decay_shapebool)
    window.Element('-decay_shape-').update(value=obj.amp_env_decay_shape)
    window.Element('-amp_env_release-').update(value=obj.amp_env_release)
    window.Element('-release_shapeBOOL-').update(value=obj.amp_env_release_shapebool)
    window.Element('-release_shape-').update(value=obj.amp_env_release_shape)
    window.Element('-filterBOOL-').update(value=obj.fil)
    window.Element('-filter_type-').update(set_to_index=filter_type.index(obj.fil_type))
    window.Element('-cutoff-').update(value=obj.cutoff)
    window.Element('-resonance-').update(value=obj.resonance)
    window.Element('-fil_keycenter-').update(value=obj.fil_keycenter)
    window.Element('-fil_keytrack-').update(value=obj.fil_keytrack)
    window.Element('-fil_veltrack-').update(value=obj.fil_veltrack)
    window.Element('-fil_random-').update(value=obj.fil_random)
    window.Element('-fil_lfo_delay-').update(value=obj.fil_lfo_delay)
    window.Element('-fil_lfo_fade-').update(value=obj.fil_lfo_fade)
    window.Element('-fil_lfo_depth-').update(value=obj.fil_lfo_depth)
    window.Element('-fil_lfo_freq-').update(value=obj.fil_lfo_freq)
    window.Element('-fil_envBOOL-').update(value=obj.fil_env)
    window.Element('-fil_env_depth-').update(value=obj.fil_env_depth)
    window.Element('-vel2depth-').update(value=obj.fil_vel2depth)
    window.Element('-fil_env_delay-').update(value=obj.fil_env_delay)
    window.Element('-fil_env_attack-').update(value=obj.fil_env_attack)
    window.Element('-fil_env_hold-').update(value=obj.fil_env_hold)
    window.Element('-fil_env_sustain-').update(value=obj.fil_env_sustain)
    window.Element('-fil_env_decay-').update(value=obj.fil_env_decay)
    window.Element('-fil_env_release-').update(value=obj.fil_env_release)
    window.Element('-pitchBOOL-').update(value=obj.pitch)
    window.Element('-pitch_keytrack-').update(value=obj.pitch_keytrack)
    window.Element('-pitch_veltrack-').update(value=obj.pitch_veltrack)
    window.Element('-pitch_random-').update(value=obj.pitch_random)
    window.Element('-pit_lfoBOOL-').update(value=obj.pit_lfo)
    window.Element('-pit_lfo_delay-').update(value=obj.pit_lfo_delay)
    window.Element('-pit_lfo_fade-').update(value=obj.pit_lfo_fade)
    window.Element('-pit_lfo_depth-').update(value=obj.pit_lfo_depth)
    window.Element('-pit_lfo_freq-').update(value=obj.pit_lfo_freq)
    window.Element('-pit_env_depth-').update(value=obj.pit_env_depth)
    window.Element('-pit_env_delay-').update(value=obj.pit_env_delay)
    window.Element('-pit_env_attack-').update(value=obj.pit_env_attack)
    window.Element('-pit_env_hold-').update(value=obj.pit_env_hold)
    window.Element('-pit_env_sustain-').update(value=obj.pit_env_sustain)
    window.Element('-pit_env_decay-').update(value=obj.pit_env_decay)
    window.Element('-pit_env_release-').update(value=obj.pit_env_release)
    window.Element('-opcode_notepad-').update(value=obj.opcode_notepad)

def get_map_names(map_objects):
    ls = []
    for map in map_objects:
        ls.append(map.get_name())
    return ls

sg.theme('DarkGray15')
global_layout = []

# init max values
gui_amp_delay = 5
gui_amp_attack = 20
gui_amp_hold = 10
gui_amp_sustain = int(100)
gui_amp_decay = 20
gui_amp_release = 10

menu_def = [
   ['File Project', ['New', 'Open', 'Save', 'Save As']],
]

dyn_map_col1 = [ sg.Text('Key:', pad=(0,0)),
                   sg.Spin(values=[i for i in range(0, 128)], initial_value=0, size=(3,3), k="-MAINMAP_LOKEY-", enable_events=True),
                   sg.Text("-", pad=(0,0)),
                   sg.Spin(values=[i for i in range(0, 128)], initial_value=127, size=(3,3), k="-MAINMAP_HIKEY-", enable_events=True),

                   sg.Text('  Vel:', pad=(0,0)),
                   sg.Spin(values=[i for i in range(0, 128)], initial_value=0, size=(3,3), k="-MAINMAP_LOVEL-", enable_events=True),
                   sg.Text("-", pad=(0,0)),
                   sg.Spin(values=[i for i in range(0, 128)], initial_value=127, size=(3,3), k="-MAINMAP_HIVEL-", enable_events=True),

                   sg.Checkbox('"note on"', pad=(0,0), key="-on_ccBOOL-"),
                   sg.Text('CC:', pad=(0,0)),
                   sg.Spin(values=[i for i in range(0, 128)], initial_value=64, size=(3,3), k="-on_ccNUMBER-", enable_events=True),
                   sg.Text('=', pad=(0,0)),
                   sg.Spin(values=[i for i in range(0, 128)], initial_value=0, size=(3,3), k="-on_locc-", enable_events=True),
                   sg.Text("-", pad=(0,0)),
                   sg.Spin(values=[i for i in range(0, 128)], initial_value=127, size=(3,3), k="-on_hicc", enable_events=True)
                   ]

'''
dyn_map_col2 = [sg.Text('Channel:', pad=(0,0)),
            sg.Spin(values=[i for i in range(1, 16)], initial_value=1, size=(3,3)),
            sg.Text("-", pad=(0,0)),
            sg.Spin(values=[i for i in range(1, 16)], initial_value=1, size=(3,3)),

            sg.Text('  Program:', pad=(0,0)),
            sg.Spin(values=[i for i in range(0, 128)], initial_value=0, size=(3,3)),
            sg.Text("-", pad=(0,0)),
            sg.Spin(values=[i for i in range(0, 128)], initial_value=127, size=(3,3))
            ]
'''

dyn_map_col2 = [sg.Checkbox('Random: ', pad=(0,0), k="-randBOOL-"),
                sg.Text('lo:', pad=(0,0)),
                sg.Input("0", size=(5,3), k="-lorand-", enable_events=True),
                sg.Text('hi:', pad=(0,0)),
                sg.Input("1", size=(5,3), k="-hirand-", enable_events=True),
                sg.Text("  Vol (dB):", pad=(0,0)),
                sg.Input("0", size=(5,3), k="-volume-", enable_events=True)
                ]

# MAPPING
mapping_properties = dyn_map_col1

#GLOBAL
global_layout = [sg.Checkbox(text='Keyswitch', k="-keyswitchBOOL-"), 
                  sg.Text('Range:', pad=(0,0)), 
                  sg.Spin(values=[i for i in range(0, 128)], initial_value=24, size=(3,3), k="-sw_lokey-", enable_events=True),
                  sg.Text("-", pad=(0,0)),
                  sg.Spin(values=[i for i in range(0, 128)], initial_value=36, size=(3,3), k="-sw_hikey-", enable_events=True),
                  sg.Text("Default:", pad=(0,0)),
                  sg.Spin(values=[i for i in range(0, 128)], initial_value=24, size=(3,3), k="-sw_default-", enable_events=True)
                  ]

# MAPPING
properties_layout = [[sg.Text("Output:"), sg.Spin(values=[i for i in range(0, 8)], initial_value=0, size=(3,3), readonly=True, k="-output-", enable_events=True)],
                     [sg.HorizontalSeparator()],
                     [sg.Checkbox(text="Polyphony:", k="-polyphonyBOOL-"), sg.Spin(values=[i for i in range(1, 513)], initial_value=16, size=(3,3), readonly=True, k="-polyphony-", enable_events=True)],
                     [sg.Checkbox(text="Note Polyphony:", k="-note_polyphonyBOOL-"), sg.Spin(values=[i for i in range(1, 513)], initial_value=16, size=(3,3), readonly=True, k="-note_polyphony-", enable_events=True)],
                     [sg.Checkbox(text="Note Selfmask", k="-note_selfmaskBOOL-", enable_events=True)],
                     [sg.HorizontalSeparator()],
                     [sg.Text("Trigger Mode: "), sg.Combo(values=trigger_modes, default_value=trigger_modes[0], readonly=True, k="-trigger_mode-", enable_events=True)],
                     [sg.Checkbox(text="rt_dead", k="-rt_dead-", enable_events=True)],
                     [sg.Checkbox(text="rt_decay (dB): ", k="-rt_decayBOOL-"), sg.Input("0", size=(5,3), k="-rt_decay-", enable_events=True)],
                     [sg.HorizontalSeparator()],
                     [sg.Checkbox("Keyswitch number:", k="-keyswitch_mapBOOL-"), sg.Spin(values=[i for i in range(0, 128)], initial_value=24, size=(3,3), k="-keyswitch_map-", enable_events=True)],
                     [sg.Text("Label:"), sg.Input(size=(20,3), k="-keyswitch_label-")],
                     [sg.HorizontalSeparator()],
                     [sg.Checkbox("Use 'key' opcode instead", k="-keyopcodeBOOL-")],
                     [sg.Checkbox("Set pitch_keycenter for all samples:", k="-pitch_keycenterBOOL-"), sg.Spin(values=[i for i in range(0, 128)], initial_value=60, size=(3,3), pad=(0,0), k="-pitch_keycenter-", enable_events=True)]
                     ]

# SAMPLE
sample_layout = [[sg.Checkbox("Offset", k="-offsetBOOL-"), sg.Input(size=(15,3), default_text="0", k="-offset-", enable_events=True)],
                 [sg.Text("Random Offset:"), sg.Input(size=(15,3), default_text="0", k="-random_offset-", enable_events=True)],
                 [sg.Text("Velocity->Offset:"), sg.Input(size=(15,3), default_text="0", k="-vel2offset-", enable_events=True)],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Sample Map Delay (sec):"), sg.Input(size=(15,3), default_text="0", k="-sample_delay-", enable_events=True)],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Pitch Transpose:"), sg.Spin(values=[i for i in range(-128, 128)], initial_value=0, size=(3,3), readonly=True, k="-pitch_transpose-", enable_events=True)],
                 [sg.Text("Note Transpose:"), sg.Spin(values=[i for i in range(-128, 128)], initial_value=0, size=(3,3), readonly=True, k="-note_transpose-", enable_events=True)],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Sample Quality (interpolation):"), sg.Combo(values=[i for i in range(1, 11)], default_value=2, readonly=True, k="-sample_quality-", enable_events=True)],
                 [sg.HorizontalSeparator()],
                 [sg.Text("Loop Mode:"), sg.Combo(values=loop_modes, default_value='None', readonly=True, k="-loop_mode-", enable_events=True)],
                 [sg.Text("Sample Direction:"), sg.Combo(values=loop_directions, default_value='None', readonly=True, k="-direction-", enable_events=True)],
                 [sg.HorizontalSeparator()],
                 [sg.Checkbox("Exclusive Class", k="-exclassBOOL-")],
                 [sg.Text("Group:"), sg.Spin(values=[i for i in range(0, 128)], initial_value=0, size=(3,3), pad=(0,0), k="-exclass_group-", enable_events=True)],
                 [sg.Text("Off by:"), sg.Spin(values=[i for i in range(0, 128)], initial_value=0, size=(3,3), pad=(0,0), k="-exclass_offby-", enable_events=True)],
                 [sg.Text("Off mode:"), sg.Combo(values=off_modes, default_value=off_modes[0], readonly=True, k="-exclass_offmode-", enable_events=True)],
                 [sg.Text("Off time:"), sg.Input("0.006", size=(6,3), k="-exclass_offtime-", enable_events=True)]
                 ]

# PAN
pan_layout = [[sg.Checkbox("Enable Pan", k="-panBOOL-")],
              [sg.Text('Pan'), sg.Slider(orientation="h", size=(58, 10), resolution=0.00, range=[-100, 100], default_value=0, k="-panSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pan-", enable_events=True)],
              [sg.Text("Pan Keycenter:"), sg.Spin(values=[i for i in range(0, 128)], initial_value=60, size=(3,3), readonly=True, k="-pan_keycenter-", enable_events=True)],
              [sg.Text('Pan Keytrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-100, 100], default_value=0, k="-pan_keytrackSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pan_keytrack-", enable_events=True)],
              [sg.Text('Pan Veltrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-100, 100], default_value=0, k="-pan_veltrackSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pan_veltrack-", enable_events=True)],
              [sg.Text('Pan Random'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-100, 100], default_value=0, k="-pan_randomSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pan_random-", enable_events=True)]
              ]


# AMPLIFIER
amp_layout = [[sg.Text("Amp Keycenter:"), sg.Spin(values=[i for i in range(0, 128)], initial_value=60, size=(3,3), readonly=True, k="-amp_keycenter-", enable_events=True)],
              [sg.Text('Amp Keytrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-96, 12], default_value=0, k="-amp_keytrackSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-amp_keytrack-", enable_events=True)],
              [sg.Text('Amp Veltrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-100, 100], default_value=100, k="-amp_veltrackSLIDER-", enable_events=True), sg.Input("100", size=(5,3), k="-amp_veltrack-", enable_events=True)],
              [sg.Text('Amp Random'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 24], default_value=0, k="-amp_randomSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-amp_random-", enable_events=True)],
              [sg.HorizontalSeparator()],
              [sg.Checkbox("Amp LFO", k="-amp_lfoBOOL-")],
              [sg.Text('LFO Delay'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 30], default_value=0, k="-amp_lfo_delaySLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-amp_lfo_delay-", enable_events=True)],
              [sg.Text('LFO Fade'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 30], default_value=0, k="-amp_lfo_fadeSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-amp_lfo_fade-", enable_events=True)],
              [sg.Text('LFO Depth'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-10, 10], default_value=0, k="-amp_lfo_depthSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-amp_lfo_depth-", enable_events=True)],
              [sg.Text('LFO Freq'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 20], default_value=15, k="-amp_lfo_freqSLIDER-", enable_events=True), sg.Input("15", size=(5,3), k="-amp_lfo_freq-", enable_events=True)],
              [sg.HorizontalSeparator()],
              [sg.Checkbox("Amp velocity floor:", k="-amp_velcurve_1BOOL-"), sg.Input("0", size=(6,3), k="-amp_velcurve_1-", enable_events=True)],
              [sg.Checkbox("Velocity->Env Amp Attack:", k="-vel2attackBOOL-"), sg.Input("0", size=(6,3), k="-vel2attack-", enable_events=True)]
              ]

env_amp_layout = [[sg.Checkbox(text="Enable Envelope", k="-amp_envBOOL-")],
            
            [sg.Frame(title="", layout=[
              [sg.Text('Delay')],
              [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_delay], k="-amp_env_delay-", enable_events=True),
               sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_delay, size=(3,3), k="-amp_env_delayMAX-", enable_events=True, readonly=True)]
            ])],

            
            [sg.Frame(title="", layout=[
             [sg.Text('Attack')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_attack], k="-amp_env_attack-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_attack, size=(3,3), k="-amp_env_attackMAX-", enable_events=True, readonly=True)],

             [sg.Checkbox(text="Enable", k="-attack_shapeBOOL-"), sg.Push(), sg.Text('Atk Shape'), sg.Slider(orientation="h", size=(30, 10), resolution=0.00, range=[-11, 11], default_value=LINEAR_CURVE, k="-attack_shape-"), sg.Button("Reset", k="-attack_shapeRESET-")]
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Hold')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_hold], k="-amp_env_hold-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_hold, size=(3,3), k="-amp_env_holdMAX-", enable_events=True, readonly=True)],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Sustain')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=int(0), range=[0, gui_amp_sustain], default_value=100, k="-amp_env_sustain-", enable_events=True)],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Decay')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_decay], k="-amp_env_decay-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_decay, size=(3,3), k="-amp_env_decayMAX-", enable_events=True, readonly=True)],

             [sg.Checkbox(text="Enable", k="-decay_shapeBOOL-"), sg.Push(), sg.Text('Dec Shape'), sg.Slider(orientation="h", size=(30, 10), resolution=0.00, range=[-11, 11], default_value=DECAY_CURVE, k="-decay_shape-"), sg.Button("Reset", k="-decay_shapeRESET-")]
             ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Release')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_release], k="-amp_env_release-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_release, size=(3,3), k="-amp_env_releaseMAX-", enable_events=True, readonly=True)],

             [sg.Checkbox(text="Enable", k="-release_shapeBOOL-"), sg.Push(), sg.Text('Rel Shape'), sg.Slider(orientation="h", size=(30, 10), resolution=0.00, range=[-11, 11], default_value=DECAY_CURVE, k="-release_shape-"), sg.Button("Reset", k="-release_shapeRESET-")]
            ])]
            ]

# FILTER
fil_layout = [[sg.Checkbox("Filter", k="-filterBOOL-")],
              [sg.Text("Type:"), sg.Combo(values=filter_type, default_value=filter_type[0], readonly=True, k="-filter_type-")],
              [sg.Text("Cutoff:"), sg.Slider(orientation="h", size=(55, 10), resolution=0, range=[0, 20000], default_value=11970, k="-cutoffSLIDER-", enable_events=True), sg.Input("11970", size=(5,3), k="-cutoff-", enable_events=True)],
              [sg.Text("Reso:"), sg.Slider(orientation="h", size=(55, 10), resolution=0.0, range=[0, 40], default_value=0, k="-resonanceSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-resonance-", enable_events=True)],
              [sg.HorizontalSeparator()],
              [sg.Text("Fil Keycenter:"), sg.Spin(values=[i for i in range(0, 128)], initial_value=60, size=(3,3), readonly=True, k="-fil_keycenter-", enable_events=True)],
              [sg.Text('Fil Keytrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0, range=[0, 1200], default_value=0, k="-fil_keytrackSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-fil_keytrack-", enable_events=True)],
              [sg.Text('Fil Veltrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0, range=[-9600, 9600], default_value=0, k="-fil_veltrackSLIDER-",enable_events=True), sg.Input("0", size=(5,3), k="-fil_veltrack-", enable_events=True)],
              [sg.Text('Fil Random'), sg.Slider(orientation="h", size=(52, 10), resolution=0, range=[0, 9600], default_value=0, k="-fil_randomSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-fil_random-", enable_events=True)],
              [sg.HorizontalSeparator()],
              [sg.Checkbox("Fil LFO", k="-fil_lfoBOOL-")],
              [sg.Text('LFO Delay'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 30], default_value=0, k="-fil_lfo_delaySLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-fil_lfo_delay-", enable_events=True)],
              [sg.Text('LFO Fade'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 30], default_value=0, k="-fil_lfo_fadeSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-fil_lfo_fade-", enable_events=True)],
              [sg.Text('LFO Depth'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-1200, 1200], default_value=0, k="-fil_lfo_depthSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-fil_lfo_depth-", enable_events=True)],
              [sg.Text('LFO Freq'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 20], default_value=15, k="-fil_lfo_freqSLIDER-", enable_events=True), sg.Input("15", size=(5,3), k="-fil_lfo_freq-", enable_events=True)]
              ]

env_fil_layout = [[sg.Checkbox(text="Enable Envelope", k="-fil_envBOOL-")],
            
            [sg.Text('Depth')],
              [sg.Slider(orientation="h", size=(60, 10), resolution=0, range=[-12000, 12000], default_value=0, k="-fil_env_depthSLIDER-", enable_events=True), sg.Input("0", size=(6,3), k="-fil_env_depth-", enable_events=True)],
            
            [sg.Text('Velocity->Depth')],
              [sg.Slider(orientation="h", size=(60, 10), resolution=0, range=[-12000, 12000], default_value=0, k="-vel2depthSLIDER-", enable_events=True), sg.Input("0", size=(6,3), k="-vel2depth-", enable_events=True)],
            
            [sg.Frame(title="", layout=[
              [sg.Text('Delay')],
              [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_delay], k="-fil_env_delay-", enable_events=True),
               sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_delay, size=(3,3), k="-fil_env_delayMAX-", enable_events=True, readonly=True)]
            ])],

            
            [sg.Frame(title="", layout=[
             [sg.Text('Attack')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_attack], k="-fil_env_attack-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_attack, size=(3,3), k="-fil_env_attackMAX-", enable_events=True, readonly=True)],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Hold')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_hold], k="-fil_env_hold-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_hold, size=(3,3), k="-fil_env_holdMAX-", enable_events=True, readonly=True)],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Sustain')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=int(0), range=[0, gui_amp_sustain], default_value=100, k="-fil_env_sustain-")],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Decay')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_decay], k="-fil_env_decay-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_decay, size=(3,3), k="-fil_env_decayMAX-", enable_events=True, readonly=True)],
             ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Release')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_release], k="-fil_env_release-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_release, size=(3,3), k="-fil_env_releaseMAX-", enable_events=True, readonly=True)],
            ])]
            ]

# PITCH
pit_layout = [[sg.Checkbox("Pitch", k="-pitchBOOL-")],
              [sg.Text('Pit Keytrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0, range=[-1200, 1200], default_value=100, k="-pitch_keytrackSLIDER-", enable_events=True), sg.Input("100", size=(5,3), k="-pitch_keytrack-", enable_events=True)],
              [sg.Text('Pit Veltrack'), sg.Slider(orientation="h", size=(52, 10), resolution=0, range=[-9600, 9600], default_value=0, k="-pitch_veltrackSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pitch_veltrack-", enable_events=True)],
              [sg.Text('Pit Random'), sg.Slider(orientation="h", size=(52, 10), resolution=0, range=[0, 9600], default_value=0, k="-pitch_randomSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pitch_random-", enable_events=True)],
              [sg.HorizontalSeparator()],
              [sg.Checkbox("Pitch LFO", k="-pit_lfoBOOL-")],
              [sg.Text('LFO Delay'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 30], default_value=0, k="-pit_lfo_delaySLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pit_lfo_delay-", enable_events=True)],
              [sg.Text('LFO Fade'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 30], default_value=0, k="-pit_lfo_fadeSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pit_lfo_fade-", enable_events=True)],
              [sg.Text('LFO Depth'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[-10, 10], default_value=0, k="-pit_lfo_depthSLIDER-", enable_events=True), sg.Input("0", size=(5,3), k="-pit_lfo_depth-", enable_events=True)],
              [sg.Text('LFO Freq'), sg.Slider(orientation="h", size=(52, 10), resolution=0.00, range=[0, 20], default_value=15, k="-pit_lfo_freqSLIDER-", enable_events=True), sg.Input("15", size=(5,3), k="-pit_lfo_freq-", enable_events=True)]
              ]

env_pit_layout = [[sg.Checkbox(text="Enable Envelope", k="-pit_envBOOL-")],
            
            [sg.Text('Depth (cents)')],
              [sg.Slider(orientation="h", size=(60, 10), resolution=0, range=[-12000, 12000], default_value=0, k="-pit_env_depthSLIDER-", enable_events=True), sg.Input("0", size=(7,3), k="-pit_env_depth-", enable_events=True)],
            
            [sg.Frame(title="", layout=[
              [sg.Text('Delay')],
              [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_delay], k="-pit_env_delay-", enable_events=True),
               sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_delay, size=(3,3), k="-pit_env_delayMAX-", enable_events=True, readonly=True)]
            ])],

            
            [sg.Frame(title="", layout=[
             [sg.Text('Attack')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_attack], k="-pit_env_attack-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_attack, size=(3,3), k="-pit_env_attackMAX-", enable_events=True, readonly=True)],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Hold')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_hold], k="-pit_env_hold-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_hold, size=(3,3), k="-pit_env_holdMAX-", enable_events=True, readonly=True)],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Sustain')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=int(0), range=[0, gui_amp_sustain], default_value=100, k="-pit_env_sustain-")],
            ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Decay')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_decay], k="-pit_env_decay-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_decay, size=(3,3), k="-pit_env_decayMAX-", enable_events=True, readonly=True)],
             ])],

            [sg.Frame(title="", layout=[
             [sg.Text('Release')],
             [sg.Slider(orientation="h", size=(60, 10), resolution=0.00, range=[0, gui_amp_release], k="-pit_env_release-", enable_events=True),
              sg.Spin(values=[i for i in range(1, 101)], initial_value=gui_amp_release, size=(3,3), k="-pit_env_releaseMAX-", enable_events=True, readonly=True)],
            ])]
            ]

# OPCODES
opcodes_layout = [[sg.Text("ADDITIONAL OPCODES")],
                  [sg.Multiline(size=(80, 30), k="-opcode_notepad-")]]

maps_tab = [[sg.Tab(title='MAP', layout=properties_layout)],
            [sg.Tab(title='SAMPLE', layout=sample_layout)],
            [sg.Tab(title='PAN', layout=pan_layout)],
            [sg.Tab(title='AMP', layout=amp_layout)],
            [sg.Tab(title='ENV AMP', layout=env_amp_layout)],
            [sg.Tab(title='FILTER', layout=fil_layout)],
            [sg.Tab(title='ENV FIL', layout=env_fil_layout)],
            [sg.Tab(title='PITCH', layout=pit_layout)],
            [sg.Tab(title='PIT ENV', layout=env_pit_layout)],
            [sg.Tab(title='OPCODES', layout=opcodes_layout)]]

mapping_layout = sg.TabGroup(layout=maps_tab)

# INIT
pypath = os.path.normpath(os.path.dirname(__file__))
preset_path = None
config_path = None
map_objects = []
global_obj = Global()
try:
    with open(pypath + "\\" + "userpath", "r") as f:
        config_path = f.readline()
except:
    config_path = None

if pathlib.Path(f"{config_path}\\Presets").is_dir():
    preset_path = f"{config_path}\\Presets"

# All the stuff inside your window.
main_layout = [[sg.Menu(menu_def)],
                [sg.Column([[sg.FolderBrowse("Select SFZBuilder Folder", k="-CONFIGPATH-", enable_events=True, p=(0,0))]]), sg.Column([[sg.Text(text=f"USERPATH: {config_path}", k="-CONFIGTEXT-", p=(0,0))]]), sg.Column([[sg.FolderBrowse("Set Preset File Location", k="-PRESETPATH-", enable_events=True, p=(0,0))]]),
                sg.Frame("", [[sg.Button('SAVE', k="-BUTTON_SAVE-", enable_events=True), sg.Checkbox("Real-time save", k="-AUTOSAVE-", enable_events=True)]])],

               [sg.Text(text=f"PRESET: {preset_path}\\", k="-PRESETTEXT-", p=(0,0)), sg.Input("My Preset", k="-PRESETINPUT-", p=(0,0), size=(30,3)), sg.Text(".sfz", p=(0,0))],
            [sg.Frame(title="Global", layout=[global_layout]), sg.Column([dyn_map_col1])],
            [sg.Text('Pack:', pad=(0,0)), sg.Combo(values=[], size=(45,10), readonly=True, k="-PACKCOMBO-", enable_events=True), sg.Text('Map:', pad=(0,0)), sg.Combo(values=[], size=(45,10), readonly=True, k="-MAPCOMBO-", enable_events=True), sg.Checkbox("Percussion", k="-percussionBOOL-", enable_events=True)],
            [sg.Column([dyn_map_col2])],
            [sg.Listbox(values=map_objects, size=(30, 35), key="-TABLEMAPS-", select_mode="BROWSE", enable_events=True), sg.VerticalSeparator(color=None), mapping_layout],
            [sg.Button(' + Mapping ', k="-BUTTON_MAP_ADD-"), sg.Button('  ^  ', k="-BUTTON_MAP_UP-"), sg.Button('  v  ', k="-BUTTON_MAP_DOWN-")],
            [sg.Button(' * Clone ', k="-BUTTON_MAP_CLONE-"), sg.Button(' - Delete ', k="-BUTTON_MAP_DELETE-"), sg.Button(' & Import ', k="-BUTTON_MAP_IMPORT-")]]

# print(vars(mymap))

slider_keys = ("-panSLIDER-",
               "-pan_keytrackSLIDER-",
               "-pan_veltrackSLIDER-",
               "-pan_randomSLIDER-",
               "-amp_keytrackSLIDER-",
               "-amp_veltrackSLIDER-",
               "-amp_randomSLIDER-",
               "-amp_lfo_delaySLIDER-",
               "-amp_lfo_fadeSLIDER-",
               "-amp_lfo_depthSLIDER-",
               "-amp_lfo_freqSLIDER-",
               "-cutoffSLIDER-",
               "-resonanceSLIDER-",
               "-fil_keytrackSLIDER-",
               "-fil_veltrackSLIDER-",
               "-fil_randomSLIDER-",
               "-fil_lfo_delaySLIDER-",
               "-fil_lfo_fadeSLIDER-",
               "-fil_lfo_depthSLIDER-",
               "-fil_lfo_freqSLIDER-",
               "-fil_env_depthSLIDER-",
               "-vel2depthSLIDER-",
               "-pitch_keytrackSLIDER-",
               "-pitch_veltrackSLIDER-",
               "-pitch_randomSLIDER-",
               "-pit_env_depthSLIDER-",
               "-pit_lfo_delaySLIDER-",
               "-pit_lfo_fadeSLIDER-",
               "-pit_lfo_depthSLIDER-",
               "-pit_lfo_freqSLIDER-")

env_slidermax_keys = ("-amp_env_delayMAX-",
                      "-amp_env_attackMAX-",
                      "-amp_env_holdMAX-",
                      "-amp_env_decayMAX-",
                      "-amp_env_releaseMAX-",
                      "-fil_env_delayMAX-",
                      "-fil_env_attackMAX-",
                      "-fil_env_holdMAX-",
                      "-fil_env_decayMAX-",
                      "-fil_env_releaseMAX-",
                      "-pit_env_delayMAX-",
                      "-pit_env_attackMAX-",
                      "-pit_env_holdMAX-",
                      "-pit_env_decayMAX-",
                      "-pit_env_releaseMAX-")

input_keys = ("-offset-",
              "-random_offset-",
              "-vel2offset-",
              "-sample_delay-",
              "-amp_velcurve_1-",
              "-vel2attack-",
              "-exclass_offtime-",
              "-volume-",
              "-pan-",
              "-pan_keytrack-",
              "-pan_veltrack-",
              "-pan_random-",
              "-vel2attack-",
              "-amp_veltrack-",
              "-amp_lfo_delay-",
              "-amp_lfo_fade-",
              "-fil_lfo_delay-",
              "-fil_lfo_fade-",
              "-pit_lfo_delay-",
              "-pit_lfo_fade-",
              "-pit_lfo_freq-",
              "-amp_lfo_freq-",
              "-fil_lfo_freq-",
              "-fil_env_depth-",
              "-vel2depth-",
              "-pit_env_depth-",
              "-fil_lfo_depth-",
              "-pitch_keytrack-",
              "-pit_lfo_depth-",
              "-fil_veltrack-",
              "-pitch_veltrack-",
              "-fil_random-",
              "-pitch_random-",
              "-cutoff-",
              "-fil_keytrack-",
              "-resonance-",
              "-amp_keytrack-",
              "-amp_random-",
              "-amp_lfo_depth-",
              "-lorand-",
              "-hirand-")

key_list_noupdate = (
    "-CONFIGPATH-",
    "-PRESETPATH-",
    "-AUTOSAVE-",
    "-PRESETINPUT-",
    "-PACKCOMBO-",
    "-MAPCOMBO-",
    "-TABLEMAPS-",
    "-BUTTON_SAVE-",
    "MouseWheel:Down",
    "MouseWheel:Up"
    )

# Ranges
GENERIC = (-100, 100)
GENERIC_PLUS = (0, 100)
LFO_DEPTH = (-10, 10)
LFO_FREQ = (0, 20)
DEPTH_A = (-12000, 12000)
DEPTH_A_PLUS = (0, 12000)
DEPTH_B = (-1200, 1200)
DEPTH_B_PLUS = (0, 1200)
DEPTH_C = (-9600, 9600)
DEPTH_C_PLUS = (0, 9600)
RESONANCE_RANGE = (0, 40)
AMP_KEYTRACK_RANGE = (-96, 12)
RT_DECAY_RANGE = (0, 200)
BINARY_RANGE = (0, 1)
MIDI_RANGE = (0, 127)


input_enter = False
QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'

def get_non_slider_keys(sliders, str):
    n = []
    for key in sliders:
        n.append(key.replace(str, ""))
    return n

def only_nums(num):
    try:
        b = float(num)
        if b.is_integer():
            r = int(num)
        else:
            r = b
        
        return r
    except:
        r = re.sub("\\D", "", num)
        if r == "":
            r = 0
        if float(r).is_integer():
            return int(r)
        else:
            return float(r)

def clip(n, range):
    if n < range[0]:
        return range[0]
    elif n > range[1]:
        return range[1]
    else:
        return n
    
def bool_map_buttons(window, bool):
        window.Element("-BUTTON_MAP_ADD-").update(disabled=bool)
        window.Element("-BUTTON_MAP_DELETE-").update(disabled=bool)
        window.Element("-BUTTON_MAP_CLONE-").update(disabled=bool)
        window.Element("-BUTTON_MAP_IMPORT-").update(disabled=bool)
        window.Element("-BUTTON_MAP_UP-").update(disabled=bool)
        window.Element("-BUTTON_MAP_DOWN-").update(disabled=bool)

# list all mappings under MSamples and PSamples into a dictionary
    # -> 'MSamples': ['Library1\\MSamples\\folder\\mapping.sfz', 'Library2\\MSamples\\folder\\mapping.sfz], 'PSamples': [...]
def get_mappings(config_path):
    mappings_dict = {}
    mappings_dict["MSamples"] = [p for p in glob.glob(f"**\\MSamples\\**", recursive=True, root_dir=f"{config_path}\\MappingPool\\") if p.endswith(".sfz")]
    mappings_dict["PSamples"] = [p for p in glob.glob(f"**\\PSamples\\**", recursive=True, root_dir=f"{config_path}\\MappingPool\\") if p.endswith(".sfz")]
    return mappings_dict

# convert the mapping dictionary into a non-repetitive list of libraries with the path of the sfz files as a list
    # -> 'Library1': ['MSamples\\folder\\mapping1.sfz', 'MSamples\\folder\\mapping2.sfz']
    # the given list variable should be already selected what kind of mapping is -> dict['MSamples'] or dict['PSamples']
def get_pack(ls):
    pack_dict = defaultdict(list)
    for p in ls:
        path_ls = pathlib.Path(p).parts # split path into list
        pack_dict[path_ls[0]].append(os.path.join(*path_ls[1:]))
    return pack_dict

# to get the list of some library based on index
def get_key_values(values, pack_dict, key):
    keys = list(pack_dict)
    if values['-MAPCOMBO-'] in keys:
        idx = keys.index(key)
    return pack_dict[keys[idx]]

current_map_ls = []
current_pack_dict = {}

def get_only_filenames(ls):
    r = []
    for str in ls:
        r.append(pathlib.Path(str).stem)
    return [r, ls]

def init_combos(window, pack_dict):
    pack_ls = list(pack_dict)
    window.Element("-PACKCOMBO-").update(value=pack_ls[0], values=pack_ls)
    map_ls = pack_dict[pack_ls[0]]
    current_map_ls = get_only_filenames(map_ls)
    window.Element("-MAPCOMBO-").update(value=current_map_ls[0][0], values=current_map_ls[0])
    return current_map_ls

def which_pack(mappings_dict, bool):
    pack = {}
    if bool:
        pack = get_pack(mappings_dict["PSamples"])
        return pack
    else:
        pack = get_pack(mappings_dict["MSamples"])
        return pack

def which_pack_str(bool):
    if bool:
        return "PSamples"
    else:        
        return "MSamples"

def generate_path(dots, ls):
    r = ""
    for i in range(dots):
        r += f"..\\"
    for j in range(len(ls)):
        r += f"{ls[j]}\\"
    return r

def save_sfz(path, dots, global_obj, mappings, values):
    sfz_content = "//THIS SFZ WAS GENERATED BY SFZBUILDER PROTOTYPE\n\n"
    sfz_content += f"<control>\n #define $USERPATH {dots}\n\n"
    
    if values["-keyswitchBOOL-"]:
        sfz_global = f"<global>\nsw_lokey={global_obj.keysw_range[0]} sw_hikey={global_obj.keysw_range[1]} sw_default={global_obj.sw_default}\n\n-"
        sfz_content += sfz_global

    for m in mappings:
        sfz_content += f"<master>\n"
        sfz_content += f"lobend={m.bend_range[0]} hibend={m.bend_range[1]}\n\n"
        sfz_content += f"locc133={m.map_key_range[0]} hicc133={m.map_key_range[1]}\n"
        sfz_content += f"locc131={m.map_vel_range[0]} hicc131={m.map_vel_range[1]}\n"
        if m.on_cc_rangebool:
            sfz_content += f"on_locc{m.on_cc_range[0]}={m.on_cc_range[1]} on_hicc{m.on_cc_range[0]}={m.on_cc_range[2]}\n"
        if m.random_rangebool:
            sfz_content += f"lorand={m.random_range[0]} hirand={m.random_range[0]}\n"
        sfz_content += f"volume={m.volume}\n\n"

        # MAP
        if m.polybool:
            sfz_content += f"polyphony={m.poly}\n"
        if m.note_polybool:
            sfz_content += f"note_polyphony={m.note_poly}\n"
        
        sfz_content += f"output={m.output}\n"
        sfz_content += f"trigger={m.trigger}\n"
        if m.rt_dead:
            sfz_content += f"rt_dead={m.rt_dead}\n"
        if m.rt_decaybool:
            sfz_content += f"rt_decay={m.rt_decay}\n"
        if m.keyswitchbool:
            sfz_content += f"sw_last={m.keyswitch}\n"
            sfz_content += f"sw_label={m.sw_label}\n"
        if m.keycenterbool:
            if m.key_opcode:
                sfz_content += f"key={m.keycenter}\n"
            else:
                sfz_content += f"pitch_keycenter={m.keycenter}\n"
        # SAMPLE
        if m.offsetbool:
            sfz_content += f"offset={m.offset}\n"
        sfz_content += f"offset={m.offset_random}\n"
        sfz_content += f"offset_cc131={m.vel2offset}\n\n"
        sfz_content += f"delay={m.delay}\n\n"
        sfz_content += f"transpose={m.pitch_transpose}\n"
        sfz_content += f"note_offset={m.note_offset}\n\n"
        sfz_content += f"sample_quality={m.quality}\n"
        if m.loop_mode != "None":
            sfz_content += f"loop_mode={m.loop_mode}\n"
        else:
            pass
        if m.direction != "None":
            sfz_content += f"direction={m.direction}\n"
        
        if m.exclass:
            sfz_content += "\n\n"
            sfz_content += f"group={m.group}\n"
            sfz_content += f"off_by={m.off_by}\n"
            sfz_content += f"off_mode={m.off_mode}\n"
            sfz_content += f"off_time={m.off_time}\n"
        
        # PAN
        if m.panbool:
            sfz_content += "\n\n"
            sfz_content += f"pan={m.pan_value}\n"
            sfz_content += f"pan_keycenter={m.pan_keycenter}\n"
            sfz_content += f"pan_keytrack={m.pan_keytrack}\n"
            sfz_content += f"pan_veltrack={m.pan_veltrack}\n"
            sfz_content += f"pan_random={m.pan_random}\n"
        
        # AMP
        sfz_content += "\n\n"
        sfz_content += f"amp_keycenter={m.amp_keycenter}\n"
        sfz_content += f"amp_keytrack={m.amp_keytrack}\n"
        sfz_content += f"amp_veltrack={m.amp_veltrack}\n"
        sfz_content += f"amp_random={m.amp_random}\n"

        if m.amp_lfo:
            sfz_content += "\n\n"
            sfz_content += f"amplfo_delay={m.amp_lfo_delay}\n"
            sfz_content += f"amplfo_fade={m.amp_lfo_fade}\n"
            sfz_content += f"amplfo_depth={m.amp_lfo_depth}\n"
            sfz_content += f"amplfo_freq={m.amp_lfo_freq}\n"
        
        if m.amp_lfo:
            sfz_content += "\n\n"
            sfz_content += f"amplfo_delay={m.amp_lfo_delay}\n"
            sfz_content += f"amplfo_fade={m.amp_lfo_fade}\n"
            sfz_content += f"amplfo_depth={m.amp_lfo_depth}\n"
            sfz_content += f"amplfo_freq={m.amp_lfo_freq}\n"
        if m.amp_velfloorbool:
            sfz_content += f"amp_velcurve_1={m.amp_velfloor}\n"
        if m.amp_env_vel2attackbool:
            sfz_content += f"ampeg_vel2attack={m.amp_env_vel2attack}\n"
        
        if m.amp_env:
            sfz_content += "\n\n"
            sfz_content += f"ampeg_delay={m.amp_env_delay}\n"
            sfz_content += f"ampeg_attack={m.amp_env_attack}\n"
            if m.amp_env_attack_shapebool:
                sfz_content += f"ampeg_attack_shape={m.amp_env_attack_shape}\n"
            sfz_content += f"ampeg_hold={m.amp_env_hold}\n"
            sfz_content += f"ampeg_sustain={m.amp_env_sustain}\n"
            sfz_content += f"ampeg_decay={m.amp_env_decay}\n"
            if m.amp_env_decay_shapebool:
                sfz_content += f"ampeg_decay_shape={m.amp_env_decay_shape}\n"
            sfz_content += f"ampeg_release={m.amp_env_release}\n"
            if m.amp_env_release_shapebool:
                sfz_content += f"ampeg_release_shape={m.amp_env_release_shape}\n"
        
        # FILTER
        if m.fil:
            sfz_content += "\n\n"
            sfz_content += f"fil_type={m.fil_type}\n"
            sfz_content += f"cutoff={m.cutoff}\n"
            sfz_content += f"resonance={m.resonance}\n\n"

            sfz_content += f"fil_keycenter={m.fil_keycenter}\n"
            sfz_content += f"fil_keytrack={m.fil_keytrack}\n"
            sfz_content += f"fil_veltrack={m.fil_veltrack}\n"
            sfz_content += f"fil_random={m.fil_random}\n"

            if m.fil_lfo:
                sfz_content += "\n\n"
                sfz_content += f"fillfo_delay={m.fil_lfo_delay}\n"
                sfz_content += f"fillfo_fade={m.fil_lfo_fade}\n"
                sfz_content += f"fillfo_depth={m.fil_lfo_depth}\n"
                sfz_content += f"fillfo_freq={m.fil_lfo_freq}\n"

            if m.fil_env:
                sfz_content += "\n\n"
                sfz_content += f"fileg_depth={m.fil_env_depth}\n"
                sfz_content += f"fil_vel2depth={m.fil_vel2depth}\n"
                sfz_content += f"fileg_delay={m.fil_env_delay}\n"
                sfz_content += f"fileg_attack={m.fil_env_attack}\n"
                sfz_content += f"fileg_hold={m.fil_env_hold}\n"
                sfz_content += f"fileg_sustain={m.fil_env_sustain}\n"
                sfz_content += f"fileg_decay={m.fil_env_decay}\n"
                sfz_content += f"fileg_release={m.fil_env_release}\n"
            
        if m.pitch:
            sfz_content += "\n\n"
            sfz_content += f"pitch_keytrack={m.pitch_keytrack}\n"
            sfz_content += f"pitch_veltrack={m.pitch_veltrack}\n"
            sfz_content += f"pitch_random={m.pitch_random}\n"

            if m.pit_lfo:
                sfz_content += "\n\n"
                sfz_content += f"pitchlfo_delay={m.pit_lfo_delay}\n"
                sfz_content += f"pitchlfo_fade={m.pit_lfo_fade}\n"
                sfz_content += f"pitchlfo_depth={m.pit_lfo_depth}\n"
                sfz_content += f"pitchlfo_freq={m.pit_lfo_freq}\n"
            
            if m.fil_env:
                sfz_content += "\n\n"
                sfz_content += f"pitcheg_depth={m.pit_env_depth}\n"
                sfz_content += f"pitcheg_delay={m.pit_env_delay}\n"
                sfz_content += f"pitcheg_attack={m.pit_env_attack}\n"
                sfz_content += f"pitcheg_hold={m.pit_env_hold}\n"
                sfz_content += f"pitcheg_sustain={m.pit_env_sustain}\n"
                sfz_content += f"pitcheg_decay={m.pit_env_decay}\n"
                sfz_content += f"pitcheg_release={m.pit_env_release}\n"
            
        sfz_content += "\n\n"
        sfz_content += "// ADDITIONAL OPCODES\n"
        sfz_content += f"{m.opcode_notepad}\n\n"

        sfz_content += "//MAPPING\n"
        sfz_content += f"<control>\ndefault_path=$USERPATH/MappingPool/{m.get_default_path()}\n#include \"$USERPATH/MappingPool/{m.get_include_path()}\"\n\n"

    f_sfz = open(os.path.normpath(path + ".sfz"), "w", encoding="utf8")
    f_sfz.write(sfz_content)
    f_sfz.close()
    print(f"""{os.path.normpath(str(path) + ".sfz")} written.""")


        #if values["-amp_lfoBOOL-"]:
        #    sfz_content += f"amplfo_delay={m.}"





mappings_dict = get_mappings(config_path)
mpack_dict = get_pack(mappings_dict["MSamples"])
ppack_dict = get_pack(mappings_dict["PSamples"])

#msamples = get_pack(current_mappings["MSamples"])
#mkeys = list(msamples)
#print(mkeys)
#result = [msamples[key] for key in mkeys if key in msamples]
#print(result)
#print(msamples[mkeys[4]])
#print(get_key_values(msamples, 4))

listbox_idx = None

# Create the Window
window = sg.Window('SFZBuilder Prototype', main_layout, size=(915, 885), return_keyboard_events=True, finalize=True)
# Event Loop to process "events" and get the "values" of the inputs

#window.bind('<FocusOut>', '+FOCUS OUT+')
#window['-PACKCOMBO-'].bind('<Enter>', '+MOUSE OVER+')
#window['-PACKCOMBO-'].bind('<Leave>', '+MOUSE AWAY+')
#window['-MAPCOMBO-'].bind('<Enter>', '+MOUSE OVER+')
#window['-MAPCOMBO-'].bind('<Leave>', '+MOUSE AWAY+')
#packcombo_bool = False
#mapcombo_bool = False

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    #print(list(values.keys()))

    # Sliders
    if event in slider_keys:
        window.Element(event.replace("SLIDER", "")).update(value=values[event]) # keyINPUT = keySLIDER
    # Inputs
    elif event in input_keys:
        last_input = str(event)
        last_input_value = values.get(last_input)
        input_enter = True
    elif event in get_non_slider_keys(slider_keys, "SLIDER"):
        last_input = str(event)
        input_enter = True
    
    # press enter
    if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2) and input_enter is True:
        if last_input in get_non_slider_keys(slider_keys, "SLIDER"):
            window.Element(last_input[:-1] + "SLIDER" + "-").update(value=values.get(last_input)) # keySLIDER = keyINPUT
            input_enter = False
        elif last_input in input_keys:
            val = 0
            match last_input:
                case "-amp_velcurve_1-" | "-lorand-" | "-hirand-":
                    val = clip(only_nums(values[last_input]), BINARY_RANGE)
                case "-vel2attack-" | "-pan-" | "-pan_keytrack-" | "-pan_veltrack-" | "-pan_random-" | "-vel2attack-" | "-amp_veltrack-":
                    val = clip(only_nums(values[last_input]), GENERIC)
                case "-sample_delay-" | "-amp_lfo_delay-" | "-amp_lfo_fade-" | "-fil_lfo_delay-" | "-fil_lfo_fade-" | "-pit_lfo_delay-" | "-pit_lfo_fade-":
                    val = clip(only_nums(values[last_input]), GENERIC_PLUS)
                case "-pit_lfo_freq-" | "-amp_lfo_freq-" | "-fil_lfo_freq-":
                    val = clip(only_nums(values[last_input]), LFO_FREQ)
                case "-fil_env_depth-" | "-vel2depth-" | "-pit_env_depth-":
                    val = clip(only_nums(values[last_input]), DEPTH_A)
                case "-fil_lfo_depth-" | "-pitch_keytrack-" | "-pit_lfo_depth-":
                    val = clip(only_nums(values[last_input]), DEPTH_B)
                case "-fil_veltrack-" | "-pitch_veltrack-":
                    val = clip(only_nums(values[last_input]), DEPTH_C)
                case "-fil_random-" | "-pitch_random-":
                    val = clip(only_nums(values[last_input]), DEPTH_C_PLUS)
                case "-cutoff-":
                    val = clip(only_nums(values[last_input]), (0, 20000))
                case "-fil_keytrack-":
                    val = clip(only_nums(values[last_input]), DEPTH_B_PLUS)
                case "-resonance-":
                    val = clip(only_nums(values[last_input]), RESONANCE_RANGE)
                case "-amp_keytrack-":
                    val = clip(only_nums(values[last_input]), AMP_KEYTRACK_RANGE)
                case "-amp_random-":
                    val = clip(only_nums(values[last_input]), (0, 24))
                case "-amp_lfo_depth-":
                    val = clip(only_nums(values[last_input]), LFO_DEPTH)
                case "-volume-":
                    val = only_nums(values[last_input])  
            window.Element(last_input).update(value=val)
            # updates the map object
            listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
            map_objects[listbox_idx].update(values)
            input_enter = False
    
    # reset envelope shape buttons
    if event in ("-attack_shapeRESET-", "-decay_shapeRESET-", "-release_shapeRESET-"):
        match event:
            case "-attack_shapeRESET-":
                window.Element(event.replace("RESET", "")).update(value=LINEAR_CURVE)
            case _:
                window.Element(event.replace("RESET", "")).update(value=DECAY_CURVE)
        listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
        map_objects[listbox_idx].update(values)

    # Sliders with Spin
    if event in env_slidermax_keys:
        window.Element(event.replace("MAX", "")).update(range=[0, values.get(event)]) 

    if event == "-CONFIGPATH-":
        print(event)
        with open(pypath + "\\" + "userpath", "w") as f:
            f.write(os.path.normpath(values[event]))
        config_path = os.path.normpath(values[event])
        window.Element("-CONFIGTEXT-").update(value=f"USERPATH: {config_path}") 
        if pathlib.Path(f"{config_path}\\Presets").is_dir():
            preset_path = f"{config_path}\\Presets"
            window.Element("-PRESETTEXT-").update(value=f"PRESET: {preset_path}\\")
        window.refresh()
    
    if event == "-PRESETPATH-":
        preset_path = os.path.normpath(values[event])
        window.Element("-PRESETTEXT-").update(value=f"PRESET: {preset_path}\\")
        window.refresh()
    
    if event == "-BUTTON_MAP_ADD-":
        if config_path is not None and preset_path is not None:
            # INIT MAP
            current_pack_dict = which_pack(mappings_dict, values["-percussionBOOL-"])
            current_map_ls = init_combos(window, current_pack_dict)
            sfz_map = Mapping(which_pack_str(values["-percussionBOOL-"]))
            #print(current_pack_dict)
            sfz_map.set_map(list(current_pack_dict)[0], current_map_ls[1][0])
            map_objects.append(sfz_map)
            window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=(len(map_objects) - 1))
        else:
            sg.popup_ok("Please check if SFZBuilder folder or Preset folder was selected.")
    
    if event in ("-BUTTON_MAP_DELETE-", "-BUTTON_MAP_CLONE-", "-BUTTON_MAP_UP-", "-BUTTON_MAP_DOWN-"):
        match event:
            case "-BUTTON_MAP_DELETE-":
                try:
                    listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
                    delete_popup = sg.popup_yes_no(f"Are you sure you want to remove {map_objects[listbox_idx].get_name()}?")
                    match delete_popup:
                        case "Yes":
                            del map_objects[listbox_idx]
                            window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=clip(listbox_idx - 1, (0, len(map_objects))))
                        case "No":
                            pass
                except IndexError:
                    pass
            case "-BUTTON_MAP_CLONE-":
                try:
                    listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
                    element = map_objects[listbox_idx]
                    map_objects.insert(clip(listbox_idx + 1, (0, len(map_objects))), element)
                    window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=listbox_idx)
                except IndexError:
                    pass
            case "-BUTTON_MAP_UP-":
                try:
                    listbox_idx = clip(window.Element("-TABLEMAPS-").get_indexes()[0], (0, len(map_objects)))
                    map_objects.insert(clip(listbox_idx - 1, (0, len(map_objects))), map_objects.pop(listbox_idx))
                    window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=clip(listbox_idx - 1, (0, len(map_objects))))
                except IndexError:
                    pass
            case "-BUTTON_MAP_DOWN-":
                try:
                    listbox_idx = clip(window.Element("-TABLEMAPS-").get_indexes()[0], (0, len(map_objects)))
                    map_objects.insert(clip(listbox_idx + 1, (0, len(map_objects))), map_objects.pop(listbox_idx))
                    window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=clip(listbox_idx + 1, (0, len(map_objects) - 1)))
                except IndexError:
                    pass
    
    if event == "-PACKCOMBO-":
        current_pack_dict = which_pack(mappings_dict, values["-percussionBOOL-"])
        current_map_ls = get_only_filenames(current_pack_dict[values["-PACKCOMBO-"]]) # convert 
        window.Element("-MAPCOMBO-").update(value=current_map_ls[0][0], values=current_map_ls[0])

        # update the object
        listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
        map_objects[listbox_idx].set_map(values["-PACKCOMBO-"], current_map_ls[1][0])
        window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=listbox_idx)

    if event == "-MAPCOMBO-":
        listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
        mp_idx = current_map_ls[0].index(values['-MAPCOMBO-']) # getting the simplified name index
        map_objects[listbox_idx].set_map(values['-PACKCOMBO-'], current_map_ls[1][mp_idx]) # stores the path of the map instead
        window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=listbox_idx)

    if event == "-percussionBOOL-":
        current_pack_dict = which_pack(mappings_dict, values["-percussionBOOL-"])
        current_map_ls = init_combos(window, current_pack_dict) # changes combos list

        # update the object
        try:
            listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
            map_objects[listbox_idx].set_map(list(current_pack_dict)[0], current_map_ls[1][0])
            map_objects[listbox_idx].change_type(which_pack_str(values["-percussionBOOL-"]))
            window.Element("-TABLEMAPS-").update(values=get_map_names(map_objects), set_to_index=listbox_idx)
        except IndexError:
            pass
    
    if event == "-TABLEMAPS-":
        # load the sfz mapping of the map object into the GUI
        listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
        pstr = map_objects[listbox_idx].pack
        pk_idx = list(current_pack_dict.keys()).index(pstr)
        mstr = map_objects[listbox_idx].map # complete name
        #print(pstr)
        #print(mstr)
        window.Element("-PACKCOMBO-").update(value=pstr, set_to_index=pk_idx)
        current_map_ls = get_only_filenames(current_pack_dict[pstr]) # convert
        mp_idx = current_map_ls[1].index(mstr) # stores index of complete name
        window.Element("-MAPCOMBO-").update(value=current_map_ls[0][mp_idx], values=current_map_ls[0]) # uses the same index for simplified name
        # get the stored values from the object
        get_map_values(window, values, map_objects[listbox_idx])

        for key in slider_keys:
            val = values[key.replace("SLIDER", "")]
            window.Element(key).update(value=val)
        for key in env_slidermax_keys:
            if values[key.replace("MAX", "")] >= values[key]:
                maxvalue = int(values[key]) + int(values[key.replace("MAX", "")])
                window.Element(key).update(range=[0, (maxvalue * 2)])
        window.refresh()
        #print(event)
    
    #print(event)
    
    if event not in key_list_noupdate:
        #print(event)
        listbox_idx = window.Element("-TABLEMAPS-").get_indexes()[0]
        map_objects[listbox_idx].update(values)
        #print(event)
    
    if event in ("-sw_lokey-", "-sw_hikey-", "-sw_default-"):
        global_obj.update(values)
    
    if event == "-BUTTON_SAVE-":
        common_path = os.path.commonprefix([config_path, preset_path])
        dots = (len(preset_path.split(os.sep)) - (len(common_path.split(os.sep)) - 1)) - 1
        r = ""
        for i in range(dots):
            r += f"../"
        define_userpath = r[:-1]
        pathstr = f"{preset_path}\\{values['-PRESETINPUT-']}"
        save_sfz(pathstr, define_userpath, global_obj, map_objects, values)



window.close()