class SfzGlobal:
  def __init__(self):
    self.keysw = False
    self.keysw_range = [24, 36]
    self.sw_default = 24

  def change_value(self, var, val):
    if isinstance(val, str):
      exec(f"self.{var} = '{val}'")
    else:
      exec(f"self.{var} = {val}")
