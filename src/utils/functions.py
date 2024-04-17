from collections  import defaultdict
from pathlib      import Path
import pathlib
import os
import json
import glob

def generate_eg(type, destination, idx, start, delay, attack, hold, decay, sustain, release, shapes=[[False, 0], [False, 0], [False, 0]]): # [attackshape, decayshape, releaseshape]
  output = ""
  output += "\n\n"
  match destination:
    case "amp":
      eg = 0
    case "fil":
      eg = 1
    case "pit":
      eg = 2

  if type == 0:
    match eg:
      case 0:
        output += f"ampeg_start={start}\n"
        output += f"ampeg_delay={delay}\n"
        output += f"ampeg_attack={attack}\n"
        if shapes[0][0]:
            output += f"ampeg_attack_shape={shapes[0][1]}\n"

        output += f"ampeg_hold={hold}\n"
        output += f"ampeg_sustain={sustain}\n"
        output += f"ampeg_decay={decay}\n"
        if shapes[1][0]:
            output += f"ampeg_decay_shape={shapes[1][1]}\n"

        output += f"ampeg_release={release}\n"
        if shapes[2][0]:
            output += f"ampeg_release_shape={shapes[2][1]}\n"
      case 1:
        output += f"fileg_start={start}\n"
        output += f"fileg_delay={delay}\n"
        output += f"fileg_attack={attack}\n"
        if shapes[0][0]:
            output += f"fileg_attack_shape={shapes[0][1]}\n"

        output += f"fileg_hold={hold}\n"
        output += f"fileg_sustain={sustain}\n"
        output += f"fileg_decay={decay}\n"
        if shapes[1][0]:
            output += f"fileg_decay_shape={shapes[1][1]}\n"

        output += f"fileg_release={release}\n"
        if shapes[2][0]:
            output += f"fileg_release_shape={shapes[2][1]}\n"
      case 2:
        output += f"pitcheg_start={start}\n"
        output += f"pitcheg_delay={delay}\n"
        output += f"pitcheg_attack={attack}\n"
        if shapes[0][0]:
            output += f"pitcheg_attack_shape={shapes[0][1]}\n"

        output += f"pitcheg_hold={hold}\n"
        output += f"pitcheg_sustain={sustain}\n"
        output += f"pitcheg_decay={decay}\n"
        if shapes[1][0]:
            output += f"pitcheg_decay_shape={shapes[1][1]}\n"

        output += f"pitcheg_release={release}\n"
        if shapes[2][0]:
            output += f"pitcheg_release_shape={shapes[2][1]}\n"
  else: # Flex
    match eg:
      case 0:
        output += f"eg{idx+1}_ampeg=100\n"
        output += f"eg{idx+1}_sustain=4\n"
        output += f"eg{idx+1}_level0={float(start) / 100} eg{idx+1}_time0=0.0000001\n"
        output += f"eg{idx+1}_level1={float(start) / 100} eg{idx+1}_time1={delay}\n"
        output += f"eg{idx+1}_level2=1 eg{idx+1}_time2={attack}\n"
        if shapes[0][0]:
            output += f"eg{idx+1}_shape2={shapes[0][1]}\n"
        output += f"eg{idx+1}_level3=1 eg{idx+1}_time3={hold}\n"
        output += f"eg{idx+1}_level4={float(sustain) / 100} eg{idx+1}_time4={decay}\n"
        if shapes[1][0]:
            output += f"eg{idx+1}_shape4={shapes[1][1]}\n"
        output += f"eg{idx+1}_level5=0 eg{idx+1}_time5={release}\n"
        if shapes[2][0]:
            output += f"eg{idx+1}_shape5={shapes[2][1]}\n"
      case 1:
        output += f"eg{idx+2}_sustain=4\n"
        output += f"eg{idx+2}_level0={float(start) / 100} eg{idx+2}_time0=0.0000001\n"
        output += f"eg{idx+2}_level1={float(start) / 100} eg{idx+2}_time1={delay}\n"
        output += f"eg{idx+2}_level2=1 eg{idx+2}_time2={attack}\n"
        if shapes[0][0]:
            output += f"eg{idx+2}_shape2={shapes[0][1]}\n"
        output += f"eg{idx+2}_level3=1 eg{idx+2}_time3={hold}\n"
        output += f"eg{idx+2}_level4={float(sustain) / 100} eg{idx+2}_time4={decay}\n"
        if shapes[1][0]:
            output += f"eg{idx+2}_shape4={shapes[1][1]}\n"
        output += f"eg{idx+2}_level5=0 eg{idx+2}_time5={release}\n"
        if shapes[2][0]:
            output += f"eg{idx+2}_shape5={shapes[2][1]}\n"
      case 2:
        output += f"eg{idx+3}_sustain=4\n"
        output += f"eg{idx+3}_level0={float(start) / 100} eg{idx+3}_time0=0.0000001\n"
        output += f"eg{idx+3}_level1={float(start) / 100} eg{idx+3}_time1={delay}\n"
        output += f"eg{idx+3}_level2=1 eg{idx+3}_time2={attack}\n"
        if shapes[0][0]:
            output += f"eg{idx+3}_shape2={shapes[0][1]}\n"
        output += f"eg{idx+3}_level3=1 eg{idx+3}_time3={hold}\n"
        output += f"eg{idx+3}_level4={float(sustain) / 100} eg{idx+3}_time4={decay}\n"
        if shapes[1][0]:
            output += f"eg{idx+3}_shape4={shapes[1][1]}\n"
        output += f"eg{idx+3}_level5=0 eg{idx+3}_time5={release}\n"
        if shapes[2][0]:
            output += f"eg{idx+3}_shape5={shapes[2][1]}\n"
  return output

