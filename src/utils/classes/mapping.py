from ..constants import *
from ..enums import *
import pathlib

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

    self.pan_lfo = False
    self.pan_lfo_delay = 0
    self.pan_lfo_fade = 0
    self.pan_lfo_depth = 0
    self.pan_lfo_freq = 15
    self.pan_lfo_wave = lfo_waves[1]

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
    self.amp_lfo_wave = lfo_waves[1]

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
    self.fil_env_attack_shapebool = False
    self.fil_env_attack_shape = LINEAR_CURVE
    self.fil_env_hold = 0
    self.fil_env_sustain = 100
    self.fil_env_decay = 0
    self.amp_env_decay_shapebool = False
    self.amp_env_decay_shape = LINEAR_CURVE
    self.fil_env_release = 0
    self.amp_env_release_shapebool = False
    self.amp_env_release_shape = LINEAR_CURVE
    # FILTER LFO
    self.fil_lfo = False
    self.fil_lfo_delay = 0
    self.fil_lfo_fade = 0
    self.fil_lfo_depth = 0
    self.fil_lfo_freq = 15
    self.fil_lfo_wave = lfo_waves[1]

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
    self.pit_lfo_wave = lfo_waves[1]

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
