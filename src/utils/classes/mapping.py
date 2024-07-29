from ..constants import *
from ..enums import *
import pathlib
import os

class Mapping:
  def __init__(self, type):
    self.type = type
    self.pack = ""
    self.map = ""
    self.name = ""
    self.tuned = True
    self.tuned_checkbox = False
    self.comment = ""

    self.fx_mode = 0
    # UNISON
    self.fx_detune = 0
    self.fx_delay = 0
    self.fx_pan = 0
    # CHORUS
    self.fx_depth = 0
    self.fx_speed = 0
    self.fx_wave = 0

    # WAVETABLE
    self.wave = "Sine"
    self.wave_mode = "Normal/RM"
    self.wave_unison = 1
    self.wave_quality = 0
    self.wave_phase = -1
    self.wave_mod_depth = 0
    self.wave_mod_depth_ccbool = False
    self.wave_mod_depth_cc = [1, 0]
    self.wave_detune = 0
    self.wave_detune_ccbool = False
    self.wave_detune_cc = [1, 0]

    # TABLEWARP
    self.tw_waveform = "Sine-tri-saw"
    self.tw_waveform_offset = 0.0
    self.tw_warp = "Saw bend"
    self.tw_warp_offset = 0.0

    self.tw_waveform_eg = False
    self.tw_waveform_eg_depth = 0.0
    self.tw_waveform_eg_start = 0.0
    self.tw_waveform_eg_delay = 0.0
    self.tw_waveform_eg_attack = 0.0
    self.tw_waveform_eg_attack_shape = 0.0
    self.tw_waveform_eg_hold = 0.0
    self.tw_waveform_eg_decay = 0.0
    self.tw_waveform_eg_decay_shape = 0.0
    self.tw_waveform_eg_sustain = 0.0
    self.tw_waveform_eg_release = 0.0
    self.tw_waveform_eg_release_shape = 0.0

    self.tw_waveform_lfo = False
    self.tw_waveform_lfo_wave = "Triangle"
    self.tw_waveform_lfo_delay = 0.0
    self.tw_waveform_lfo_fade = 0.0
    self.tw_waveform_lfo_depth = 0.0
    self.tw_waveform_lfo_freq = 0.0

    self.tw_warp_eg = False
    self.tw_warp_eg_depth = 0.0
    self.tw_warp_eg_start = 0.0
    self.tw_warp_eg_delay = 0.0
    self.tw_warp_eg_attack = 0.0
    self.tw_warp_eg_attack_shape = 0.0
    self.tw_warp_eg_hold = 0.0
    self.tw_warp_eg_decay = 0.0
    self.tw_warp_eg_decay_shape = 0.0
    self.tw_warp_eg_sustain = 0.0
    self.tw_warp_eg_release = 0.0
    self.tw_warp_eg_release_shape = 0.0

    self.tw_warp_lfo = False
    self.tw_warp_lfo_wave = "Triangle"
    self.tw_warp_lfo_delay = 0.0
    self.tw_warp_lfo_fade = 0.0
    self.tw_warp_lfo_depth = 0.0
    self.tw_warp_lfo_freq = 0.0

    # MAP PROPERTIES
    self.mute = False
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
    self.pitch_bend_range = [-2400, 2400] # two octaves

    self.volume = 0

    self.keyswitchbool = False
    self.keyswitch = 24
    self.sw_label = ""

    self.output = 0
    self.width = 100

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
    self.tunebool = False
    self.tune = 0

    # SAMPLE PROPERTIES
    self.offsetbool = False
    self.offset = 0
    self.offset_random = 0
    self.delay = 0

    self.note_offset = 0
    self.pitch_transpose = 0

    self.qualitybool = False
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
    self.pan_lfo_wave = lfo_waves[0]

    # AMP PROPERTIES
    self.amp_keycenter = 60
    self.amp_keytrack = 0
    self.amp_veltrack = 100
    self.amp_random = 0
    # (PERC RELATED)
    self.amp_velfloorbool = False
    self.amp_velfloor = 0.000001 # amp_velcurve_1
    self.amp_env_vel2attackbool = False
    self.amp_env_vel2attack = 0 # ampeg_vel2attack

    # AMP ENVELOPE
    self.amp_env = False
    self.amp_env_ver = 0
    self.amp_env_start = 0
    self.amp_env_delay = 0
    self.amp_env_attack = 0
    self.amp_env_attack_shapebool = False
    self.amp_env_attack_shape = 0 # linear
    self.amp_env_hold = 0
    self.amp_env_decay = 0
    self.amp_env_decay_shapebool = False
    self.amp_env_decay_shape = DECAY_CURVE_B
    self.amp_env_sustain = 100
    self.amp_env_release = 0
    self.amp_env_release_shapebool = False
    self.amp_env_release_shape = DECAY_CURVE_B
    # AMP LFO
    self.amp_lfo = False
    self.amp_lfo_delay = 0
    self.amp_lfo_fade = 0
    self.amp_lfo_depth = 0
    self.amp_lfo_freq = 15
    self.amp_lfo_wave = lfo_waves[0]

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
    self.fil_env_ver = 0
    self.fil_env_start = 0
    self.fil_env_depth = 0
    self.fil_vel2depth = 0
    self.fil_env_delay = 0
    self.fil_env_attack = 0
    self.fil_env_attack_shapebool = False
    self.fil_env_attack_shape = 0 # linear
    self.fil_env_hold = 0
    self.fil_env_decay = 0
    self.fil_env_decay_shapebool = False
    self.fil_env_decay_shape = DECAY_CURVE_B
    self.fil_env_sustain = 100
    self.fil_env_release = 0
    self.fil_env_release_shapebool = False
    self.fil_env_release_shape = DECAY_CURVE_B
    # FILTER LFO
    self.fil_lfo = False
    self.fil_lfo_delay = 0
    self.fil_lfo_fade = 0
    self.fil_lfo_depth = 0
    self.fil_lfo_freq = 15
    self.fil_lfo_wave = lfo_waves[0]

    # PITCH PROPERTIES
    self.pitch = False
    self.pitch_veltrack = 0
    self.pitch_keytrack = 100
    self.pitch_random = 0
    # PITCH ENVELOPE
    self.pit_env = False
    self.pit_env_ver = 0
    self.pit_env_start = 0
    self.pit_env_depth = 0
    self.pit_env_delay = 0
    self.pit_env_attack = 0
    self.pit_env_hold = 0
    self.pit_env_decay = 0
    self.pit_env_sustain = 100
    self.pit_env_release = 0
    # PITCH LFO
    self.pit_lfo = False
    self.pit_lfo_delay = 0
    self.pit_lfo_fade = 0
    self.pit_lfo_depth = 0
    self.pit_lfo_freq = 15
    self.pit_lfo_wave = lfo_waves[0]

    # MISC
    self.opcode_notepad = ""

  def get_default_path(self):
    return f"{self.pack}/{os.path.dirname(self.map).replace(os.sep, '/')}"

  def get_include_path(self):
    pstr = f"{self.pack}/{self.map.replace(os.sep, '/')}"
    path = str(pathlib.Path(pstr).parent).replace(os.sep, '/')
    filename = pathlib.Path(pstr).stem
    if self.tuned is True and self.tuned_checkbox is True:
        return f"{path}/{filename} --TN.sfz"
    else:
      return f"{path}/{filename}.sfz"

  def get_name(self):
    match self.type:
      case "MSamples":
        return f"M: {self.name}"
      case "PSamples":
        return f"P({self.keycenter}): {self.name}"
      case "Wavetables":
        if self.wave == "Sample":
          return f"W: {self.name}"
        elif self.wave == "TableWarp2":
          return f"W: TableWarp"
        else:
          return f"W: {self.wave}"

  def get_name_b(self):
    match self.type:
      case "MSamples":
        return self.name
      case "PSamples":
        return self.name
      case "Wavetables":
        if self.wave == "Sample":
          return self.name
        else:
          return self.wave

  def get_wave(self):
    match self.wave:
      case "Sine":
        return "*sine"
      case "Triangle":
        return "*triangle"
      case "Square":
        return "*square"
      case "Saw":
        return "*saw"
      case "Noise":
        return "*noise"
      case "Sample":
        return self.map
      case "TableWarp2":
        return "*com.Madbrain.TableWarp2"

  def set_map(self, pack, map):
    self.pack = pack
    self.map = map.replace('\\',"/")
    self.name = pathlib.Path(self.map).stem

  def change_type(self, type):
    self.type = type

  def change_value(self, var, val):
    if isinstance(val, str):
      if var == "opcode_notepad":
        self.opcode_notepad = val
      else:
        exec(f"self.{var} = '{val}'")
    else:
      if "env_release" in var and not isinstance(val, bool):
        if val == 0:
          val = ZERO
      exec(f"self.{var} = {val}")
