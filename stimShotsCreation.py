import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui
from itertools import combinations, permutations

### R = tr, L = vl, x = ee. changed for programming purposes of keeping all words same length.
# only changed in trial ['fullTrial'], not in w1,2,3,4
units=['t','R','v','L','eb','Xb','ig','Ug']
onsets=['t','R','v','L']
clusters = ['R','L']
rhymes=['eb','Xb','ig','Ug']
#define keys to be used and corresponding sounds
capKeys = {'t':'1','R':'2','v':'3','L':'4',
          'eb':'7','Xb':'8','ig':'9', 'Ug':'0'}

words=set() # make 3-l words
for c1 in onsets:
    for c2 in rhymes:
        w1=c1+c2
        words.update([w1])

#create object for presenting key combinations required to copy
class Tap:
    def __init__(self):
        self.win = visual.Window([1200, 300],
                        color="white", units='pix')
        self.capList = units       
        self.locations=[(-400,0),(-300, 0),(-200, 0),(-100, 0),
                        (100, 0),(200, 0), (300,0),(400,0)]
        self.fixation= visual.ShapeStim(self.win, vertices=((0, -80), (0, 80), (0,0), 
                                                            (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, lineColor='grey')
    def setRectangles(self, word):
        """Create rectangles (visual.Rect) of height and width size and set their positions. Returns a list of rectangles """    
        self.rectangles = [visual.Rect(self.win, size = (120,120),fillColor='grey', lineColor='grey',
                                       units="pix") for i in range(len(self.capList))]
        self.colors = []
        for cap in self.capList:
            if cap not in word:
                self.colors.append('grey')
            elif cap in word:
                if cap in clusters:
                    self.colors[-1] = 'black'
                self.colors.append('black')                   

        [rectangle.setPos(location) for rectangle,location in zip(self.rectangles,self.locations)]
        [rectangle.setFillColor(color) for rectangle,color in zip(self.rectangles,self.colors)]
        [rectangle.setLineColor(color) for rectangle,color in zip(self.rectangles,self.colors)]

    def drawStims(self,stims):
        [stim.draw() for stim in stims]
        
tap=Tap()

# dictionary of tranlations from 3-letter code to full word
transKeys = {'tr':'R','vl':'L','oo':'U','ee':'X'}

#create fullword screen shots (blue,yellow,red appear together)
tap.setRectangles('www')
tap.drawStims(tap.rectangles)
tap.win.flip()
tap.win.getMovieFrame()
tap.win.saveMovieFrames('AAA_FF.png')     
for curWord in words:
    tap.setRectangles(curWord)
    tap.drawStims(tap.rectangles)
    tap.win.flip()
    tap.win.getMovieFrame()
    for i in transKeys.keys(): #
        curWord = curWord.replace(transKeys[i], i)
    tap.win.saveMovieFrames(curWord + '_FF.png') 
    core.wait(.2)
    print curWord
tap.win.close()
