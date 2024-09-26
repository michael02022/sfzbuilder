from .functions import clip

def sfz_portamento(eg_idx, time):
    return f"""
eg{eg_idx}_sustain=1
eg{eg_idx}_level0=-1
eg{eg_idx}_time0=0
eg{eg_idx}_pitch_oncc140=100 //This is the pitch depth
eg{eg_idx}_time1={time} //GLIDE TIME
eg{eg_idx}_level1=0\n"""

def sfz_xfade(str):
    match str:
        case "key":
            return f"""
xfin_lokey=0 //in
xfin_hikey=63
xfout_lokey=64 //out
xfout_hikey=127
xf_keycurve=power // gain, power\n"""
        case "vel":
            return f"""
xfin_lovel=0 //in
xfin_hivel=63
xfout_lovel=64 //out
xfout_hivel=127
xf_velcurve=power // gain, power\n"""
        case _: # number
            return f"""
xfin_locc{str}=0 //in
xfin_hicc{str}=63
xfout_locc{str}=64 //out
xfout_hicc{str}=127
xf_cccurve=power // gain, power\n"""

def sfz_roundrobin(length, index):
    if index > length:
        index = length
    len_ls = list(range(1, length+1))
    return f"""seq_length={length}\nseq_position={len_ls[index - 1]}\n\n"""

def sfz_random(length, index):
    rand_base = 1 / length
    rand_ls = []
    for i in range(length):
        rand_ls.append(rand_base * i)
    rand_ls.append(1)
    return f"""lorand={rand_ls[clip(index-1, (0, length-1))]}\nhirand={rand_ls[clip(index, (0, length))]}\n\n"""

def sfz_midi_value(length, index):
    value_base = 127 // length
    value_ls = []
    for i in range(length):
        value_ls.append(value_base * i)
    value_ls.append(127)
    return f"""{value_ls[clip(index-1, (0, length-1))]}\n{value_ls[clip(index, (0, length))]}\n\n"""
