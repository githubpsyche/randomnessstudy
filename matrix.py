#!/usr/bin/env python

# What this program is supposed to do:
# 1. Collects subject name and id.
# 2. Loads parameters defining matrix size, step size, and randomness type.
# 3. Generates switch(x) matrix for a random value x.
# 4. Permits subject to increment or decrease x and alter matrix's appearance.
# 5. Enables the subject to finish and save various data

import random, Tkinter, tkFont, os, time
from PIL import Image, ImageTk, ImageDraw

window = Tkinter.Tk()        # start up window
screen_midpoint = window.winfo_screenwidth()


# update canvas to reflect new switch(x) sequence
def update(canvas):
    s = switch(p)   # generate a switch sequence with which to define matrix
    matrix = Image.new('RGBA', (n, n)) # create image to draw matrix on
    draw = ImageDraw.Draw(matrix)

    # color tile colorA or colorB depending on switch(x) sequence
    # and lay tiles horizontally/vertically depending on prior random choice
    isHorizontal = random.choice([True, False])
    for i in range(n):
        for j in range(n):
            if s[i * n + j] is True:
                if isHorizontal: draw.point((i, j), colorA)
                else:            draw.point((j, i), colorA)
            else:
                if isHorizontal: draw.point((i, j), colorB)
                else:            draw.point((j, i), colorB)

    # size up and place matrix in window
    matrix = ImageTk.PhotoImage(matrix.resize((size, size), Image.NEAREST))
    canvas.create_image(size/2, size/2, image = matrix)
    canvas.matrix = matrix

# define a switch(x) sequence of length n^2
def switch(x):
    s = []                                     # define a bit string s:
    s.append(random.choice([True, False]))     # set its first bit randomly,
    for i in range(1, n * n):                  # but for every subsequent bit i,
        prior = s[i-1]                         # find its prior bit i-1,
        shouldSwitch = x > random.random()     # and with probability 1-x,
        if shouldSwitch: s.append(not prior)   # set i to opposite of its prior;
        else: s.append(prior)                  # otherwise, have i = its prior.
    return s

# provide interface for determining parameters by either filename or input
def getParameters():
    global window, parameters                  # global variables to be modified

    center = screen_midpoint/2 - 200           # establish center for interface
    window.geometry('+' + str(center) + '+0')  # place near center of screen
    # define the parameters I'm looking to clarify
    # last value in list decides whether config file or input decides parameters
    parameters = ['Configuration filename: ', 'Subject Name: ',
          'Step size [.0001, 1]: ', 'Tiles per row/column: ',
          'Matrix size (in pixels): ', 'First color (keep it simple): ',
          'Second color: ', Tkinter.IntVar()]

    # prepare window for the GUI
    for w in window.children.values(): w.destroy()     # clears window for GUI
    window.wm_title("Dynamic Switch(x) Matrix, 12/31/2014")    # titles window

    # start with instructions for the user at the top of the interface
    newframe = Tkinter.Frame(window)
    newframe.pack(side = Tkinter.TOP)
    instruct = ("\nInput a subject name AND specify a configuration."
                "\nYou can use a filename or specify the information here.\n"
                "\nThe file must be in a folder named 'config' within the same"
                "directory as this program.\n")
    Tkinter.Message(newframe, text = instruct,
                    justify = Tkinter.CENTER, width = 400,
                    font = tkFont.Font(family = 'Helvetica', size = 11)).pack()

    # set up labeled entry boxes for every parameter but the last
    for i in range(len(parameters)-1):
        newframe = Tkinter.Frame(window)
        newframe.pack(side = Tkinter.TOP)
        Tkinter.Label(newframe, justify = Tkinter.RIGHT, width = 35,
                      text = parameters[i]).pack(side = Tkinter.LEFT)
        parameters[i] = Tkinter.StringVar()
        Tkinter.Entry(newframe, textvariable = parameters[i]).pack(side = Tkinter.LEFT)

    # allow last parameter to be decided using a checkbox
    # last value in list decides whether config file or input decides parameters
    newframe = Tkinter.Frame(window)
    newframe.pack(side = Tkinter.TOP)
    Tkinter.Checkbutton(newframe, variable = parameters[-1], text =
            "Check here if loading parameters from configuration file").pack()

    # Finally, a Run button to set the parameters and then tile the matrix
    newframe = Tkinter.Frame(window)
    newframe.pack(side = Tkinter.TOP)
    Tkinter.Button(window, bg = 'yellow', text = 'Run',
                   command = setParameters,
                   font = tkFont.Font(family = 'Helvetica', size = 11)).pack()
    window.mainloop()

