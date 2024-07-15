import pretty_midi

pm = pretty_midi.PrettyMIDI('media/Twinkle-Little-Star-Nr-1.mid')
data = {}

for i in pm.instruments:
    for n in i.notes:
        tstart = str(round(n.start, 1))
        pitch = n.pitch
        norm_pitch = pitch % 12 + 1

        if tstart not in data.keys():
            data[tstart] = [norm_pitch]
        else:
            data[tstart].append(norm_pitch)

print(data)