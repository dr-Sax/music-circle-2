import pygame
import sys
from core.input import Input  # from input.py

class Base(object):

    # A non-square screenSize will stretch the image along one dimension
    def __init__(self, screenSize = [512, 512]):

        # initialize all pygame modules
        pygame.init()

        # indicate rendering details (https://www.pygame.org/docs/ref/display.html for additional display settings i.e resizable window)
        # DOUBLEBUF - double buffering technique for rendering (two image buffers) - pixel data from one buffer is displayed while second buffer can be used to
        # store new image data.  This technique prevents screen tearing from synchronization issues between rendering cycles and display refresh rates for a single buffer.
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL  # bitwise OR for display settings

        # initialize buffers to perform antialiasing
        # Anti-aliasing removes jagged/pixelated lines for polygon endges.
        # each edge pixel is sampled multiple times where an offset smaller than pixel size is used to smooth pixel color transitions @edges.
        pygame.display.gl_set_attribute(
            pygame.GL_MULTISAMPLEBUFFERS, 
            1
            )

        pygame.display.gl_set_attribute(
            pygame.GL_MULTISAMPLESAMPLES, 
            4
            )

        # use a core OpenGL profile for cross-platform compatibility
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, 
            pygame.GL_CONTEXT_PROFILE_CORE
            )

        # create and display the window
        self.screen = pygame.display.set_mode(
            screenSize, 
            displayFlags
            )
        

        # set the text that appears in the title bar of the window
        pygame.display.set_caption('Graphics Window')


        # determine if main loop is active
        self.running = True

        # manage time-related data and operations
        # used to track time past since a function call, num of loop iterations, each loop represents an image effectively a frame rate.
        # 
        self.clock = pygame.time.Clock()

        # manage user input
        self.input = Input()

        # number of seconds application has been running
        self.time = 0
        self.deltaTime = 0


    # implement by extending class
    def initialize(self):
        pass

    # implement by extending class
    def update(self):
        pass

    def run(self):

        ## startup ##
        self.initialize()

        ## main loop ##  (At 60 fps, this runs once every 0.017 secs.)
        while self.running:

            ## process input ##
            self.input.update()
            if self.input.quit:
                self.running = False
                
            ## update ##
            self.update()

            # seconds since iteration of run loop
            self.deltaTime = self.clock.get_time() / 1000
            # increment time application has been running
            self.time += self.deltaTime

            ## render ##
            # display image on screen
            self.screen.fill((255, 255, 0))
            pygame.display.flip()    # switches which of the double buffers is displayed to the screen and written to.
            # pause if necessare to achieve 60 FPS
            self.clock.tick(60)

        ## shutdown ##
        pygame.quit()
        sys.exit()