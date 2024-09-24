from .functions import clip

def sfz_portamento(eg_idx, time):
    return f"""
eg{eg_idx}_sustain=1 //Pitch envelope setup for legato slides
eg{eg_idx}_level0=-1 //Envelope starts away from the note pitch
eg{eg_idx}_time0=0
eg{eg_idx}_pitch_oncc140=100 //This is the pitch depth\n
eg{eg_idx}_time1={time} //Glide time
eg{eg_idx}_level1=0 //At the end of the envelope, return to base pitch\n\n"""

def sfz_xfade(str):
    match str:
        case "key":
            return f"""
xfin_lokey=0 //Xfade in
xfin_hikey=63
xfout_lokey=64 //Xfade out
xfout_hikey=127
xf_keycurve=power // gain, power\n\n
            """
        case "vel":
            return f"""
xfin_lovel=0 //Xfade in
xfin_hivel=63
xfout_lovel=64 //Xfade out
xfout_hivel=127
xf_velcurve=power // gain, power\n\n
            """
        case _: # number
            return f"""
xfin_locc{str}=0 //Xfade in
xfin_hicc{str}=63
xfout_locc{str}=64 //Xfade out
xfout_hicc{str}=127
xf_cccurve=power // gain, power\n\n
            """

def sfz_roundrobin(length, index):
    len_ls = list(range(1, length+1))
    return f"""seq_length={length}\nseq_position={len_ls[index - 1]}\n\n"""

def sfz_random(length, index):
    rand_base = 1 / length
    rand_ls = [0]
    for i in length:
        rand_ls.append(rand_base * i)
    rand_ls.append(1)
    return f"""lorand={rand_ls[clip(index-2, (0, length-1))]}\nhirand={rand_ls[clip(index-1, (0, length-1))]}\n\n"""
