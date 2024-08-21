from pyo import *

s = Server().boot()
s.amp = 0.1

# Creates a sine wave as the source to process.
a = Sine().out()

# Passes the sine wave through an harmonizer.
h1 = Harmonizer(a).out()

# Then the harmonized sound through another harmonizer.
h2 = Harmonizer(h1).out()

# And again...
h3 = Harmonizer(h2).out()

# And again...
h4 = Harmonizer(h3).out()

s.gui(locals())