def get_mappings(config_path):
  mappings_dict = {}
  mappings_dict["MSamples"] = [p for p in glob.glob(f"**/MSamples/**", recursive=True, root_dir=f"{config_path}/MappingPool/") if p.endswith(".sfz")]
  mappings_dict["PSamples"] = [p for p in glob.glob(f"**/PSamples/**", recursive=True, root_dir=f"{config_path}/MappingPool/") if p.endswith(".sfz")]
  mappings_dict["Wavetables"] = [p for p in glob.glob(f"**", recursive=True, root_dir=f"{config_path}/Wavetables/") if p.endswith(".wav")]
  return mappings_dict

def get_pack(ls):
  pack_dict = defaultdict(list)
  for p in ls:
      path_ls = pathlib.Path(p).parts # split path into list
      pack_dict[path_ls[0]].append(os.path.join(*path_ls[1:]))
  return pack_dict

def which_pack(mappings_dict, pbool, wbool):
    pack = {}
    if pbool:
        pack = get_pack(mappings_dict["PSamples"])
        return pack
    else:
        if wbool:
          pack = get_pack(mappings_dict["Wavetables"])
        else:
          pack = get_pack(mappings_dict["MSamples"])
        return pack

def which_pack_str(pbool, wbool):
    if pbool:
        return "PSamples"
    else:
        if wbool:
          return "Wavetables"
        else:
          return "MSamples"

def get_map_names(map_objects):
    ls = []
    for map in map_objects:
        ls.append(map.get_name())
    return ls

def clip(n, range):
    if n < range[0]:
        return range[0]
    elif n > range[1]:
        return range[1]
    else:
        return n

def float_to_int(_flt, decimals):
  negative = False
  flt = "{:.3f}".format(float(_flt))
  ls = str(flt).split(".")
  if "-" in ls[0]:
    negative = True
    s = ls[0][1:]
  else:
    s = ls[0]
  zeros = (decimals - len(ls[1]))
  d = ls[1] + ("0" * zeros)
  r = s + d
  if negative:
    r = "-" + r
  return int(r)

def int_to_float(integer, decimals):
  decimals = 3
  negative = False
  ls = str(integer)
  if "-" in ls[0]:
    negative = True
    s = ls[1:]
  else:
    s = ls
  if len(s) <= decimals:
    predecimal = 0
  else:
    predecimal = s[:-abs(decimals)]

  postdecimal = s[-abs(decimals):]
  r = f"{predecimal}.{postdecimal}"
  if negative:
    r = "-" + r

  return float(r)

def save_project(projpath, name, global_obj, map_objects):
  proj_dict = {}
  proj_dict["global"] = vars(global_obj)
  proj_dict["maps"] = []
  for obj in map_objects:
      proj_dict["maps"].append(vars(obj))
  output_file = Path(os.path.normpath(f"{projpath}/{name}"))
  output_file.parent.mkdir(exist_ok=True, parents=True)
  with open(os.path.normpath(f"{projpath}/{name}"), 'w') as f:
    json.dump(proj_dict, f)