# establish global parameters according to user input
def setParameters():
    global p, n, step, subject, colorA, colorB, numPChanges, starttime, pStart, size

    # set parameters by user input or by loading a configuration file
    if parameters[-1].get() == 0:    # examine content of input if no filename
        step = float(parameters[2].get())
        n = int(parameters[3].get())
        size = int(parameters[4].get())
        colorA = parameters[5].get()
        colorB = parameters[6].get()
    else:    # otherwise grab most info from some file
        if parameters[0].get().endswith('.txt'): name = parameters[0].get()
        else:                             name = parameters[0].get() + '.txt'
        filename = open(os.getcwd() + '\\config\\' + name, 'r')
        config = filename.read().split('\n')
        filename.close()
        step = float(config[1])
        n = int(config[3])
        size = int(config[5])
        colorA = config[7]
        colorB = config[9]
    subject = parameters[1].get()   # must be input manually no matter what
    p = random.random()             # decided randomly every time
    pStart = p                      # must keep track of starting p
    numPChanges = 0                 # must start at 0 for every trial
    starttime = time.time()         # start timing how long trial takes
    tileMatrix()                    # tile matrix according to set parameters


# central method that generates matrix and interface for controlling it
def tileMatrix():
    global window, canvas                          # the basis of the matrix
    for w in window.children.values(): w.destroy() # clears window for matrix

    center = screen_midpoint/2 - size/2        # establish center for interface
    window.geometry('+' + str(center) + '+0')  # place near center of screen

    # generate an appropriately sized and titled backdrop for the GUI
    window.wm_title("Please adjust in order to make the input random")
    newframe = Tkinter.Frame(window)
    newframe.pack(side = Tkinter.TOP)
    canvas = Tkinter.Canvas(newframe, bg = 'grey',
                            height = size, width = size)
    canvas.pack()   # this has Tkinter decide the place of the canvas for me
    update(canvas)

    # establish the four buttons constituting the GUI:
    # the buttons incrementing/decrementing p by the value of step
    newframe = Tkinter.Frame(window)
    newframe.pack(side = Tkinter.TOP)
    stepfont = tkFont.Font(family = 'Helvetica', weight = 'bold', size = 12)
    Tkinter.Button(newframe, height = 2, width = 21, bg = 'blue', fg = 'white',
                   text = 'Less repeating', font = stepfont,
                   command = lessRepeat).pack(side = Tkinter.LEFT, padx = 30, pady = 10)
    Tkinter.Button(newframe, height = 2, width = 21, bg = 'blue', fg = 'white',
                   text = 'More repeating', font = stepfont,
                   command = moreRepeat).pack(side = Tkinter.LEFT, padx = 30, pady = 10)

    # ...and the buttons quitting and either saving or not saving collected data
    newframe = Tkinter.Frame(window)
    newframe.pack(side = Tkinter.TOP)
    quitfont = tkFont.Font(family = 'Helvetica', size = 11)
    Tkinter.Button(newframe, height = 1, width = 21, bg = 'yellow',
                   text = 'Quit and lose all data', font = quitfont,
                   command = getParameters).pack(side = Tkinter.LEFT, padx = 30, pady = 15)
    Tkinter.Button(newframe, height = 1, width = 21, bg = 'pink',
                   text = 'Record choice and quit', font = quitfont,
                   command = quitSave).pack(side = Tkinter.LEFT, padx = 30, pady = 15)
    window.mainloop()     # start the window

# increment p and thus also the probability of alternation; record change
def lessRepeat():
    global p, numPChanges, canvas      # global variables to be modified
    numPChanges = numPChanges + 1      # to be incremented
    if p + step <= 1: p = p + step     # increment p by step
    else: p = 1        # but if p would fall below 0, make it equal 0 instead
    update(canvas)     # update matrix

# decrease p and thus also the probability of alternation; record change
def moreRepeat():
    global p, numPChanges              # global variables to be modified
    numPChanges = numPChanges + 1      # to be incremented
    if p - step >= 0: p = p - step     # decrement p by step
    else: p = 0        # but if p would fall below 0, make it 0 instead
    update(canvas)       # update matrix

# quit and record all data, returning to the parameter-setting window
def quitSave():
    date = time.strftime("20%y_%m_%d")
    elapse = time.time() - starttime
    filename = open(os.getcwd() + '\\output\\output.txt', 'a')
    filename.write(subject + ' ' + date + ' ' + str(step) + ' ' + str(n) + ' '
                   + colorA + ' ' + colorB + ' ' + str(numPChanges) + ' '
                   + str(elapse) + ' ' + str(pStart) + " " + str(p) + '\n')
    filename.close()
    getParameters()

getParameters()