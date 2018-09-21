# FF_task
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 06 12:23:19 2018
8c4
@author: Arella Gussow
"""

import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui

#define keys to be used and corresponding phonemes from stim creation
vowels=['U','a','x','i']
onsets=['S','C','g','k']
codas=['b','p','f','v']

capKeys = {'S':'1','C':'2','g':'3','k':'4',
          'U':'c','a':'v','x':'n','i':'m','b':'8','p':'9','f':'0','v':'minus'}
keys=capKeys.values()


### importing trials list from csv file ###
sep=','
def importTrials(numTrials):
    bTrial= open ('8wFF_stim.csv', 'rb')
    colNames = bTrial.next().rstrip().split(sep)
    reader=csv.DictReader(bTrial)
    global trialsList
    trialsList = []
    for t in range(numTrials):
        trialStr=bTrial.next().rstrip().split(sep)
        assert len(trialStr) == len(colNames)
        trialDict = dict(zip(colNames, trialStr))
        trialsList.append(trialDict)
importTrials(10)

random.shuffle(trialsList)



#
##still under old version
#hand = {'t':'Right','d':'Right','b':'Right',
#                   'p':'Right','k':'Left','g':'Left',
#                   'c':'Left','j':'Left',
#                   'e':'Left','i':'Right',
#                   'u':'Left','y':'Right'}


#finger = {'T':'ring','D':'ring','S':'mid',
#                   'Z':'mid','K':'mid', 'G': 'mid',
#                   'F':'ring','V':'ring',
#                   'A':'ind','E':'ind',
#                   'I':'ind','i':'ind'}



##running from pre-saved pics
win = visual.Window([800, 500], fullscr=True,
                        color="white", units='pix')
breakText=visual.TextStim(win=win, height=40,
                 text="Please take a short break. Press 'c' to continue.",
                 color='grey')
endText=visual.TextStim(win=win, height=40,
                 text="All Done! Please call the experimenter.",
                 color='grey')

wrongText=visual.TextStim(win=win, height=40,
                 text="Look at the pattern again and give it another try.",
                 color='grey')


fixation= visual.ShapeStim(win, vertices=((0, -80), (0, 80), (0,0), 
                                               (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey')

pic1 = visual.ImageStim(win=win, mask=None,interpolate=False,pos=(0,0), size=(800,500))
picW1 = visual.ImageStim(win=win, mask=None,interpolate=False,pos=(-300,0), size=(127,123))
picW2 = visual.ImageStim(win=win, mask=None,interpolate=False,pos=(-100,0), size=(127,123))
picW3 = visual.ImageStim(win=win, mask=None,interpolate=False,pos=(100,0), size=(127,123))
picW4 = visual.ImageStim(win=win, mask=None,interpolate=False,pos=(300,0), size=(127,123))


##shows keyboard template, with three keys colored blue, yellow, red (order of press).
##then shows question mark and waits for paricipant to key in the same pattern. 
## if wrong, text shows up saying so and they must try again.


with open('subject'+'_pilotTest8w.txt','w') as resultsFile:
    core.wait(2)
    breakTime=core.Clock()
    trialNum=0
    for trial in trialsList:
        trialNum+=1
        wordPos=0
        fixation.draw()
        win.flip()
        core.wait(1)              
        picW1.setImage('Shapes\shapesOGnames\\'+trial['w1']+'.png')
        picW2.setImage('Shapes\shapesOGnames\\'+trial['w2']+'.png')
        picW3.setImage('Shapes\shapesOGnames\\'+trial['w3']+'.png')
        picW4.setImage('Shapes\shapesOGnames\\'+trial['w4']+'.png')
        picW1.draw()
        picW2.draw()
        picW3.draw()
        picW4.draw()
        core.wait(0.5)
        win.flip()
        capInd=1
        for rep in range(1,4):
            for curWord in trial['fullTrial'].split():
                for curTap in curWord:
                    timer=core.Clock()
                    response=(event.waitKeys(keyList=keys))[0]
                    RT=int(timer.getTime()*(1000))
                    tapAcc=1 if response==capKeys[curTap] else 0              
                    capInd+=1
                    string=[str(var) for var in rep, trialNum, wordPos, curWord,
                            capInd, curTap, response, 
                                capKeys[curTap], tapAcc, RT]
                    print string                             
                    line='\t'.join(string) + '\n'
                    resultsFile.write(line)
                    resultsFile.flush()                                     
        wordPos+=1
        core.wait(.5)           
        fixation.draw()
        win.flip()
        core.wait(.5)
                
        if int(breakTime.getTime())>40:
            breakClick=False
            while not breakClick:
                breakText.draw()
                win.flip()
                stop= event.waitKeys(['c','q'])
                if stop==['c']:
                    breakTime.reset()
                    breakClick=True
                elif stop==['q']:
                    win.close()
                    core.quit()
    
    endText.draw()
    resultsFile.close()
    win.flip()
    core.wait(5)
    win.close()
win.close()
core.quit()
