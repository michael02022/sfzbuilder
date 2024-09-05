from collections  import defaultdict
from pathlib      import Path
import pathlib
import os
import json
import glob
import math
import re

def only_nums(str):
    r = re.sub(r'[^\d]+', '', str)
    return r

def cents_to_hz(hz, cents):
  result = math.pow(2, cents/1200) * hz
  return result

def reformat_string_paths(ls):
  n = []
  for string in ls:
    pth = pathlib.Path(string).parts
    if pth[0] in ("MSamples", "PSamples"):
       n_str = str(os.path.join(*pth[1:]))
    else:
      n_str = str(os.path.join(*pth))
    n.append(n_str.replace("/", " » ").replace("\\", " » "))
  return n

def cc_sw(cc, value):
  try:
    match int(str(value).split('.')[1]):
      case 1:
        return 135 # unipolar random
      case 2:
        return 136 # bipolar random
      case 3:
        return 137 # alternate random
      case _:
        return cc
  except:
    return cc

def notepad_opcode_filter(txt, lfo_idx, eg_idx):
  # please I need a better way to do this
  # SFZ v2
  r1 = txt.replace("egN_", f"eg{eg_idx}")
  r2 = r1.replace("egNA", f"eg{eg_idx+1}")
  r3 = r2.replace("egNF", f"eg{eg_idx+2}")
  r4 = r3.replace("egNP", f"eg{eg_idx+3}")

  r5 = r4.replace("lfoN_", f"lfo{lfo_idx}")
  r6 = r5.replace("lfoNA", f"lfo{lfo_idx+1}")
  r7 = r6.replace("lfoNF", f"lfo{lfo_idx+2}")
  r8 = r7.replace("lfoNP", f"lfo{lfo_idx+3}")

  # CC
  r9 = r8.replace("ccMOD", "cc1")
  r10 = r9.replace("ccBREATH", "cc2")
  r11 = r10.replace("ccFOOT", "cc4")
  r12 = r11.replace("ccGLIDE", "cc5")
  r13 = r12.replace("ccVOL", "cc7")
  r14 = r13.replace("ccPAN", "cc10")
  r15 = r14.replace("ccEXP", "cc11")
  r16 = r15.replace("ccHOLD", "cc64")
  r17 = r16.replace("ccHOLD2", "cc69")
  r18 = r17.replace("ccRESO", "cc71")
  r19 = r18.replace("ccRELEASE", "cc72")
  r20 = r19.replace("ccATTACK", "cc73")
  r21 = r20.replace("ccCUTOFF", "cc74")

  # SFZ CC
  r22 = r21.replace("ccPITCHBEND", "cc128")
  r23 = r22.replace("ccVEL", "cc131")
  r24 = r23.replace("ccVELOFF", "cc132")
  r25 = r24.replace("ccKEY", "cc133")
  r26 = r25.replace("ccKEYGATE", "cc134")
  r27 = r26.replace("ccUNIRAND", "cc135")
  r28 = r27.replace("ccBIRAND", "cc136")
  r29 = r28.replace("ccALTER", "cc137")

  # FX
  r30 = r29.replace("lfoFX", f"lfo{lfo_idx+4}")

  # TABLEWARP
  r31 = r30.replace("lfoTW1", f"lfo{lfo_idx+5}")
  r32 = r31.replace("lfoTW2", f"lfo{lfo_idx+6}")

  return r32

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

def generate_eg_tw(idx, start, delay, attack, attack_shape, hold, decay, decay_shape, sustain, release, release_shape):
  output = ""
  output += f"eg{idx}_sustain=4\n"
  output += f"eg{idx}_level0={float(start) / 100} eg{idx}_time0=0.0000001\n"
  output += f"eg{idx}_level1={float(start) / 100} eg{idx}_time1={delay}\n"
  output += f"eg{idx}_level2=1 eg{idx}_time2={attack}\n"
  output += f"eg{idx}_shape2={attack_shape}\n"
  output += f"eg{idx}_level3=1 eg{idx}_time3={hold}\n"
  output += f"eg{idx}_level4={float(sustain) / 100} eg{idx}_time4={decay}\n"
  output += f"eg{idx}_shape4={decay_shape}\n"
  output += f"eg{idx}_level5=0 eg{idx}_time5={release}\n"
  output += f"eg{idx}_shape5={release_shape}\n"
  return output

def get_mappings(config_path):
  mappings_dict = {}
  mappings_dict["MSamples"] = [p.replace('\\',"/") for p in glob.glob(f"**/MSamples/**", recursive=True, root_dir=f"{config_path}/MappingPool/") if p.endswith(".sfz") and not p.endswith(" --TN.sfz")]
  mappings_dict["PSamples"] = [p.replace('\\',"/") for p in glob.glob(f"**/PSamples/**", recursive=True, root_dir=f"{config_path}/MappingPool/") if p.endswith(".sfz")]
  mappings_dict["Wavetables"] = [p.replace('\\',"/") for p in glob.glob(f"**", recursive=True, root_dir=f"{config_path}/Wavetables/") if p.endswith(".wav")]
  return mappings_dict

def get_pack(ls):
  pack_dict = defaultdict(list)
  for p in ls:
      path_ls = pathlib.Path(p).parts # split path into list
      pack_dict[path_ls[0]].append(str(os.path.join(*path_ls[1:]).replace('\\',"/")))
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

def float_to_int(flt, decimals):
  dec = 10 ** decimals
  return int(flt * dec)

def int_to_float(integer, decimals):
  dec = 10 ** decimals
  return float(integer / dec)

def _float_to_int(_flt, decimals):
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

def _int_to_float(integer, decimals):
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

def save_project(projpath, name, global_obj, map_objects, fx):
  proj_dict = {}
  proj_dict["global"] = vars(global_obj)
  proj_dict["effects"] = json.loads(json.dumps(fx))
  proj_dict["maps"] = []
  for obj in map_objects:
      proj_dict["maps"].append(vars(obj))
  output_file = Path(os.path.normpath(f"{projpath}/{name}"))
  output_file.parent.mkdir(exist_ok=True, parents=True)
  with open(os.path.normpath(f"{projpath}/{name}"), 'w') as f:
    json.dump(proj_dict, f)
