from pyo import *

PATH = 'C:/Users/nicor/OneDrive/Documents/Code/music-circle-2/main/media/beetlejuice.wav'
s = Server().boot()
s.start()
sf = SfPlayer(PATH, loop=True, mul=.5)
#chor = Chorus(sf, depth=[1.5,1.6], feedback=0.5, bal=0.5).out()
harm = Harmonizer(sf, transpo=-10, winsize=0.05).out(1)
s.gui(locals())