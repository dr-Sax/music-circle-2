from pyo import *
s = Server()
s.setMidiInputDevice(1)
s.boot()
notes = Notein(poly=10, scale=1, mul=.5)
adsr = MidiAdsr(notes['velocity'],attack=.005,decay=.1, sustain=.4, release=1)
ratio = Midictl(1, channel=1, mul=.5)
index1 = Midictl(2, channel=1, mul=5)
index2 = Midictl(3, channel=1, mul=5)
print(index1)
xfm = CrossFM(carrier = notes['pitch'], ratio=ratio, ind1=index1, ind2=index2, mul=adsr).out()
s.gui(locals())

while True:
    print(index1)