class SfzGlobal:
  def __init__(self):
    self.keysw = False
    self.keysw_range = [24, 36]
    self.sw_default = 24
    self.oversampling = "x1"
    self.portamento = False
    self.portamento_time = 0.05
    self.portamento_cc = 5
    self.portamento_time_mode = 0
    self.portamento_time_mode_add = 0.0
    self.bend_range = [-98304, 98304] # two octaves
    self.pitch_bendbool = True
    self.pitch_bend = 2400 # two octaves

  def change_value(self, var, val):
    if isinstance(val, str):
      exec(f"self.{var} = '{val}'")
    else:
      exec(f"self.{var} = {val}")
