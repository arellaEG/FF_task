###################################
########fill in subject ID #######

subject =''

###################################
###################################

# presents four word from TT trial, one under the other, for participants to read
# little blue dot on the left serves as pacer - marking which word should
# be said; moving at a predetermined speed "pacerTempo"

import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui, microphone
from pyo import *



### R = tr, L = vl, x = ee. changed for programming purposes of keeping all words same length
units=['t','R','v','L','eb','xb','ig','ug']
onsets=['t','R','v','L']
rhymes=['eb','xb','ig','ug']
pacerTempo = .45 # speed of pacer


transLetter = {'R':'tr', 'L':'fl', 'x':'ee','u': 'oo'}


win = visual.Window([800, 500], fullscr=True,
                        color="white", units='pix')

breakText=visual.TextStim(win=win, height=40,
                 text="Please take a short break. Press 'c' to continue.",
                 color='black')

endText=visual.TextStim(win=win, height=40,
                 text="All Done! Please call the experimenter.",
                 color='black')

pacer= visual.Circle(win=win, radius = 20, fillColor='blue') # blue dot that marks which word should be pressed

fixationView = visual.Circle(win=win, radius = 40, fillColor='red', pos=(-250,310)) # red circle for viewing time


fixationCross= visual.ShapeStim(win, vertices=((0, -80), (0, 80), (0,0),  
                                               (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey') # used between trials

word1 = visual.TextStim(win=win,pos=(0,300), height = 60, color='black')
word2 = visual.TextStim(win=win,pos=(0,100), height = 60, color='black')
word3 = visual.TextStim(win=win,pos=(0,-100), height = 60, color='black')
word4 = visual.TextStim(win=win,pos=(0,-300), height = 60, color='black')



sep=','
import io
def importTrials(numTrials):
    bTrial= open ('FF_bw/TTstim.csv', 'rb') 
    colNames = bTrial.next().rstrip().split(sep)
    reader=csv.DictReader(bTrial)
    global trialsList
    trialsList = []
    for t in range(numTrials):
        trialStr=bTrial.next().rstrip().split(sep)
        assert len(trialStr) == len(colNames)
        trialDict = dict(zip(colNames, trialStr))
        trialsList.append(trialDict)
importTrials(32)
random.shuffle(trialsList)
trialsList[0] # just looking

headers=["trialNum", "trialType", "itemID", "rep", "wordInd", "curWord"]


def write4():   
        word1.draw()
        word2.draw()
        word3.draw()
        word4.draw()
    
# define expected keys per word

     
with open(subject+'_TTwb.txt','wb') as resultsFile:
    Rwriter=csv.DictWriter(resultsFile, fieldnames=headers)
    Rwriter.writeheader()
    core.wait(2)
    breakTime=core.Clock()
    trialNum=0   
    for trial in trialsList:
        trialNum+=1
        fixationCross.draw()
        win.flip()
        core.wait(1)
        t = trial['fullTrial'].split()
        w1,w2,w3,w4=t
        word1.setText(w1)
        word2.setText(w2)
        word3.setText(w3)
        word4.setText(w4)
        write4()
        fixationView.draw() # fixation to allow brief viewing - 2 sec of big red circle
        win.flip()
        core.wait(2)
        write4()
        win.flip() 
        core.wait(.4) # big red circle disappears, nothing on screen for 1 sec ;
                     # then small blue circle appears and participants must begin              

        for rep in range(1,4):
            wordInd=0 # index of word within trial (first word, second...)
            write4()
            pacer.pos = (-250,300)
            pacer.draw()
            win.flip()
            for curWord in trial['fullTrial'].split():
                wordInd += 1           
                write4()
                pacer.draw()
                win.flip()
                
                reactionTime=core.Clock()
                pacerTime=core.Clock()              
                core.wait(pacerTempo-(pacerTime.getTime())) # wait full time even if participant answered before time's up

                string=[str(var) for var in trialNum, trial['type'], trial['ID'], 
                        rep, wordInd, curWord]              
                print string               
                line='\t'.join(string) + '\n'
                resultsFile.write(line)
                resultsFile.flush()
                pacer.pos -=(0,200)                                  
        fixationCross.draw()
        win.flip()
        core.wait(.5)
        if int(breakTime.getTime())>10:
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
